from flask import Flask 
from .config import Config
from .db import *
# from flask_wtf.csrf import CSRFProtect

from .Authentication.routes import authentication
from .Screen.routes import screen
from .Seats.routes import seats
from .Movie.routes import movie
from .Schedule.routes import schedule
from .Booking.routes import booking
from .Home.routes import home
from .Payment.routes import payment
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    # csrf = CSRFProtect(app)
    # csrf.init_app(app)
    
    app.static_folder = app.config.get("STATIC_FOLDER_PATH")

    # check and create img upload dir if not existing
    if not os.path.exists(app.config['IMG_UPLOAD_PATH']):
        os.makedirs(app.config['IMG_UPLOAD_PATH'])

    init_db(app)

    app.register_blueprint(authentication, url_prefix="/auth/")
    # app.register_blueprint(movieHall, url_prefix="/movie-hall/")
    app.register_blueprint(screen, url_prefix="/screen/")
    app.register_blueprint(seats, url_prefix="/seat/")
    app.register_blueprint(movie, url_prefix="/movie/")
    app.register_blueprint(schedule, url_prefix="/schedule/")
    app.register_blueprint(booking, url_prefix="/booking/")
    app.register_blueprint(payment, url_prefix="/payment/")
    app.register_blueprint(home, url_prefix="/")

    return app
