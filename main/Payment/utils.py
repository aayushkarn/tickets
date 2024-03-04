from datetime import date, time
from functools import wraps
import json
import uuid
from flask import redirect, session, url_for
from main import Booking

from main.Authentication.utils import getUserByUsername
from main.Booking.utils import getBookingById
from main.Schedule.utils import getPriceListById, getScheduleById
from main.Seats.utils import getSeatById

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (date, time)):
            return obj.isoformat()
        return super().default(obj)

def genTransactionId():
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
    transactionid = genTransactionId()
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
        for s in seatsPrice:
            if seat.type == s.seat_type:
                # print(s.seat_type)
                totalPrice += s.price
        
                movieInfo.append({'title':schedule.movieref.title, 'duration':schedule.movieref.duration,'date':schedule.start_time.date(), 'time':schedule.start_time.time(), 'seat_id':bookingData.seatid, 'screen':schedule.screenref.name, 'seat_row':seat.row, 'seat_column': seat.column, 'seat_type': seat.type.value, "price":s.price})

                break

        
        # print("\n")

    return {'transactionid':transactionid, 'name':name, 'movieInfo':movieInfo, 'totalPrice': totalPrice, 'email':email}


def emptySeats():
    print("called emprt")
    # session.pop("seats", None)

def freeHolds():
    print("called")
    # for b in session['booking']:
    #     Booking.query.filter_by(id=b.id).delete()