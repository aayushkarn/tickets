import json
from flask import Flask, flash

from main.Authentication.utils import deleteFromDB, saveToDB

from .models import SeatType, Seats
from ..Screen.utils import isInputEmpty, isArrEmpty, isNone

def easyCheckIfInputEmpty(**value):
    # result = []
    for val in value.items():
        out = checkIfInputEmpty(val)
    #     result.append(out)
    # return all(result)

def checkIfInputEmpty(*value):
    for key,val in value:
        if isInputEmpty(val):
            flash(f"{key} cannot be empty!")
            return True
        if isNone(val):
            flash(f"{key} cannot be empty!")
            return True
        if isArrEmpty(val):
            flash(f"{key} cannot be empty!")
            return True
        if isNone(val):
            flash(f"{key} cannot be empty!")
            return True
    return False

# BUGS
def easyCheckIfPositiveInt(**value):
    for val in value.items():
        checkIfPositiveInt(val)
    
def checkIfPositiveInt(value):
    try:
        value = int(value)
        if isinstance(value, int):
            if value > 0 :
                return True
            else:
                return False
        else:
            return False
    except:
        return False

def getSeatById(id):
    seat = Seats.query.filter_by(id=id).first()
    return seat

def checkIfSeatExists(row, column, screen):
    seat = Seats.query.filter_by(row=row, column=column, screen=screen).first()
    # print(seat)
    return True if seat!=None else False

def checkIfSeatExistsAndIsGap(row, column, screen, type):
    seat = Seats.query.filter_by(row=row, column=column, screen=screen, type=SeatType.GAP).first()
    return True if seat!=None else False

def getSeatmap(screen):
    result = Seats.query.filter_by(screen=screen).order_by(Seats.row.asc(), Seats.column.asc()).all()
    return result #result or None

def getAllSeats(row, column, screen):
    result = Seats.query.filter_by(row=row, column=column, screen=screen).first()
    return result #result or None

def getHighestRowCol(screen):
    seats = getSeatmap(screen)
    highestRow = 0 
    highestColumn = 0
    for seat in seats:
        if highestRow<seat.row:
            highestRow = seat.row
        if highestColumn<seat.column:
            highestColumn = seat.column
    # print(highestRow, highestColumn)
    return [highestRow, highestColumn]

def storeGapWhereNoSeats(screen):
    data = getHighestRowCol(screen)
    highestRow = data[0]
    highestColumn = data[1]
    for i in range(1, highestRow+1):
        for j in range(1, highestColumn+1):
            existing = Seats.query.filter_by(row=i, column=j, screen=screen).first()
            if not existing:
                storeSeatGaps = Seats(row=i, column=j, type=SeatType.GAP, screen=screen)
                saveToDB(storeSeatGaps)

def deleteSeatsWithNoNextRowAndAllGap(screen):
    data = getHighestRowCol(screen)
    highestRow = data[0]
    highestColumn = data[1]
    gaps = []
    # deletes all row with all gaps
    # for i in range(highestRow, 0, -1):
    #     non_gap_seats = Seats.query.filter_by(row=i, screen=screen).filter(Seats.type!=SeatType.GAP).first()
    #     if not non_gap_seats:
    #         gaps_in_row = Seats.query.filter_by(row=i, type=SeatType.GAP, screen=screen).all()
    #         for gap_seat in gaps_in_row:
    #             print(f"Deleting {gap_seat}")
    #             deleteFromDB(gap_seat)
    # deletes only the lower seats row which are all of type gap
    non_gap_seats = Seats.query.filter_by(row=highestRow, screen=screen).filter(Seats.type!=SeatType.GAP).first()
    if not non_gap_seats:
        gaps_in_row = Seats.query.filter_by(row=highestRow, type=SeatType.GAP, screen=screen).all()
        for gap_seat in gaps_in_row:
            print(f"Deleting {gap_seat}")
            deleteFromDB(gap_seat)

def getJsonSeatMap(screen):
    seats = getSeatmap(screen)
    result = []
    data = getHighestRowCol(screen)
    extrainfo = {
        "highest_rows":data[0],
        "highest_cols":data[1]
    }
    result.append(extrainfo)
    for seat in seats:
        result.append({
            "id":seat.id,
            "row":seat.row,
            "column":seat.column,
            "type":seat.type.value,
            "screen":seat.screen
        })

    return json.dumps(result, indent=4)