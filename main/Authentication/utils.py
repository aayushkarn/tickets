from .models import User
import hashlib
from main.db import db
from flask import flash, session, redirect, url_for

from functools  import wraps

salt = b'cd62a18e82c040db8faff500eabaf29e'

def hashPassword(password):
    newPass = password.encode('utf-8')+salt
    hashedPass = hashlib.sha256(newPass).hexdigest()
    return hashedPass

def verifyPassword(password, userPass):
    newPass = hashPassword(password)
    if newPass == userPass:
        return True
    return False

def commitDB():
    db.session.commit()

def saveToDB(data):
    db.session.add(data)
    commitDB()

def deleteFromDB(data):
    db.session.delete(data)
    commitDB()

def addToSession(username):
    session['user'] = username

def getUserByEmail(email):
    user = User.query.filter_by(email=email)
    return user.first()

def getUserByUsername(username):
    user = User.query.filter_by(username=username)
    return user.first()

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user' not in session or session['user'] == "":
            return redirect(url_for('authentication.login'))
        return func(*args, **kwargs)
    return wrapper

def login_not_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user' in session:
            return redirect(url_for('authentication.profile')) 
        return func(*args, **kwargs)
    return wrapper

def superuser_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user = getUserByUsername(session['user'])
        if not user.is_superuser:
            flash("Unauthorized access!")
            return redirect(url_for('authentication.login'))
        return func(*args, **kwargs)
    return wrapper