from main.Schedule.models import Price, PriceStatus, Schedule, ScheduleStatus
from main.Movie.models import Movie, MovieStatus
from datetime import datetime, date, timedelta
from main.Movie.utils import getImagePath, strDateTimeToPythonDateTime, strDateToPythonDate

def getRunningMovie():
    resp = Movie.query.filter(Movie.release_date <= date.today(), Movie.status == MovieStatus.ACTIVE).all()
    for movie in resp:
        movie.poster_url = getImagePath(movie.poster_url)
    return resp

def getUpcomingMovie():
    resp = Movie.query.filter(Movie.release_date>date.today(), Movie.status == MovieStatus.ACTIVE).all()
    for movie in resp:
        movie.poster_url = getImagePath(movie.poster_url)
    return resp

def isUpcomingMovie(id):
    resp = Movie.query.filter(Movie.id==id, Movie.release_date>date.today(), Movie.status == MovieStatus.ACTIVE).all()
    return False if resp==[] else True

def isUpcomingSchedule(id):
    resp = Schedule.query.join(Schedule.movieref).filter(Schedule.id==id, Movie.release_date>date.today()+timedelta(days=2)).all()
    return False if resp==[] else True

def getMovieSchedule(id):
    resp = Schedule.query.join(Schedule.priceref).filter(Schedule.movie==id, Schedule.start_time>datetime.now()+timedelta(minutes=15), Schedule.status==ScheduleStatus.UPCOMING, Price.status==PriceStatus.ENABLED).order_by(Schedule.start_time).all()

    schedules_by_date = {}
    for schedule in resp:
        # Extract the date part from the start_time
        date = schedule.start_time.date()
        # time = schedule.start_time.time()
        if date not in schedules_by_date:
            schedules_by_date[date] = []
        print((schedule))
        schedules_by_date[date].append(schedule)

    print(schedules_by_date)
    return schedules_by_date
