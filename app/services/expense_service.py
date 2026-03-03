from app.models import Expense
from app.extensions import db
from datetime import datetime

def create_expense(user_id, form):
    expense = Expense(
        description=form["description"],
        amount=float(form["amount"]),
        category=form["category"],
        date=datetime.strptime(form["date"], "%Y-%m-%d").date(),
        user_id=user_id
    )

    db.session.add(expense)
    db.session.commit()


def delete_expense(expense):
    db.session.delete(expense)
    db.session.commit()