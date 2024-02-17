from main.db import db
from datetime import datetime

class Screen(db.Model):
    __tablename__ = "screen"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    unique_name = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def __rep__(self):
        return f"{self.name}"
    