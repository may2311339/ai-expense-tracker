from flask import Blueprint, render_template, request, redirect, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
import calendar

from .models import User, Expense
from .extensions import db
from .services.expense_service import create_expense, delete_expense

main = Blueprint("main", __name__)

# -------------------------
# AUTH
# -------------------------

@main.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if User.query.filter_by(username=username).first():
            flash("Username already exists")
            return redirect("/register")

        user = User(
            username=username,
            password=generate_password_hash(password),
            monthly_budget=10000
        )

        db.session.add(user)
        db.session.commit()

        flash("Registered successfully. Please login.")
        return redirect("/login")

    return render_template("register.html")


@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password, password):
            flash("Invalid credentials")
            return redirect("/login")

        session["user_id"] = user.id
        return redirect("/")

    return render_template("login.html")


@main.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# -------------------------
# DASHBOARD
# -------------------------

@main.route("/")
def index():
    if "user_id" not in session:
        return redirect("/login")

    user = User.query.get(session["user_id"])
    expenses = Expense.query.filter_by(user_id=user.id)\
        .order_by(Expense.date.desc()).all()

    total = sum(e.amount for e in expenses)

    today = date.today()

    # Monthly data
    month_expenses = [
        e for e in expenses
        if e.date.month == today.month and e.date.year == today.year
    ]

    month_total = sum(e.amount for e in month_expenses)

    budget = user.monthly_budget
    budget_exceeded = month_total > budget

    days_in_month = calendar.monthrange(today.year, today.month)[1]
    predicted_month = (month_total / today.day) * days_in_month if today.day else 0

    # Financial score
    if budget == 0:
        financial_score = 100
    else:
        ratio = month_total / budget
        financial_score = max(0, int(100 - (ratio * 100)))

    score_label = (
        "Excellent" if financial_score >= 80
        else "Good" if financial_score >= 60
        else "Warning"
    )

    # Categories
    categories = ["Food", "Travel", "Bills", "Shopping", "Other"]

    # Pie chart data
    pie_data = {}
    for e in expenses:
        pie_data[e.category] = pie_data.get(e.category, 0) + e.amount

    pie_labels = list(pie_data.keys())
    pie_values = list(pie_data.values())

    # Daily chart data
    daily_data = {}
    for e in month_expenses:
        day = e.date.day
        daily_data[day] = daily_data.get(day, 0) + e.amount

    daily_labels = list(daily_data.keys())
    daily_values = list(daily_data.values())

    insight = None
    if budget_exceeded:
        insight = "⚠ You are overspending this month."

    return render_template(
        "index.html",
        expenses=expenses,
        total=total,
        month_total=month_total,
        budget=budget,
        budget_exceeded=budget_exceeded,
        predicted_month=predicted_month,
        financial_score=financial_score,
        score_label=score_label,
        categories=categories,
        pie_labels=pie_labels,
        pie_values=pie_values,
        daily_labels=daily_labels,
        daily_values=daily_values,
        today=today.isoformat(),
        insight=insight
    )


# -------------------------
# BUDGET UPDATE
# -------------------------

@main.route("/update_budget", methods=["POST"])
def update_budget():
    if "user_id" not in session:
        return redirect("/login")

    user = User.query.get(session["user_id"])
    user.monthly_budget = float(request.form["budget"])
    db.session.commit()

    flash("Budget updated")
    return redirect("/")


# -------------------------
# ADD EXPENSE
# -------------------------

@main.route("/add", methods=["POST"])
def add():
    if "user_id" not in session:
        return redirect("/login")

    create_expense(session["user_id"], request.form)
    return redirect("/")


# -------------------------
# DELETE
# -------------------------

@main.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    if "user_id" not in session:
        return redirect("/login")

    expense = Expense.query.get_or_404(id)

    if expense.user_id != session["user_id"]:
        return redirect("/")

    delete_expense(expense)
    return redirect("/")


# -------------------------
# EDIT
# -------------------------

@main.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    if "user_id" not in session:
        return redirect("/login")

    expense = Expense.query.get_or_404(id)

    if expense.user_id != session["user_id"]:
        return redirect("/")

    categories = ["Food", "Travel", "Bills", "Shopping", "Other"]

    if request.method == "POST":
        expense.description = request.form["description"]
        expense.amount = float(request.form["amount"])
        expense.category = request.form["category"]
        expense.date = datetime.strptime(
            request.form["date"], "%Y-%m-%d"
        ).date()

        db.session.commit()
        return redirect("/")

    return render_template("edit.html", e=expense, categories=categories)