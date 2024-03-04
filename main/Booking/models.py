from main.db import db 
from enum import Enum
from ..Seats.models import Seats
from datetime import datetime

class BookingStatus(Enum):
    RESERVED = "RESERVED"
    BOOKED = 'BOOKED'
    HOLD = "HOLD"
    UNRESERVED = 'UNRESERVED'

class Booking(db.Model):
    __tablename__ = "booking"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userid = db.Column(db.Integer, db.ForeignKey("users.id"))
    seatid = db.Column(db.Integer, db.ForeignKey("seats.id"))
    scheduleid = db.Column(db.Integer, db.ForeignKey("schedule.id"))
    status = db.Column(db.Enum(BookingStatus), default=BookingStatus.UNRESERVED)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def __init__(self, userid, seatid, scheduleid, status):
        self.userid = userid
        self.seatid = seatid
        self.scheduleid = scheduleid
        self.status = status