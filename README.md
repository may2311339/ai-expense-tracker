# 🚀 AI Expense Tracker

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-black)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-red)
![Render](https://img.shields.io/badge/Deployment-Render-purple)

Live Demo: https://ai-expense-tracker-whdx.onrender.com

A modular full-stack web application built with Flask that allows users to securely manage and analyze personal expenses.

The application follows clean backend architecture principles using service-layer separation and the Flask application factory pattern.

---

✨ Features

- 🔐 User Authentication (Register / Login / Logout)
- 🔑 Secure password hashing using Werkzeug
- ➕ Add expenses
- ✏️ Edit expenses
- ❌ Delete expenses
- 📂 Category-wise expense tracking
- 📊 Monthly expense summary
- 💰 Budget management
- 🧠 Financial score calculation
- 🥧 Pie chart analytics (Chart.js)
- 📈 Daily expense bar chart

---

🛠 Tech Stack

Backend

- Python
- Flask
- SQLAlchemy
- Gunicorn

Frontend

- HTML
- Tailwind CSS
- Chart.js

Deployment

- Render
- GitHub

---

📂 Project Structure

AI Expense Tracker
│
├── app
│   ├── routes.py
│   ├── models.py
│   ├── extensions.py
│   ├── services/
│   └── templates/
│
├── instance
│   └── expenses.db
│
├── run.py
├── config.py
├── requirements.txt
└── README.md

---

⚙️ Installation

Clone the repository

git clone https://github.com/may2311339/ai-expense-tracker.git

Navigate to the project directory

cd ai-expense-tracker

Create virtual environment

python -m venv venv

Activate virtual environment (Windows)

venv\Scripts\activate

Install dependencies

pip install -r requirements.txt

Run the application

python run.py

Open in browser

http://127.0.0.1:5000

---

📸 Screenshots

(Add screenshots of dashboard and analytics here)

Dashboard

"Dashboard" (screenshots/dashboard.png)

Analytics

"Analytics" (screenshots/analytics.png)

---

👨‍💻 Author

Mayank Sharma
BTech Computer Science (2027)

---

⭐ If you like this project, consider giving it a star on GitHub.