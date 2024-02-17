from flask import Blueprint, redirect, render_template, request,url_for, flash

from main.Authentication.utils import commitDB, deleteFromDB, saveToDB,login_not_required, login_required, superuser_required
from .models import Seats, SeatType

from ..Screen.utils import getAllScreen
from .utils import *

seats = Blueprint("seats", __name__, template_folder="templates")


@seats.route("/", methods=['GET', 'POST'])
@login_required
@superuser_required
def create_seat():
    seatType = [(seat.name, seat.value) for seat in SeatType]
    screens = [(screen.id, screen.name) for screen in getAllScreen()]
    temp = {}
    if request.method == "POST":
        row = request.form.get("row")
        column = request.form.get("column")
        type = request.form.get("type")
        screen = request.form.get("screen")
        
        # may be BUG in easyCheckIfInputEmpty
        if not easyCheckIfInputEmpty(row=row, column=column, type=type, screen=screen):
            if checkIfPositiveInt(row):
                temp['row'] = row
                if checkIfPositiveInt(column):
                    temp['column'] = column
                    temp['type'] = type
                    temp['screen'] = screen

                    if not checkIfSeatExists(row, column, screen):
                        newSeat = Seats(row=row, column=column, type=type, screen=screen)
                        saveToDB(newSeat)
                        storeGapWhereNoSeats(screen)
                        flash("Saved")
                        return redirect(url_for("seats.create_seat"))
                    elif checkIfSeatExistsAndIsGap(row, column, screen, type=type):
                        updateSeatType = getAllSeats(row, column, screen)
                        updateSeatType.type = type
                        commitDB()
                        flash("Saved")
                        return redirect(url_for("seats.create_seat"))
                    else:
                        flash("Seat already exists")
                else:
                    flash("Column must be integer greater than 0")
            else:  
                flash("Row must be integer greater than 0")

    return render_template("create_seat.html", seatType=seatType, screens=screens, temp=temp)


@seats.route("/get-seats/", methods=['POST'])
@login_required
@superuser_required
def get_seats():
    data = request.get_json()
    _screen = data["screen"]
    seats = getJsonSeatMap(_screen)
    return seats


@seats.route("/show-seats/", methods=['GET'])
@login_required
@superuser_required
def show_seats():
    screens = [(screen.id, screen.name) for screen in getAllScreen()]
    return render_template("show_seat.html",screens=screens)

# only type change possible

@seats.route("/edit/", methods=['GET','POST'])
@login_required
@superuser_required
def edit_seats():
    seatType = [(seat.name, seat.value) for seat in SeatType]
    screens = [(screen.id, screen.name) for screen in getAllScreen()]
    temp={}
    if request.method == "POST":
        row = request.form.get("row")
        column = request.form.get("column")
        type = request.form.get("type")
        screen = request.form.get("screen")

        if not easyCheckIfInputEmpty(row=row, column=column, type=type, screen=screen):
            if checkIfPositiveInt(row):
                temp['row'] = row
                if checkIfPositiveInt(column):
                    temp['column'] = column
                    temp['type'] = type
                    temp['screen'] = screen

                    if checkIfSeatExists(row, column, screen):
                        updatedSeat = getAllSeats(row=row, column=column, screen=screen)
                        updatedSeat.type = type
                        commitDB()
                        deleteSeatsWithNoNextRowAndAllGap(screen)
                        flash("Edited")
                        return redirect(url_for("seats.edit_seats"))
                    else:
                        flash("Seat doen't exists")
                else:
                    flash("Column must be integer greater than 0")
            else:  
                flash("Row must be integer greater than 0")


    return render_template("edit_seat.html", seatType=seatType, screens=screens,temp=temp)



@seats.route("/delete", methods=['GET', 'POST'])
@login_required
@superuser_required
def delete_seats():
    screens = [(screen.id, screen.name) for screen in getAllScreen()]
    temp={}
    if request.method == "POST":
        row = request.form.get("row")
        column = request.form.get("column")
        screen = request.form.get("screen")

        if not easyCheckIfInputEmpty(row=row, column=column, screen=screen):
            if checkIfPositiveInt(row):
                temp['row'] = row
                if checkIfPositiveInt(column):
                    temp['column'] = column
                    temp['screen'] = screen

                    if checkIfSeatExists(row, column, screen):
                        deleteSeat = getAllSeats(row=row, column=column, screen=screen)
                        deleteSeat.type = SeatType.GAP
                        commitDB()
                        deleteSeatsWithNoNextRowAndAllGap(screen)
                        flash("Deleted")
                        return redirect(url_for("seats.delete_seats"))
                    else:
                        flash("Seat doen't exists")
                else:
                    flash("Column must be integer greater than 0")
            else:  
                flash("Row must be integer greater than 0")
                
    return render_template("delete_seat.html", screens=screens,temp=temp)