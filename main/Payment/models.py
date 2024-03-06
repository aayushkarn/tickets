from main.db import db
from datetime import datetime
from enum import Enum

class PaymentStatus(Enum):
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"

class PaymentMethod(Enum):
    KHALTI = "KHALTI"
    MOCK = "MOCK"

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userid = db.Column(db.Integer, db.ForeignKey("users.id"))
    transaction_id = db.Column(db.String(100))
    booking_id = db.Column(db.Integer, db.ForeignKey("booking.id"))
    price = db.Column(db.Float)
    payment_method = db.Column(db.Enum(PaymentMethod))
    payment_status = db.Column(db.Enum(PaymentStatus))
    bookingref = db.relationship('Booking', backref=db.backref("booking"), lazy=True)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, userid, transaction_id, booking_id, price, payment_method, payment_status):
        self.userid = userid
        self.transaction_id = transaction_id
        self.booking_id = booking_id
        self.price = price
        self.payment_method = payment_method
        self.payment_status = payment_status