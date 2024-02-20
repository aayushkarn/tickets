from datetime import datetime, timedelta
from flask import Blueprint, jsonify, render_template, request, url_for, redirect,flash
from main.Authentication.utils import commitDB, deleteFromDB, saveToDB, login_required, login_not_required, superuser_required
from main.Seats.models import SeatType

from main.config import Config
from .models import PriceStatus, Schedule
from ..Movie.utils import getMovieById, getMovieList, checkIfInputEmptyVAL,emptyBoilerPlate, strDateTimeToPythonDateTime, strDateToPythonDate
from ..Screen.utils import generateUniqueNameFromName, getAllScreen, isNone
from .utils import *

schedule = Blueprint("schedule", __name__, template_folder="templates")

# TODO: cant edit if the schedule is expired and ongoing
# TODO: also editing time less than current time is invalid
# TODO: schedule date must be greater than release date

@schedule.route("/")
@login_required
@superuser_required
def list_schedules():
    runEvery5minutes()
    schedulesList = getAllMovieAndScreenInSchedule(expire=1)
    return render_template("list_schedule.html", schedulesList=schedulesList)

@schedule.route("/create/", methods=['GET','POST'])
@login_required
@superuser_required
def create_schedule():
    runEvery5minutes()
    movies = getMovieList()
    screens = getAllScreen()
    prices = getPriceListOnlyId()
    minTime = pythonDateTimeToHtml(datetime.now())
    temp = {}
    if request.method == "POST":
        movie = request.form.get("movie")
        screen = request.form.get("screen")
        price = request.form.get("price")
        starttime = request.form.get("starttime")
        endtime = request.form.get("endtime")

        if not checkIfInputEmptyVAL(movie):
            temp['movie'] = movie
            if not checkIfInputEmptyVAL(screen):
                temp['screen'] = screen 
                if not checkIfInputEmptyVAL(price):
                    temp['price'] = price
                    if not checkIfInputEmptyVAL(starttime):
                        temp['starttime'] = starttime
                        if not checkIfInputEmptyVAL(endtime):
                            _starttime = strDateTimeToPythonDateTime(starttime)
                            _endtime = strDateTimeToPythonDateTime(endtime)
                            # TODO: check if the value already exist
                            if checkIfScheduleAlreadyExists(id=-1,movie=movie,screen=screen,starttime=_starttime, endtime=_endtime):
                                flash("Schedule already exists!")
                            else:
                                if checkIfTimeIsOccupied(screen=screen, starttime=_starttime, endtime=_endtime):
                                    flash(f"Time Slot is already occupied in screen {screen}")
                                else:
                                    temp['endtime'] = endtime
                                    newSchedule = Schedule(movie,screen,price,_starttime,_endtime)
                                    saveToDB(newSchedule)
                                    flash("Saved")
                                    return redirect(url_for("schedule.list_schedules"))
                        else:
                            emptyBoilerPlate("End Time")
                    else:
                        emptyBoilerPlate("Start Time")
                else:
                    emptyBoilerPlate("Price")
            else:
                emptyBoilerPlate("Screen")
        else:
            emptyBoilerPlate("Movie")

    return render_template("create_schedule.html", movies=movies, screens=screens, temp=temp, minTime=minTime, prices=prices)

@schedule.route("/calculate-endtime/", methods=['POST'])
@login_required
@superuser_required
def calculate_endtime():
    data = request.get_json()
    starttime = strDateTimeToPythonDateTime(data['starttime'])
    movieId = int(data['movieId'])
    movie = getMovieById(movieId)
    endtime = starttime + timedelta(minutes=movie.duration+Config.DELAY_MOVIE_SCHEDULE_ENDTIME_BY_MIN)
    print(endtime-starttime)
    return jsonify({'endtime':pythonDateTimeToHtml(endtime)})

@schedule.route("/update/<int:id>", methods=['GET','POST'])
@login_required
@superuser_required
def update_schedule(id):
    runEvery5minutes()
    schedule = getScheduleById(id)
    movies = getMovieList()
    screens = getAllScreen()
    prices = getPriceListOnlyId()
    # minTime = pythonDateTimeToHtml(datetime.now())
    starttime = pythonDateTimeToHtml(schedule.start_time)
    endtime = pythonDateTimeToHtml(schedule.end_time)
    temp={}
    if request.method == "POST":
        movie = request.form.get("movie")
        screen = request.form.get("screen")
        price = request.form.get("price")
        starttime = request.form.get("starttime")
        endtime = request.form.get("endtime")
        
        if not checkIfInputEmptyVAL(movie):
            temp['movie'] = movie
            if not checkIfInputEmptyVAL(screen):
                temp['screen'] = screen 
                if not checkIfInputEmptyVAL(price):
                    temp['price'] = price
                    if not checkIfInputEmptyVAL(starttime):
                        temp['starttime'] = starttime
                        if not checkIfInputEmptyVAL(endtime):
                            temp['endtime'] = endtime
                            _starttime = strDateTimeToPythonDateTime(starttime)
                            _endtime = strDateTimeToPythonDateTime(endtime)
                            if checkIfScheduleAlreadyExists(id=id, movie=movie,screen=screen,starttime=_starttime, endtime=_endtime):
                                flash("Schedule already exists!")
                            else:
                                    if checkIfTimeIsOccupied(screen=screen, starttime=_starttime, endtime=_endtime, scheduleid=schedule.id):
                                        flash(f"Time Slot is already occupied in screen {screen}")
                                    else:
                                        if hasChanged(movie, schedule.movie):
                                            print("movie name")
                                            schedule.movie = movie
                                        if hasChanged(screen, schedule.screen):
                                            print("screen name")
                                            schedule.screen = screen
                                        if hasChanged(price, schedule.price):
                                            print("price ")
                                            schedule.price = price
                                        if hasChanged(starttime, schedule.start_time):
                                            print("start time")
                                            schedule.start_time = strDateTimeToPythonDateTime(starttime)
                                        if hasChanged(endtime, schedule.end_time):
                                            print("end time")
                                            schedule.end_time = strDateTimeToPythonDateTime(endtime)
                                        commitDB()
                                        flash("Edited")
                                        return redirect(url_for("schedule.list_schedules"))
                        else:
                            emptyBoilerPlate("End Time")
                    else:
                        emptyBoilerPlate("Start Time")
                else:
                    emptyBoilerPlate("Price")
            else:
                emptyBoilerPlate("Screen")
        else:
            emptyBoilerPlate("Movie")

    return render_template("edit_schedule.html", movies=movies, screens=screens, starttime=starttime, endtime=endtime,temp={}, schedule=schedule, prices=prices)

@schedule.route("/delete/<int:id>", methods=['GET', 'POST'])
@login_required
@superuser_required
def delete_schedule(id):
    runEvery5minutes()
    schedule = getScheduleById(id=id)
    if not isNone(schedule):
        if request.method == "POST":
            deleteFromDB(schedule)
            return redirect(url_for("schedule.list_schedules"))
    else:
        flash("No such schedule exists!")
        return redirect(url_for("schedule.list_schedules"))

    return render_template("delete_schedule.html", schedule=schedule)


@schedule.route("/price/")
@login_required
@superuser_required
def list_price():
    prices = getPriceListWithSameId()
    return render_template("prices/list_price.html", prices=prices)

@schedule.route("/price/create", methods=['GET', 'POST'])
@login_required
@superuser_required
def create_price():
    seatType = [(seat.name, seat.value) for seat in SeatType]
    priceStatus = [(price.name, price.value) for price in PriceStatus]
    if request.method == "POST":
        name = request.form.get("name")
        price_CLASSIC = request.form.get("price_CLASSIC")
        price_EXCLUSIVE = request.form.get("price_EXCLUSIVE")
        price_BUSINESS = request.form.get("price_BUSINESS")
        status = request.form.get("status")

        if checkIfInputEmptyVAL(name):
            emptyBoilerPlate("Name")
        else:
            if checkIfInputEmptyVAL(price_CLASSIC):
                emptyBoilerPlate("Classic price")
            else:
                if checkIfInputEmptyVAL(price_EXCLUSIVE):
                    emptyBoilerPlate("Executive price")
                else:
                    if checkIfInputEmptyVAL(price_BUSINESS):
                        emptyBoilerPlate("Business price")
                    else:
                        if checkIfInputEmptyVAL(status):
                            emptyBoilerPlate("Status")
                        else:
                            if not checkIfPositiveFloat(price_CLASSIC):
                                flash("Price must be greater than 0")
                                if not checkIfPositiveFloat(price_BUSINESS):
                                    flash("Price must be greater than 0")
                                    if not checkIfPositiveFloat(price_EXCLUSIVE):
                                        flash("Price must be greater than 0")
                                return redirect(url_for("schedule.create_price"))
                            else:
                                # TODO: check if invalid status is provided
                                uniqueid = generateUniqueNameFromName(name)
                                if checkIfInputEmptyVAL(checkIfUniqueNameExists(uniqueid)):
                                    name=name.upper()
                                    for key, value in seatType:
                                        if key != "GAP":
                                            price = locals()["price_{}".format(value)]
                                            newPrice = Price(name=name, uniqueid=uniqueid, status=status, seat_type=value, price=price)
                                            saveToDB(newPrice)
                                    flash("Saved")
                                    return redirect(url_for("schedule.list_price"))
                                else:
                                    flash("Name already exists. Use a new name!")
                                pass
                                
                            
        return redirect(url_for("schedule.create_price"))

    return render_template("prices/create_price.html", priceStatus=priceStatus, seatType=seatType)


#TODO: Disabled currently make it later
@schedule.route("/price/edit/<string:id>", methods=['GET',"POST"])
@login_required
@superuser_required
def edit_price(id):
    price = getPriceListWithSameId(id)[0] #since arr=[{}]
    # price = getPriceListById(id)
    seatType = [(seat.name, seat.value) for seat in SeatType]
    priceStatus = [(p.name, p.value) for p in PriceStatus]
    currentUniqueName = price['uniqueid']

    if not checkIfInputEmptyVAL(price):
        if request.method == "POST":
            name = request.form.get("name")
            price_CLASSIC = request.form.get("price_CLASSIC")
            price_EXCLUSIVE = request.form.get("price_EXCLUSIVE")
            price_BUSINESS = request.form.get("price_BUSINESS")
            status = request.form.get("status")
            if checkIfInputEmptyVAL(name):
                emptyBoilerPlate("Name")
            else:
                if checkIfInputEmptyVAL(price_CLASSIC):
                    emptyBoilerPlate("Classic price")
                else:
                    if checkIfInputEmptyVAL(price_EXCLUSIVE):
                        emptyBoilerPlate("Executive price")
                    else:
                        if checkIfInputEmptyVAL(price_BUSINESS):
                            emptyBoilerPlate("Business price")
                        else:
                            if checkIfInputEmptyVAL(status):
                                emptyBoilerPlate("Status")
                            else:
                                if not checkIfPositiveFloat(price_CLASSIC):
                                    flash("Price must be greater than 0")
                                    if not checkIfPositiveFloat(price_BUSINESS):
                                        flash("Price must be greater than 0")
                                        if not checkIfPositiveFloat(price_EXCLUSIVE):
                                            flash("Price must be greater than 0")
                                    return redirect(url_for("schedule.create_price"))
                                else:
                                    if not hasChanged(price['name'], name):
                                        print("Name not changed")
                                        tempEdit = getPriceListById(id)
                                        for data in tempEdit:
                                            for key, value in seatType:
                                                currentSeatType = "SeatType.{}".format(key)
                                                if currentSeatType != SeatType.GAP:
                                                    if currentSeatType == str(data.seat_type):
                                                        price = locals()["price_{}".format(value)]
                                                        data.seat_type = value
                                                        data.price = price
                                                data.status = status
                                                commitDB()
                                    else:
                                        uniqueid = generateUniqueNameFromName(name)
                                        uniqueidChecker = checkIfUniqueNameExists(uniqueid)
                                        
                                        if not checkIfInputEmptyVAL(uniqueidChecker):
                                            flash("Name you are trying to use is already assigned!")
                                        else:
                                            tempEdit = getPriceListById(id)
                                            print(tempEdit)
                                            name=name.upper()
                                            for data in tempEdit:
                                                data.name = name
                                                data.uniqueid = uniqueid
                                                for key, value in seatType:
                                                    currentSeatType = "SeatType.{}".format(key)
                                                    if currentSeatType != SeatType.GAP:
                                                        if currentSeatType == str(data.seat_type):
                                                            price = locals()["price_{}".format(value)]
                                                            data.seat_type = value
                                                            data.price = price
                                                    data.status = status
                                                    commitDB()
            # return redirect(url_for("schedule.edit_price",id=id))
            return redirect(url_for("schedule.list_price"))
    else:
        flash("No such data found")
        return redirect(url_for("schedule.list_price"))
    return render_template("prices/edit_price.html", price=price, seatType=seatType, priceStatus=priceStatus)

@schedule.route("/price/delete/<string:id>", methods=['GET',"POST"])
@login_required
@superuser_required
def delete_price(id):
    price = getPriceListWithSameId(id)[0]
    if request.method == "POST":
        price = getPriceListById(id)
        for p in price:
            deleteFromDB(p)
            print(p)
        return redirect(url_for("schedule.list_price"))
    return render_template("prices/delete_price.html", price=price)