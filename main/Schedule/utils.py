from datetime import datetime
from main.Authentication.utils import commitDB

from main.Movie.utils import getMovieById, strDateTimeToPythonDateTime
from main.Screen.utils import getScreenById
from .models import Schedule, ScheduleStatus

def pythonDateTimeToHtml(_datetime):
    # 2024-02-21 18:23:00 to 2024-02-21T14:59
    formatted_obj = _datetime.strftime("%Y-%m-%dT%H:%M")
    return formatted_obj

def checkIfScheduleAlreadyExists(movie, screen, starttime, endtime):
    result =  Schedule.query.filter_by(movie=movie, screen=screen, start_time=starttime, end_time=endtime).first()
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
        schedules = Schedule.query.filter(Schedule.status!=ScheduleStatus.EXPIRED).join(Schedule.movieref).join(Schedule.screenref).order_by(Schedule.start_time).all()
    else:
        schedules = Schedule.query.join(Schedule.movieref).join(Schedule.screenref).order_by(Schedule.start_time).all()            
    return schedules

def getScheduleById(id):
    schedule = Schedule.query.filter_by(id=id).first()            
    return schedule

def hasChanged(val1, val2):
    print(val1,val1)
    if val1 != val2:
        return True
    return False

# find a better way to do this
def manageScheduleStatus():
    print("called")
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
