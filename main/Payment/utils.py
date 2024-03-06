from datetime import date, time
from functools import wraps
import json
import uuid
from flask import redirect, session, url_for
from main import Booking

from main.Authentication.utils import commitDB, deleteFromDB, getUserByUsername, saveToDB
from main.Booking.utils import getBookingById
from main.Payment.models import Payment
from main.Schedule.utils import getPriceListById, getScheduleById
from main.Seats.utils import getSeatById

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (date, time)):
            return obj.isoformat()
        return super().default(obj)

def genUniqueId():
    return uuid.uuid4().hex

def seats_selected(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'booking' not in session:            
            return redirect(url_for('home.index'))
        return func(*args, *kwargs)
    return wrapper

def generatePaymentInfo():
    # print(session['booking'])
    uniqueid = genUniqueId()
    user = getUserByUsername(session['user'])
    name = user.name
    email = user.email
    totalPrice = 0.0
    movieInfo = []
    for b in session['booking']:
        bookingData = getBookingById(b)
        seat = getSeatById(bookingData.seatid)
        # print(b)
        # print(bookingData.seatid)
        # print(bookingData.scheduleid)
        schedule = getScheduleById(bookingData.scheduleid)

        seatsPrice = getPriceListById(schedule.price)
        responseData = {}
        for s in seatsPrice:
            if seat.type == s.seat_type:
                # print(s.seat_type)
                totalPrice += s.price
        
                responseData = {'title':schedule.movieref.title, 'duration':schedule.movieref.duration,'date':schedule.start_time.date(), 'time':schedule.start_time.time(), 'seat_id':bookingData.seatid, 'screen':schedule.screenref.name, 'seat_row':seat.row, 'seat_column': seat.column, 'seat_type': seat.type.value, "price":s.price, "bookingid":bookingData.id, "scheduleid":schedule.id}

                break
        responseData['bookingid'] = bookingData.id
        movieInfo.append(responseData)
        
        # print("\n")

    return {'uniqueid':uniqueid, 'name':name, 'movieInfo':movieInfo, 'totalPrice': totalPrice, 'email':email, 'userid':user.id}


def emptySeats():
    print("called emprt")
    # session.pop("seats", None)

def freeHolds():
    print("called")
    # for b in session['booking']:
    #     Booking.query.filter_by(id=b.id).delete()

def CreatePayment(userid, transactionid, bookingid, price, payment_method, payment_status):
    pay = Payment(userid=userid, transaction_id=transactionid, booking_id=bookingid, price=price, payment_method=payment_method, payment_status=payment_status)
    saveToDB(pay)
    return pay

def getPaymentByTransactionId(transactionid):
    pay = Payment.query.filter_by(transaction_id=transactionid).all()
    return pay

def deletePaymentWithNullBookingId():
    pays = Payment.query.filter_by(booking_id=None).all()
    if pays != []:
        for pay in pays:   
            deleteFromDB(pay)

def getPaymentById(id):
    return Payment.query.filter_by(id=id).first()