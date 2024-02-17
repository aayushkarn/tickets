from main.db import db 
from datetime import datetime
from enum import Enum

class ScheduleStatus(Enum):
    UPCOMING = 'UPCOMING'
    EXPIRED = 'EXPIRED'
    ONGOING = 'ONGOING'
# # movie schedule and screen available
class Schedule(db.Model):
    __tablename__ = "schedule"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    movie = db.Column(db.Integer, db.ForeignKey('movies.id'))
    screen = db.Column(db.Integer, db.ForeignKey('screen.id'))
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    movieref = db.relationship('Movie', backref=db.backref('schedules'), lazy=True)
    screenref = db.relationship('Screen', backref=db.backref('schedules'), lazy=True)
    status = db.Column(db.Enum(ScheduleStatus), default=ScheduleStatus.UPCOMING)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def __init__(self, movie, screen, start_time, end_time):
        self.movie = movie
        self.screen = screen
        self.start_time = start_time
        self.end_time = end_time
    def __repr__(self):
        return f"{self.movieref.title}->{self.screenref.name}->{self.start_time} to {self.end_time}"
 