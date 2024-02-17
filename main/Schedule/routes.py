from datetime import datetime, timedelta
from flask import Blueprint, jsonify, render_template, request, url_for, redirect,flash
from main.Authentication.utils import commitDB, deleteFromDB, saveToDB, login_required, login_not_required, superuser_required

from main.config import Config
from .models import Schedule
from ..Movie.utils import getMovieById, getMovieList, checkIfInputEmptyVAL,emptyBoilerPlate, strDateTimeToPythonDateTime, strDateToPythonDate
from ..Screen.utils import getAllScreen, isNone
from .utils import *

schedule = Blueprint("schedule", __name__, template_folder="templates")

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
    minTime = pythonDateTimeToHtml(datetime.now())
    temp = {}
    if request.method == "POST":
        movie = request.form.get("movie")
        screen = request.form.get("screen")
        starttime = request.form.get("starttime")
        endtime = request.form.get("endtime")

        if not checkIfInputEmptyVAL(movie):
            temp['movie'] = movie
            if not checkIfInputEmptyVAL(screen):
                temp['screen'] = screen 
                print(temp['screen'])
                if not checkIfInputEmptyVAL(starttime):
                    temp['starttime'] = starttime
                    if not checkIfInputEmptyVAL(endtime):
                        _starttime = strDateTimeToPythonDateTime(starttime)
                        _endtime = strDateTimeToPythonDateTime(endtime)
                        if checkIfScheduleAlreadyExists(movie=movie,screen=screen,starttime=_starttime, endtime=_endtime):
                            flash("Schedule already exists!")
                        else:
                            if checkIfTimeIsOccupied(screen=screen, starttime=_starttime, endtime=_endtime):
                                flash(f"Time Slot is already occupied in screen {screen}")
                            else:
                                temp['endtime'] = endtime
                                newSchedule = Schedule(movie,screen,_starttime,_endtime)
                                saveToDB(newSchedule)
                                flash("Saved")
                                return redirect(url_for("schedule.list_schedules"))
                    else:
                        emptyBoilerPlate("End Time")
                else:
                    emptyBoilerPlate("Start Time")
            else:
                emptyBoilerPlate("Screen")
        else:
            emptyBoilerPlate("Movie")

    return render_template("create_schedule.html", movies=movies, screens=screens, temp=temp, minTime=minTime)

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
    # minTime = pythonDateTimeToHtml(datetime.now())
    starttime = pythonDateTimeToHtml(schedule.start_time)
    endtime = pythonDateTimeToHtml(schedule.end_time)
    temp={}
    if request.method == "POST":
        movie = request.form.get("movie")
        screen = request.form.get("screen")
        starttime = request.form.get("starttime")
        endtime = request.form.get("endtime")
        
        if not checkIfInputEmptyVAL(movie):
            temp['movie'] = movie
            if not checkIfInputEmptyVAL(screen):
                temp['screen'] = screen 
                print(temp['screen'])
                if not checkIfInputEmptyVAL(starttime):
                    temp['starttime'] = starttime
                    if not checkIfInputEmptyVAL(endtime):
                        temp['endtime'] = endtime
                        _starttime = strDateTimeToPythonDateTime(starttime)
                        _endtime = strDateTimeToPythonDateTime(endtime)
                        if checkIfScheduleAlreadyExists(movie=movie,screen=screen,starttime=_starttime, endtime=_endtime):
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
                emptyBoilerPlate("Screen")
        else:
            emptyBoilerPlate("Movie")

    return render_template("edit_schedule.html", movies=movies, screens=screens, starttime=starttime, endtime=endtime,temp={}, schedule=schedule)

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