from main.db import db 
from enum import Enum
from datetime import datetime

class MovieCertificate(Enum):
    U = "U" #everyone
    UA = "UA" #parental guidance under 12
    A = "A" #for adult

# # probably add a different table for actors later
class Movie(db.Model):
    __tablename__ = "movies"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    poster_url = db.Column(db.String(200))
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text())
    trailer_link = db.Column(db.Text())
    duration = db.Column(db.Integer) #in minutes
    certificate = db.Column(db.Enum(MovieCertificate), default="UA")
    release_date = db.Column(db.Date,nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def __init__(self, poster, title, description, traile_link, duration, certificate, release):
        self.poster_url = poster
        self.title = title
        self.description = description
        self.trailer_link = traile_link
        self.duration = duration
        self.certificate = certificate
        self.release_date = release

    def __repr__(self):
        return f"{self.title}-{self.release_date}"
