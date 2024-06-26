import json
from flask import Blueprint, redirect, session, url_for, render_template
from main.Authentication.utils import login_required
from main.Booking.utils import cleanLongHoldSeats, getSeats
from main.Movie.models import MovieStatus

from main.Movie.utils import checkIfInputEmptyVAL, getImagePath, getMovieById
from main.Payment.utils import deletePaymentWithNullBookingId
from main.config import Config
from .utils import *

home = Blueprint("home",__name__,template_folder="templates", static_folder="static",static_url_path='/Home/static')

@home.route("/")
def index():
    # session.popitem()
    currentMovies = getRunningMovie()
    for movie in currentMovies:
        movie.banner_url = getImagePath(movie.banner_url)
    upcomingMovies = getUpcomingMovie()

    return render_template("index.html", currentMovies=currentMovies, upcomingMovies=upcomingMovies)

@home.route("/<int:id>")
def movie(id):
    movie = getMovieById(id)
    movieSchedule = getMovieSchedule(id)
    # print(movieSchedule)
    if checkIfInputEmptyVAL(movie) or movie.status==MovieStatus.EXPIRED or isUpcomingMovie(id):
        return redirect(url_for("home.index"))
    movie.poster_url = getImagePath(movie.poster_url)
    movie.banner_url = getImagePath(movie.banner_url)
    return render_template("movie.html", movie=movie, movieSchedule=movieSchedule)

@home.route("/movieSeat/<int:id>")
@login_required
def movieSeat(id):
    cleanLongHoldSeats()
    deletePaymentWithNullBookingId()
    seats = getSeats(id)
    print(seats)
    if checkIfInputEmptyVAL(seats) or isUpcomingSchedule(id):
        return redirect(url_for("home.index"))
    highestRow = seats[0]['highest_rows']
    highestColumn = seats[0]['highest_cols']
    seatPrice = seats[0]['seatprice']
    seats = seats[1:]
    movieId = Schedule.query.filter_by(id=id).first()
    movie = {}
    movie["title"]=movieId.movieref.title
    movie["duration"]=movieId.movieref.duration
    movie["date"]= movieId.start_time.date()
    movie["time"]= movieId.start_time.time()
    movie["screen"]= movieId.screenref.name
    selectionLimit = Config.SEAT_SELECTION_LIMIT 


    return render_template("seat.html", seats=seats, highestColumn=highestColumn, highestRow=highestRow, seatPrice=seatPrice, movie=movie, selectionLimit=selectionLimit, scheduleid=id)

