import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

INSTANCE_PATH = os.path.join(BASE_DIR, "instance")
os.makedirs(INSTANCE_PATH, exist_ok=True)

DB_PATH = os.path.join(INSTANCE_PATH, "expenses.db")

class Config:
    SECRET_KEY = "super-secret-key-change-this"
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + DB_PATH
    SQLALCHEMY_TRACK_MODIFICATIONS = False