from main.db import db 
from enum import Enum
from datetime import datetime

from ..Screen.models import Screen

class SeatType(Enum):
    CLASSIC = "CLASSIC"
    BUSINESS = "BUSINESS"
    EXCLUSIVE = "EXCLUSIVE"
    GAP = "GAP"

class Seats(db.Model):
    __tablename__ = "seats"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    row = db.Column(db.Integer)
    column = db.Column(db.Integer)
    type = db.Column(db.Enum(SeatType), default=SeatType.GAP)
    screen = db.Column(db.Integer, db.ForeignKey('screen.id'), nullable=True)
    # booking = db.relationship('Booking', backref='Seat', lazy=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def __init__(self, row, column, screen, type):
        self.row = row
        self.column = column
        self.type = type
        self.screen = screen

    def __repr__(self):
        return f"{Screen.query.filter_by(id=self.screen).first().name} {self.row},{self.column}"
