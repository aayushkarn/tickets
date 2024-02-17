import re
from .models import User

def checkName(name):
    if name != "":
        return True
    return False

def checkEmail(email):
    if email == "":
        return False
    else:
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if(re.fullmatch(regex, email)):
            return True
        return False

def checkEmailExist(email):
    email = User.query.filter_by(email=email)
    if email.first() != None:
        return True 
    return False

def checkPasswordEmpty(password):
    if password != "":
        return True
    return False

def checkPassword(password):
    if len(password)>=8:
        return True
    return False

def checkUsername(username):
    if username != "":
        return True
    return False

def checkUsernameExist(username):
    username = User.query.filter_by(username=username)
    if username.first() != None:
        return True
    return False
