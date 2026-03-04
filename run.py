from app import create_app
from app.extensions import db

app = create_app()

def create_database():
    with app.app_context():
        db.create_all()

create_database()

if __name__ == "__main__":
    app.run()