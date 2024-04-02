from flask import Blueprint, redirect, session, url_for
import uuid

from main.Authentication.utils import commitDB, login_required
from main.Booking.models import BookingStatus
from main.Payment.models import PaymentMethod, PaymentStatus
from main.Payment.utils import CreatePayment, generatePaymentInfo, getPaymentByTransactionId, seats_selected
from main.Ticket.utils import generate_ticket

mock = Blueprint("mock", __name__)

@mock.route("/initiate/", methods=['POST'])
@login_required
@seats_selected
def initiate_payment():
    
    info = generatePaymentInfo()
    tagId = uuid.uuid4().hex
    for movie in info['movieInfo']:
        pay = CreatePayment(info['userid'], info['uniqueid'], movie['bookingid'],movie['price'],PaymentMethod.MOCK,PaymentStatus.SUCCESS)
        generate_ticket(tagId, info['userid'], pay.id, movie['scheduleid'])
    pays = getPaymentByTransactionId(info["uniqueid"])
    for pay in pays:
        pay.bookingref.status = BookingStatus.RESERVED
        commitDB()
    session.pop('booking', None)

    # return redirect(url_for("payment.redirectTicket", tagid=tagId))

    return redirect(url_for("ticket.index", tagid=tagId))

    