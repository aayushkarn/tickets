import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DEBUG = True
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite3"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # TODO ADD MAX FILESIZE
    STATIC_FOLDER_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../static/'))
    IMG_UPLOAD_PATH = "/uploads/img/"
    TICKET_UPLOAD_PATH = "/tickets/img/"
    PDF_OUTPUT_PATH = "/tickets/pdf/"
    SEAT_SELECTION_LIMIT = 2 #TODO: make it dynamic 
    ALLOWED_IMG_EXT = ["jpeg", "jpg", "png"]
    DELAY_MOVIE_SCHEDULE_ENDTIME_BY_MIN = 15
    MAX_SEAT_HOLD_DURATION_IN_MIN = 10
    KHALTI_BASE_URL = "https://a.khalti.com/api/v2/"
    KHALTI_PUBLIC_KEY = os.getenv("KHALTI_LIVE_PUBLIC_KEY")
    KHALTI_SECRET_KEY = os.getenv("KHALTI_LIVE_SECRET_KEY")