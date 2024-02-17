from main.db import db 
from datetime import datetime

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    is_superuser = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def __init__(self, name, email, username, password,is_superuser=None):
        self.name = name
        self.email = email
        self.username = username
        self.password = password
        self.is_superuser = is_superuser

# if not User.query.filter(username="admin").first():
#     db.session.add(User(name="Admin", username="admin", email="admin@a.com", password="password", is_superuser="True"))
# TODO: probably create a new model for admin