import os
from flask import flash, redirect, url_for
from werkzeug.utils import secure_filename
import uuid
from main.Screen.utils import isArrEmpty, isInputEmpty, isNone
from main.config import Config
from datetime import datetime

from .models import Movie

def upload_img(file):
    filename = secure_filename(file.filename)
    ext = filename.split(".")[-1]
    newFilename = uuid.uuid4().hex+filename
    if ext not in Config.ALLOWED_IMG_EXT:
        return None
    print(f"Saving Image at {Config.STATIC_FOLDER_PATH+Config.IMG_UPLOAD_PATH+newFilename}")
    file.save(Config.STATIC_FOLDER_PATH+Config.IMG_UPLOAD_PATH+newFilename)
    return newFilename

def getAllowedImgExt():
    return Config.ALLOWED_IMG_EXT

def getImageExt(file):
    filename = secure_filename(file.filename)
    ext = filename.split(".")[-1]
    return ext

def strDateTimeToPythonDateTime(_dateTime):
    return datetime.strptime(_dateTime, '%Y-%m-%dT%H:%M')

def strDateToPythonDate(date):
    return datetime.date(datetime.strptime(date, '%Y-%m-%d'))

def getMovieList():
    return Movie.query.all()

def getMovieById(id):
    return Movie.query.filter_by(id=id).first()

def getImagePath(filename):
    return Config.IMG_UPLOAD_PATH+filename

def emptyBoilerPlate(name):
    flash(f"{name} cannot be empty!")

def deleteImage(filename):
    try:
        os.remove(Config.STATIC_FOLDER_PATH+filename)
    except:
        pass

# responseValue = {}
# def setResponseValue(tag, value):
#     responseValue[tag] = checkIfInputEmptyVAL(value)
#     print(f"{value=} Added to {tag}")

# def getResponseValue(tag):
#     print(responseValue[tag])
#     responseValue.pop(tag)
#     # result = []
#     # result = responseValue
#     # responseValue = []
#     # return all(result)

def checkIfInputEmptyVAL(value):
    if isInputEmpty(value):
        return True
    if isNone(value):
        return True
    if isArrEmpty(value):
        return True
    return False