# 🚀 AI Expense Tracker

A modular full-stack web application built with Flask that allows users to securely manage and analyze personal expenses.

The application follows clean backend architecture principles using service-layer separation and the Flask application factory pattern.

---

## ✨ Features

- 🔐 User Authentication (Register / Login / Logout)
- 🔑 Secure password hashing (Werkzeug)
- ➕ Add, ✏ Edit, ❌ Delete Expenses
- 📊 Category-wise expense tracking
- 📅 Monthly expense summary
- 💰 Budget management
- 📈 Financial score calculation
- 🥧 Pie chart analytics (Chart.js)
- 📊 Daily expense bar chart
- 🌙 Dark/Light theme toggle (Tailwind CSS)
- 🏗 Modular backend structure

---

## 🏗 Architecture

This project follows:

- Flask Application Factory Pattern
- Service Layer Pattern
- Separation of Concerns
- ORM-based database modeling (SQLAlchemy)

### Project Structure

AI-Expense-Tracker/
│
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   ├── extensions.py
│   ├── services/
│   │   └── expense_service.py
│   └── templates/
│
├── config.py
├── run.py
├── requirements.txt
└── README.md

---

## 🛠 Tech Stack

### Backend
- Python
- Flask
- SQLAlchemy
- SQLite
- Gunicorn (for production)

### Frontend
- HTML
- Tailwind CSS (CDN)
- Jinja2 Templates
- Chart.js

### Tools
- Git
- GitHub

---

## ⚙️ Local Setup

1. Clone repository:
   git clone https://github.com/YOUR_USERNAME/AI-Expense-Tracker.git

2. Navigate into project:
   cd AI-Expense-Tracker

3. Create virtual environment:
   python -m venv venv
   venv\Scripts\activate  (Windows)

4. Install dependencies:
   pip install -r requirements.txt

5. Run the app:
   python run.py

6. Open in browser:
   http://127.0.0.1:5000

---

## 🚀 Future Improvements

- REST API version
- JWT authentication
- PostgreSQL support
- Docker containerization
- Cloud deployment
- Advanced financial analytics

---

## 👨‍💻 Author

Mayank Sharma  
B.Tech Computer Science (2027)
