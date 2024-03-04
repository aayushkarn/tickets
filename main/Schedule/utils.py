from datetime import datetime
from main import db
from main.Authentication.utils import commitDB
from main.Movie.models import Movie

from main.Movie.utils import checkIfInputEmptyVAL, getMovieById, strDateTimeToPythonDateTime
from main.Screen.utils import getScreenById
from main.Seats.models import SeatType
from .models import Price, PriceStatus, Schedule, ScheduleStatus

def pythonDateTimeToHtml(_datetime):
    # 2024-02-21 18:23:00 to 2024-02-21T14:59
    formatted_obj = _datetime.strftime("%Y-%m-%dT%H:%M")
    return formatted_obj

def checkIfScheduleAlreadyExists(id, movie, screen, starttime, endtime):
    result =  Schedule.query.filter(Schedule.id!=id,Schedule.movie==movie, Schedule.screen==screen, Schedule.start_time==starttime, Schedule.end_time==endtime).first()
    return True if result!=None else False

def checkIfTimeIsOccupied(screen, starttime, endtime, scheduleid=None):
    if scheduleid:
        results = Schedule.query.filter(Schedule.screen==screen, Schedule.id!=str(scheduleid)).all()
        print("WITH ID")
        print(results)
    else:
        print("WITHOUT ID")
        results = Schedule.query.filter_by(screen=screen).all()
    if results:
        print("inside result")
        for result in results:
            print(result)
            if starttime>=result.start_time and endtime<=result.end_time:
                print("Condition 1")
                return True   
            if starttime<=result.start_time and endtime>=result.start_time and endtime <= result.end_time:
                print("Condition 2")
                return True
            if starttime>=result.start_time and starttime<=result.end_time and endtime>=result.end_time:
                print("Condition 3")
                return True
            if starttime<=result.start_time and endtime>=result.end_time:
                print("Condition 4")
                return True
    return False

def getAllSchedule():
    return Schedule.query.all()

def hasScheduleExpired(end_time):
    pass

def getAllMovieAndScreenInSchedule(expire=None):
    if expire:
        schedules = Schedule.query.join(Schedule.movieref).join(Schedule.screenref).join(Schedule.priceref).filter(Schedule.status!=ScheduleStatus.EXPIRED, Price.status == PriceStatus.ENABLED).order_by(Schedule.start_time).all()
    else:
        schedules = Schedule.query.join(Schedule.movieref).join(Schedule.screenref).order_by(Schedule.start_time).all()            
    return schedules

def getScheduleById(id):
    schedule = Schedule.query.filter_by(id=id).first()            
    return schedule

def hasChanged(val1, val2):
    if val1 != val2:
        return True
    return False

# find a better way to do this
def manageScheduleStatus():
    schedules = getAllSchedule()
    currentDateTime = datetime.now()
    for schedule in schedules:
        if schedule.status != ScheduleStatus.EXPIRED:
            startTime = schedule.start_time
            endTime = schedule.end_time
            if currentDateTime>startTime and currentDateTime<endTime:
                schedule.status = ScheduleStatus.ONGOING
            elif currentDateTime<startTime and currentDateTime<endTime:
                schedule.status = ScheduleStatus.UPCOMING
            else:
                schedule.status = ScheduleStatus.EXPIRED
        

def runEvery5minutes():
    # probably use celery
    manageScheduleStatus()
    commitDB()

def getPriceList():
    return Price.query.all()

def getPriceListOnlyId():
    unique = Price.query.group_by(Price.uniqueid).distinct().all()
    return [(u.uniqueid, u.name, u.status) for u in unique]


def getPriceListById(id):
    return Price.query.filter_by(uniqueid=id).all()

def getUniqueId(onlyid=None):
    if onlyid:
        unique = getPriceListById(onlyid)
        if unique:
            return [unique[0].uniqueid]
        return []
    else:
        unique = Price.query.group_by(Price.uniqueid).distinct().all()
    return [u.uniqueid for u in unique]

# TODO: fix for single id request. Currently using list[0]
def getPriceListWithSameId(onlyid=None):
    if onlyid:
        uniqueidArr = getUniqueId(onlyid)
    else:
        uniqueidArr = getUniqueId()
    result = []
    for uniqueid in uniqueidArr:
        rows = Price.query.filter(Price.uniqueid==uniqueid).all()
        data = {}
        data['uniqueid'] = rows[0].uniqueid
        data['status'] = rows[0].status.value

        for row in rows:
            if "name" not in data:
                data['name'] = row.name
            if row.seat_type == SeatType.CLASSIC:
                data['CLASSIC'] = row.price
            if row.seat_type == SeatType.BUSINESS:
                data['BUSINESS'] = row.price
            if row.seat_type == SeatType.EXCLUSIVE:
                data['EXCLUSIVE'] = row.price
        result.append(data)
    return result

def checkIfPositiveFloat(value):
    try:
        value = float(value)
        if isinstance(value, float):
            if value > 0.0 :
                return True
            else:
                return False
        else:
            return False
    except:
        return False

def checkIfUniqueNameExists(uniqueid):
    return Price.query.filter(Price.uniqueid == uniqueid).all()

def isScheduleBeforeRelease(movie, starttime):
    start_date = strDateTimeToPythonDateTime(starttime).date()
    movie = Movie.query.filter_by(id=movie).first()
    if movie.release_date>start_date:
        return True
    else:
        return False