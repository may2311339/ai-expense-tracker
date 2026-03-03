from datetime import date
import calendar

def calculate_metrics(user, expenses):
    today = date.today()

    month_expenses = [
        e for e in expenses
        if e.date.month == today.month and e.date.year == today.year
    ]

    month_total = sum(e.amount for e in month_expenses)
    budget = user.monthly_budget
    budget_exceeded = month_total > budget

    days_in_month = calendar.monthrange(today.year, today.month)[1]
    predicted_month = (month_total / today.day) * days_in_month if today.day else 0

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

    return {
        "month_total": month_total,
        "budget": budget,
        "budget_exceeded": budget_exceeded,
        "predicted_month": predicted_month,
        "financial_score": financial_score,
        "score_label": score_label
    }