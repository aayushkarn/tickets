from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from .models import User
from .validator import *
from .utils import *

authentication = Blueprint('authentication', __name__, template_folder="templates")

@authentication.route("/", methods=['GET', 'POST'])
@login_not_required
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        if(checkEmail(email)):
            if(checkPasswordEmpty(password)):
                if(checkEmailExist(email)):
                    user = getUserByEmail(email)
                    if user == None:
                        flash("No such user exists")
                    passVerify = verifyPassword(password, user.password)
                    if passVerify:
                        addToSession(user.username)
                        return redirect(url_for("authentication.home"))
                    else:
                        flash("Wrong password")
                else:
                    flash("Email does not exist!")
            else:
                flash("Password cannot be empty!")
                
        else:
            flash("Invalid Email")
        return render_template("login.html", values={'email':email})

    return render_template("login.html", values={})

@authentication.route("/register/", methods=['GET','POST'])
@login_not_required
def create_user():
    # TODO: find alternative to is_superuser
    if request.method=="POST":
        name = request.form.get("name")
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")

        values = {'name':name,'email':email,'username':username}

        if checkName(name):
            if checkEmail(email):
                if not checkEmailExist(email):
                    if checkUsername(username):
                        if not checkUsernameExist(username):
                            if checkPassword(password):
                                securePass = hashPassword(password)
                                newUser = User(name=name, email=email, username=username, password=securePass)
                                saveToDB(newUser)
                                flash("Registered Successfully")
                                addToSession(username)
                                return redirect(url_for('authentication.home'))
                            else:
                                flash("Password must be of atleast 8 character!")
                        else:
                            flash(f"Username {username} already exist.")
                    else:
                        flash("Username Cannot be empty!")
                else:
                    flash(f"Email {email} already exist.")
            else:
                flash("Email doesn't match format")
        else:
            flash("Name cannot be empty")
        return render_template("register.html", values=values)
    
    return render_template("register.html", values={})
    
@authentication.route("/profile/")
@login_required
def profile():
    user = getUserByUsername(session['user'])
    if user == None:
        return redirect(url_for('authentication.logout'))
    if user.is_superuser:
        return  render_template("admin/admin_profile.html", user=user)
    return render_template("profile.html", user=user)

@authentication.route("/home/")
@login_required
def home():
    user = getUserByUsername(session['user'])
    if user == None:
        return redirect(url_for('authentication.logout'))
    if user.is_superuser:
        return render_template("admin/admin_home.html", user=user)
    return render_template("profile.html", user=user)

@authentication.route("/logout/")
@login_required
def logout():
    session.pop('user', None)
    session.pop('_flashes', None)
    return redirect(url_for('home.index'))

@authentication.route("/delete", methods=['GET','POST'])
@login_required
def delete():
    user = getUserByUsername(session['user'])
    if user == None:
        return redirect(url_for('authentication.logout'))
    if user.is_superuser:
        return render_template("admin/admin_delete.html", user=user)
    if request.method == "POST":
        password = request.form.get("password")
        if verifyPassword(password, user.password):
            deleteFromDB(user)
            return redirect(url_for("authentication.logout"))
        else:
            flash("Wrong Password!")
    return render_template("delete.html", user=user)
    
@authentication.route("/update/", methods=['GET', "POST"])
@login_required
def update():
    # TODO: solve critical region problem of same username or email as well
    user = getUserByUsername(session['user'])
    if user == None:
        return redirect(url_for('authenticaion.logout'))
    if user.is_superuser:
        return render_template("admin/admin_update.html", user=user)
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        
        temp = user
        # for name
        if not checkName(name):
            flash("Name cannot be empty")
        else:
            temp.name = name
        # for email
        if not checkEmail(email):
            flash("Invalid Email Address")
        else:
            if email ==  user.email:
                pass 
            else:
                if checkEmailExist(email):
                    flash("Email already exists")
                else:
                    temp.email = email
        # for username
        if not checkUsername(username):
            flash("Username cannot be empty")
        else:
            if username == user.username:
                pass
            else:
                if checkUsernameExist(username):
                    flash("Username already exists")
                else:
                    temp.username = username.lower()
        # check password
        if not checkPasswordEmpty(password):
            flash("Password empty")
        else:
            if not verifyPassword(password, user.password):
                flash("Password Incorrect")
            else:
                user=temp
                commitDB()
                session.pop('user', None)
                addToSession(user.username)
        return render_template("update.html", user=temp)

    return render_template("update.html", user=user)

@authentication.route("/change_password/", methods=['GET', 'POST'])
@login_required
def change_password():
    user = getUserByUsername(session['user'])
    if user == None:
        return redirect(url_for("authentication.logout"))
    if user.is_superuser:
        return render_template("admin/admin_change_password.html", user=user)
    if request.method == "POST":
        password = request.form.get("password")
        newPassword = request.form.get("newPassword")
        confirmPassword = request.form.get("confirmPassword")


        if not checkPasswordEmpty(password):
            flash("Password empty")
        else:
            if not checkPasswordEmpty(newPassword) or not checkPasswordEmpty(confirmPassword):
                flash("New Password and Confirm password cannot be empty!")
            else:
                if not checkPassword(newPassword):
                    flash("Password must be atleast 8 characters")
                else:
                    if not verifyPassword(password, user.password):
                        flash("Password Incorrect")
                    else:
                        if password != newPassword:
                            user.password = hashPassword(newPassword)
                            commitDB()
                            flash("Password changed!")
                            return redirect(url_for("authentication.home"))
                        else:
                            flash("Old Password and New Password cannot be same!")
    return  render_template("change_password.html", user=user)
                    

# TODO: Add Forgot password also
