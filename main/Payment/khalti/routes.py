import uuid
from flask import flash, redirect, request, session, url_for
from main.Authentication.utils import commitDB, login_required
from main.Booking.models import BookingStatus
from main.Payment.khalti.khalti import initkhalti, verifyPayment
from main.Payment.models import PaymentMethod, PaymentStatus
from main.Payment.routes import Blueprint
from main.Payment.utils import CreatePayment, generatePaymentInfo, getPaymentByTransactionId, seats_selected
from main.Ticket.utils import generate_ticket

khalti = Blueprint("khalti", __name__)

@khalti.route("/initiate/", methods=['POST'])
@login_required
@seats_selected
def initiate_payment():
    csrf_token = request.form.get("csrf_token")
   
    info = generatePaymentInfo()
    
    res = initkhalti()
    if not 'detail' in res:
        # print(res)
        return redirect(res['payment_url'])

    
    flash("Something went wrong")
    return redirect(url_for("payment.errorPage"))

@khalti.route("/finaliaze/")
@login_required
@seats_selected
def finalize_payment():
    info = generatePaymentInfo()

    pidx = request.args.get('pidx')
    res = verifyPayment(pidx)
    print(res)
    
    tagId = uuid.uuid4().hex
    if res['status'] == "Completed":
        for movie in info['movieInfo']:
            pay = CreatePayment(info['userid'], res['transaction_id'], movie['bookingid'],movie['price'],PaymentMethod.KHALTI,PaymentStatus.SUCCESS)
            generate_ticket(tagId, info['userid'], pay.id, movie['scheduleid'])

        pays = getPaymentByTransactionId(res['transaction_id'])
        if pays != []:
            for pay in pays:
                pay.bookingref.status = BookingStatus.RESERVED
                commitDB()
        session.pop('booking', None)
        # ticket generation
        return redirect(url_for("ticket.index", tagid=tagId))
    else:
        for movie in info['movieInfo']:
            CreatePayment(info['userid'], None, movie['bookingid'],movie['price'],PaymentMethod.KHALTI,PaymentStatus.FAILURE)
        return redirect(url_for("payment.errorPage"))
    return render_template("payment_finalize.html")