from .models import Screen

def getScreenById(_id):
    result = Screen.query.filter_by(id=_id).first()
    return result

def getScreenByUniqueName(uniqueName):
    result = Screen.query.filter_by(unique_name=uniqueName).first()
    return result #result or None

def getAllScreen():
    result = Screen.query.all()
    return result #result or []

def isInputEmpty(value):
    if value == "":
        return True
    return False

def isNone(value):
    if value == None:
        return True
    return False

def isArrEmpty(arr):
    if arr == []:
        return True
    return False

def checkIfInt(value):
    try:
        # return isinstance(value, int) and value > 0
        value = int(value)
        if isinstance(value, int):
            return True
        else:
            return False
    except:
        return False

def generateUniqueNameFromName(name):
    return name.replace(" ","").lower()
