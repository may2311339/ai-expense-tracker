from flask import Flask, render_template, request, redirect, flash, make_response, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date, datetime
from sqlalchemy import func
import csv, io, os

# ----------------------
# APP CONFIG
# ----------------------

app = Flask(__name__)

# create instance folder safely
os.makedirs(app.instance_path, exist_ok=True)

# database config
app.config["SQLALCHEMY_DATABASE_URI"] = \
    "sqlite:///" + os.path.join(app.instance_path, "expenses.db")

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# session security
app.config["SECRET_KEY"] = "super_secure_secret_key_123"

app.config["SESSION_COOKIE_HTTPONLY"] = True

app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

# for local development keep False
app.config["SESSION_COOKIE_SECURE"] = False

db = SQLAlchemy(app)

MONTHLY_BUDGET = 1000

CATEGORIES = [
    "Food",
    "Transport",
    "Rent",
    "Utilities",
    "Health",
    "Entertainment",
    "Other"
]


# ----------------------
# DATABASE MODELS
# ----------------------

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(200),
        nullable=False
    )


class Expense(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    description = db.Column(
        db.String(120),
        nullable=False
    )

    amount = db.Column(
        db.Float,
        nullable=False
    )

    category = db.Column(
        db.String(50),
        nullable=False
    )

    date = db.Column(
        db.Date,
        default=date.today
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )


# create tables
with app.app_context():
    db.create_all()


# ----------------------
# HELPER FUNCTIONS
# ----------------------

def parse_date(s):

    try:
        return datetime.strptime(
            s,
            "%Y-%m-%d"
        ).date()

    except Exception:
        return date.today()


def get_current_user():

    user_id = session.get("user_id")

    if not user_id:
        return None

    return db.session.get(User, user_id)


# ----------------------
# AUTH ROUTES
# ----------------------

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form.get("username", "").strip()

        password = request.form.get("password", "").strip()

        if not username or not password:

            flash("All fields required")

            return redirect("/register")

        existing = User.query.filter_by(
            username=username
        ).first()

        if existing:

            flash("Username already exists")

            return redirect("/register")

        hashed = generate_password_hash(password)

        user = User(
            username=username,
            password=hashed
        )

        db.session.add(user)

        db.session.commit()

        flash("Registration successful")

        return redirect("/login")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username", "")

        password = request.form.get("password", "")

        user = User.query.filter_by(
            username=username
        ).first()

        if user and check_password_hash(
            user.password,
            password
        ):

            session["user_id"] = user.id

            flash("Login successful")

            return redirect("/")

        flash("Invalid credentials")

    return render_template("login.html")


@app.route("/logout")
def logout():

    session.clear()

    flash("Logged out")

    return redirect("/login")


# ----------------------
# DASHBOARD
# ----------------------

@app.route("/")
def index():

    user = get_current_user()

    if not user:
        return redirect("/login")

    expenses = Expense.query.filter_by(
        user_id=user.id
    ).order_by(
        Expense.date.desc()
    ).all()

    total = sum(e.amount for e in expenses)

    today = date.today()

    # pie chart data
    pie = db.session.query(
        Expense.category,
        func.sum(Expense.amount)
    ).filter_by(
        user_id=user.id
    ).group_by(
        Expense.category
    ).all()

    pie_labels = [x[0] for x in pie]

    pie_values = [float(x[1]) for x in pie]

    # daily chart data
    daily = db.session.query(
        Expense.date,
        func.sum(Expense.amount)
    ).filter_by(
        user_id=user.id
    ).group_by(
        Expense.date
    ).all()

    daily_labels = [str(x[0]) for x in daily]

    daily_values = [float(x[1]) for x in daily]

    # month total
    month_total = db.session.query(
        func.sum(Expense.amount)
    ).filter(
        Expense.user_id == user.id,
        func.strftime(
            "%Y-%m",
            Expense.date
        ) == today.strftime("%Y-%m")
    ).scalar() or 0

    budget_exceeded = month_total >= MONTHLY_BUDGET

    # prediction
    avg = db.session.query(
        func.avg(Expense.amount)
    ).filter_by(
        user_id=user.id
    ).scalar() or 0

    predicted_month = avg * 30

    # insight
    top = db.session.query(
        Expense.category,
        func.sum(Expense.amount)
    ).filter_by(
        user_id=user.id
    ).group_by(
        Expense.category
    ).order_by(
        func.sum(Expense.amount).desc()
    ).first()

    insight = ""

    if top:
        insight = "Highest spending category: " + top[0]

    # financial score
    score = 100

    if month_total > MONTHLY_BUDGET:
        score -= 30

    if predicted_month > MONTHLY_BUDGET:
        score -= 20

    score = max(score, 0)

    if score >= 80:
        score_label = "Excellent"
    elif score >= 60:
        score_label = "Good"
    else:
        score_label = "Needs Improvement"

    return render_template(
        "index.html",
        expenses=expenses,
        total=total,
        categories=CATEGORIES,
        today=today.isoformat(),
        pie_labels=pie_labels,
        pie_values=pie_values,
        daily_labels=daily_labels,
        daily_values=daily_values,
        month_total=month_total,
        budget=MONTHLY_BUDGET,
        budget_exceeded=budget_exceeded,
        predicted_month=predicted_month,
        insight=insight,
        financial_score=score,
        score_label=score_label
    )


# ----------------------
# ADD EXPENSE
# ----------------------

@app.route("/add", methods=["POST"])
def add():

    user = get_current_user()

    if not user:
        return redirect("/login")

    amount = float(
        request.form.get("amount", 0)
    )

    expense = Expense(
        description=request.form.get("description", ""),
        amount=amount,
        category=request.form.get("category", ""),
        date=parse_date(
            request.form.get("date", "")
        ),
        user_id=user.id
    )

    db.session.add(expense)

    db.session.commit()

    flash("Expense added")

    return redirect("/")


# ----------------------
# DELETE
# ----------------------

@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):

    user = get_current_user()

    if not user:
        return redirect("/login")

    expense = Expense.query.get_or_404(id)

    if expense.user_id != user.id:
        return redirect("/")

    db.session.delete(expense)

    db.session.commit()

    flash("Deleted")

    return redirect("/")


# ----------------------
# EDIT
# ----------------------

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):

    user = get_current_user()

    if not user:
        return redirect("/login")

    expense = Expense.query.get_or_404(id)

    if expense.user_id != user.id:
        return redirect("/")

    if request.method == "POST":

        expense.description = request.form.get("description", "")

        expense.amount = float(
            request.form.get("amount", 0)
        )

        expense.category = request.form.get("category", "")

        expense.date = parse_date(
            request.form.get("date", "")
        )

        db.session.commit()

        flash("Updated")

        return redirect("/")

    return render_template(
        "edit.html",
        e=expense,
        categories=CATEGORIES
    )


# ----------------------
# EXPORT CSV
# ----------------------

@app.route("/export")
def export():

    user = get_current_user()

    if not user:
        return redirect("/login")

    output = io.StringIO()

    writer = csv.writer(output)

    writer.writerow([
        "Date",
        "Description",
        "Category",
        "Amount"
    ])

    expenses = Expense.query.filter_by(
        user_id=user.id
    ).all()

    for e in expenses:

        writer.writerow([
            e.date,
            e.description,
            e.category,
            e.amount
        ])

    response = make_response(
        output.getvalue()
    )

    response.headers[
        "Content-Disposition"
    ] = "attachment; filename=expenses.csv"

    response.headers[
        "Content-type"
    ] = "text/csv"

    return response


# ----------------------
# RUN APP
# ----------------------

if __name__ == "__main__":
    app.run(debug=True)
