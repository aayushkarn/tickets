import json
from main.Movie.utils import checkIfInputEmptyVAL
from main.Schedule.utils import getPriceListWithSameId
from main.Seats.models import Seats
from .models import Booking, BookingStatus
from main.Schedule.models import PriceStatus, Schedule

from main.Seats.utils import getJsonSeatMap

def isBooked(scheduleid, seatid):
    # schedule = Schedule.query.filter_by(id=scheduleid).first()
    # screen = schedule.screen
    # seat = Seats.query.filter_by(id=seatid)
    booking = Booking.query.filter(Booking.scheduleid==scheduleid, Booking.seatid==seatid).first()
    return False if booking == None else True

def getBookingList(scheduleid):
    booking = Booking.query.filter(Booking.scheduleid==scheduleid).all()
    return booking

def getSeats(scheduleid):
    schedule = Schedule.query.filter_by(id=scheduleid).first()
    if checkIfInputEmptyVAL(schedule):
        return None
    seats = json.loads(getJsonSeatMap(schedule.screen))
    priceid = schedule.price
    prices = getPriceListWithSameId(priceid)
    booking = getBookingList(scheduleid)
    # print(prices)
    if prices[0]['status'] == PriceStatus.DISABLED.value:
        return []
    seatPrice = []
    for price in prices:
        data = {
            "CLASSIC":price['CLASSIC'],
            "BUSINESS":price['BUSINESS'],
            "EXCLUSIVE":price['EXCLUSIVE']
        }
        seatPrice.append(data)
    seats[0]['seatprice'] = seatPrice
    for seat in seats[1:]:
        if seat['type'] != "GAP":
            seat['status'] = BookingStatus.UNRESERVED.value

    if booking is not []:
        for b in booking:
            for seat in seats[1:]:
                if seat['type'] != "GAP":
                    if b.seatid == seat['id']:
                        seat['status'] = b.status.value
                        break
            

    for seat in seats[1:]:
        seat.pop('screen')
    # return json.dumps(seats, indent=4)
    return seats

def getBookingById(id):
    booking = Booking.query.filter_by(id=id).first()
    return booking