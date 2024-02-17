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
    ALLOWED_IMG_EXT = ["jpeg", "jpg", "png"]
    DELAY_MOVIE_SCHEDULE_ENDTIME_BY_MIN = 15