from flask import Blueprint, Config, flash, redirect, render_template, request, session, url_for
import requests

from main.Authentication.utils import getUserByUsername, login_required
from main.Booking.models import BookingStatus
from main.Movie.utils import strDateToPythonDate
from .models import Payment, PaymentMethod, PaymentStatus
from .utils import *

from main.config import Config
from main.Payment.khalti.routes import khalti
from main.Payment.mock.routes import mock

payment = Blueprint("payment", __name__, template_folder="templates", static_folder='static')
payment.register_blueprint(khalti, url_prefix='/khalti/')
payment.register_blueprint(mock, url_prefix='/mock/')

@payment.route("/")
@login_required
@seats_selected
# TODO: restrict the user's payment only to user 
def home():
    info = generatePaymentInfo()
    return render_template("payment_home.html", uniqueid= info['uniqueid'], name=info['name'], movieInfo=info['movieInfo'], totalPrice=info['totalPrice'], email=info['email'])

# @payment.route("/initiate/", methods=['POST'])
# @login_required
# @seats_selected
# def initiate_payment():
#     csrf_token = request.form.get("csrf_token")
   
#     info = generatePaymentInfo()
    
#     res = initkhalti()
#     if not 'detail' in res:
#         # print(res)
#         for movie in info['movieInfo']:
#             CreatePayment(info['userid'], info['transactionid'], movie['bookingid'],movie['price'],PaymentMethod.KHALTI,PaymentStatus.FAILURE)
#         return redirect(res['payment_url'])

    
#     flash("Something went wrong")
#     return redirect(url_for("home.index"))

# @payment.route("/finaliaze/")
# @login_required
# @seats_selected
# def finalize_payment():
#     pidx = request.GET.get('pidx')
#     res = verifyPayment(pidx)
#     print(res)
    
#     if res['status'] == "Completed":
#         pays = getPaymentByTransactionId(res["transaction_id"])
#         if pays != []:
#             for pay in pays:
#                 pay.status = PaymentStatus.SUCCESS
#                 pay.bookingref.status = BookingStatus.RESERVED
#                 commitDB()
#         session.pop('booking', None)
#         return redirect(url_for("home.index"))
#     else:
#         return redirect(url_for("payment.errorPage"))
#     return render_template("payment_finalize.html")

@payment.route("/error/")
@login_required
def errorPage():
    return render_template("error.html")

# @payment.route("/redirect-payment/")
# @login_required
# def redirectTicket(tagid):
#     redirect_url = url_for("ticket.index", tagid=tagid)
#     print(redirect_url)
#     return render_template('payment_finalize.html')