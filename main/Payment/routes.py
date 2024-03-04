from flask import Blueprint, Config, flash, redirect, render_template, request, session, url_for
import requests

from main.Authentication.utils import getUserByUsername, login_required
from main.Movie.utils import strDateToPythonDate
from .models import Payment, PaymentMethod, PaymentStatus
from .utils import *

from .khalti.khalti import *
from main.config import Config

payment = Blueprint("payment", __name__, template_folder="templates")

@payment.route("/")
@login_required
@seats_selected
# TODO: restrict the user's payment only to user 
def home():
    info = generatePaymentInfo()
    return render_template("payment_home.html", transactionid= info['transactionid'], name=info['name'], movieInfo=info['movieInfo'], totalPrice=info['totalPrice'], email=info['email'])

@payment.route("/initiate/", methods=['POST'])
@login_required
@seats_selected
def initiate_payment():
    csrf_token = request.form.get("csrf_token")
   
    info = generatePaymentInfo()

    res = json.loads(initkhalti())
    if not 'detail' in res:
        return redirect(res['payment_url'])

    
    flash("Something went wrong")
    return redirect(url_for("home.index"))