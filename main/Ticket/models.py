from datetime import datetime
from main import db
from enum import Enum

class TicketStatus(Enum):
    ACTIVE = "ACTIVE"
    EXPIRED = "EXPIRED"

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tagid = db.Column(db.String(100))
    qrcode = db.Column(db.String(100), unique=True)
    userid = db.Column(db.Integer, db.ForeignKey("users.id"))
    paymentid =  db.Column(db.Integer, db.ForeignKey("payment.id"))
    scheduleid = db.Column(db.Integer, db.ForeignKey("schedule.id"))
    paymentref = db.relationship('Payment', backref=db.backref("tickets"), lazy=True)
    scheduleref = db.relationship('Schedule', backref=db.backref("tickets"), lazy=True)
    ticket_status = db.Column(db.Enum(TicketStatus), default=TicketStatus.ACTIVE)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, tagid, qrcode, userid, paymentid, scheduleid):
        self.tagid = tagid
        self.qrcode = qrcode
        self.userid = userid
        self.paymentid = paymentid
        self.scheduleid = scheduleid