from main.db import db
from datetime import datetime
from enum import Enum

class PaymentStatus(Enum):
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"

class PaymentMethod(Enum):
    KHALTI = "KHALTI"

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userid = db.Column(db.Integer, db.ForeignKey("users.id"))
    transaction_id = db.Column(db.String(100), unique=True)
    booking_id = db.Column(db.Integer, db.ForeignKey("booking.id"))
    price = db.Column(db.Float)
    payment_method = db.Column(db.Enum(PaymentMethod))
    payment_status = db.Column(db.Enum(PaymentStatus))
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __init__(self) -> None:
        super().__init__()