from flask import Blueprint, redirect, render_template, flash, request, url_for
from .models import Screen

from .utils import *
from ..Authentication.utils import commitDB, deleteFromDB, saveToDB, login_required, login_not_required, superuser_required

screen = Blueprint("screen",__name__,template_folder="templates")

@screen.route("/", methods=['GET','POST'])
@login_required
@superuser_required
def create_screen():
    if request.method == "POST":
        name = request.form.get("name")
        if not isInputEmpty(name):
            uniqueName = name.replace(" ","").lower()
            if getScreenByUniqueName(uniqueName) == None:
                newScreen = Screen(name=name, unique_name=uniqueName)
                saveToDB(newScreen)
            else:
                flash("Name must be unique")
        else:
            flash("Name cannot be empty")
    return render_template("screen/create_screen.html", screens=getAllScreen())

@screen.route("/edit/<int:id>", methods=['GET','POST'])
@login_required
@superuser_required
def edit_screen(id):
    screen = getScreenById(id)
    if not isNone(screen):
        if request.method == "POST":
            name = request.form.get("name")
            unique = generateUniqueNameFromName(name)
            checkScreen = getScreenByUniqueName(unique)
            if isNone(checkScreen):
                screen.name = name
                screen.unique_name = unique
                commitDB()
                return redirect(url_for("screen.create_screen"))
            else:
                flash("Screen with same name already exists")
    else:
        flash("No such screen exists")
        return redirect(url_for("screen.create_screen"))
    return render_template("screen/edit_screen.html", screens=screen)


@screen.route("/delete/<int:id>", methods=['GET','POST'])
@login_required
@superuser_required
def delete_screen(id):
    screen = getScreenById(id)
    if not isNone(screen):
        if request.method == "POST":
                deleteFromDB(screen)
                return redirect(url_for("screen.create_screen"))
    else:
        flash("No such screen exists")
        return redirect(url_for("screen.create_screen"))
    return render_template("screen/delete_screen.html", screens=screen)