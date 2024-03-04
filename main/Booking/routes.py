from datetime import datetime, timedelta
import json
import time
from flask import Blueprint, flash, render_template, redirect, request, session, url_for
from main.Authentication.models import User
from main.Authentication.utils import getUserByUsername, login_required, saveToDB
from main.Booking.utils import isBooked
from main.Movie.utils import checkIfInputEmptyVAL, emptyBoilerPlate 
from main.Schedule.utils import getAllMovieAndScreenInSchedule, getScheduleById
from main.Screen.utils import getScreenById
from main.Seats.utils import getSeatById
from .models import Booking, BookingStatus

booking = Blueprint("booking", __name__, template_folder="templates")

@booking.route("/", methods=['GET','POST'])
def create_booking():
    users = User.query.all()
    schedules = getAllMovieAndScreenInSchedule(expire=1)

    newSchedule = []
    for schedule in schedules:
        if not schedule.start_time>datetime.now()+timedelta(minutes=15):
            print(f"Removed {schedule}")
        else:
            newSchedule.append(schedule)
    bookingStatus = [(s.name, s.value) for s in BookingStatus]

    if request.method == "POST":
        userid = request.form.get("user")
        scheduleid = request.form.get("schedule")
        screenid = request.form.get("screenid")
        seatid = request.form.get("seat")
        status = request.form.get("status")

        # temp = {}
        if checkIfInputEmptyVAL(userid):
            emptyBoilerPlate("User ")
        else:
            # temp['userid'] = userid
            if checkIfInputEmptyVAL(scheduleid):
                emptyBoilerPlate("Schedule ")
            else:
                # temp['scheduleid'] = scheduleid
                if checkIfInputEmptyVAL(seatid):
                    emptyBoilerPlate("Seat ")
                else:
                    # temp['seatid'] = seatid
                    if checkIfInputEmptyVAL(status):
                        emptyBoilerPlate("Status ")
                    else:
                        # temp['status'] = status
                        if checkIfInputEmptyVAL(screenid):
                            emptyBoilerPlate("Screen ")
                        else:
                            if isBooked(scheduleid, seatid):
                                flash("Already booked. Use another seat or schedule")
                            else:
                                newBooking = Booking(userid, seatid, scheduleid, status)
                                saveToDB(newBooking)
                                flash("Saved")

    return render_template("create_booking.html", users=users, schedules=newSchedule, bookingStatus=bookingStatus, temp={})

@booking.route("/get-screen/", methods=['POST'])
def get_screen():
    resp = request.get_json()
    scheduleId = resp["scheduleid"]
    schedule = getScheduleById(scheduleId)
    if schedule == []:
        return json.dumps({"none"})
    screen = schedule.screenref
    return json.dumps({"name":screen.name, "id":screen.id}, indent=4)

@booking.route("/jsonbook", methods=['POST'])
@login_required
# TODO: hold seats for 10min max
def json_book():
    resp = request.get_json()
    userid = getUserByUsername(session['user']).id
    booking = Booking.query.filter(Booking.userid==userid, Booking.scheduleid==resp['scheduleid'], Booking.status == BookingStatus.HOLD).all()
    if resp['seats'] == [] and booking == []:
        return {"success":False,"msg":"No seats selected"}
    for seat in resp['seats']:
        if isBooked(resp['scheduleid'], seat):
            return {"success":False,"msg":"Someone has already hold seat. Please try another one"}
        if getScheduleById(resp['scheduleid']) is None:
            return {"success":False,"msg":"No such schedule exists"}
        if getSeatById(seat)is None:
            return {"success":False,"msg":"No such seat exists"}

        newBooking = Booking(userid, seat, resp['scheduleid'], BookingStatus.HOLD)
        saveToDB(newBooking)
    newBookId = Booking.query.filter(Booking.userid==userid, Booking.scheduleid==resp['scheduleid'], Booking.status == BookingStatus.HOLD).all()
    booking_ids = [booking.id for booking in newBookId]
    session.pop('booking', None)
    session['booking'] = booking_ids
    return {"success":True, "msg":resp}