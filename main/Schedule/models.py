from main.db import db 
from datetime import datetime
from enum import Enum

from main.Seats.models import SeatType

class ScheduleStatus(Enum):
    UPCOMING = 'UPCOMING'
    EXPIRED = 'EXPIRED'
    ONGOING = 'ONGOING'

class PriceStatus(Enum):
    ENABLED = 'ENABLED'
    DISABLED = 'DISABLED'

# # movie schedule and screen available
class Schedule(db.Model):
    __tablename__ = "schedule"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    movie = db.Column(db.Integer, db.ForeignKey('movies.id'))
    screen = db.Column(db.Integer, db.ForeignKey('screen.id'))
    price = db.Column(db.String(100), db.ForeignKey('prices.uniqueid'))
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    movieref = db.relationship('Movie', backref=db.backref('schedules'), lazy=True)
    screenref = db.relationship('Screen', backref=db.backref('schedules'), lazy=True)
    priceref = db.relationship('Price', backref=db.backref('schedules'), lazy=True)
    status = db.Column(db.Enum(ScheduleStatus), default=ScheduleStatus.UPCOMING)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def __init__(self, movie, screen, price, start_time, end_time):
        self.movie = movie
        self.screen = screen
        self.price = price
        self.start_time = start_time
        self.end_time = end_time
    def __repr__(self):
        return f"{self.movieref.title} | {self.screenref.name} | {self.start_time} to {self.end_time}"
 


class Price(db.Model):
    __tablename__ = "prices"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uniqueid = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    seat_type = db.Column(db.Enum(SeatType), default=SeatType.CLASSIC)
    status = db.Column(db.Enum(PriceStatus), default=PriceStatus.ENABLED)
    price = db.Column(db.Float, nullable=False)

    def __init__(self, name, uniqueid, seat_type, status, price):
        self.name = name
        self.uniqueid = uniqueid
        self.seat_type = seat_type
        self.status = status
        self.price = price