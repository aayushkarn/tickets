from flask import Blueprint, redirect, render_template, request, url_for, flash
from main.Authentication.utils import commitDB, deleteFromDB, saveToDB, login_required, login_not_required, superuser_required

from main.Screen.utils import isNone

from .models import Movie, MovieCertificate, MovieStatus
from ..Seats.utils import checkIfInputEmpty, easyCheckIfInputEmpty
from .utils import *

movie = Blueprint("movie", __name__, template_folder="templates")

@movie.route("/", methods=['GET', 'POST'])
@login_required
@superuser_required
def create_movie():
    movieCertificate = [(cert.name, cert.value) for cert in MovieCertificate]
    movieStatus = [(stat.name, stat.value) for stat in MovieStatus]
    temp = {}
    if request.method == "POST":
        poster = request.files["poster"]
        title = request.form.get("title")
        description = request.form.get("description")
        trailer = request.form.get("trailer")
        duration = request.form.get("duration")
        certificate = request.form.get("certificate")
        release = request.form.get("release")
        status = request.form.get("status")

        if not easyCheckIfInputEmpty(poster=poster, title=title, trailer=trailer, duration=duration, certificate=certificate, release=release, status=status):
            temp['title'] = title
            temp['description'] = description
            temp['duration'] = duration
            temp['certificate'] = certificate
            temp['release'] = release
            temp['status'] = status

            extension = getImageExt(poster)
            if(extension in getAllowedImgExt()):
                posterURL = upload_img(poster)
                if isNone(posterURL):
                    flash("Error getting file")
                else:
                    newRelease = strDateToPythonDate(release)
                    newMovie = Movie(posterURL, title, description, trailer, duration, certificate, status, newRelease)
                    
                    saveToDB(newMovie)
                    flash("Saved")
                    return redirect(url_for("movie.create_movie"))
            else:
                flash(f"{extension} not allowed. Only {getAllowedImgExt()} allowed!")

    return render_template("create_movie.html",temp=temp,movieCertificate=movieCertificate, movieStatus=movieStatus)

@movie.route("/list/")
@login_required
@superuser_required
def movie_list():
    movies = getMovieList()
    for movie in movies:
        movie.poster_url = getImagePath(movie.poster_url)
    return render_template("movie_list.html", moviesList=movies)

@movie.route("/delete/<int:id>", methods=['GET','POST'])
@login_required
@superuser_required
def delete_movie(id):
    movie =  getMovieById(id)
    # oldImageURL = movie.poster_url
    # print(oldImageURL)
    movie.poster_url = getImagePath(movie.poster_url)
    oldImageURL = movie.poster_url
    if not isNone(movie):
        if request.method == "POST":
            deleteFromDB(movie)
            deleteImage(oldImageURL)
            return redirect(url_for("movie.movie_list"))
    else:
        flash("No Such Movie")
        return redirect(url_for("movie.movie_list"))
    return render_template("delete_movie.html", movie=movie)

@movie.route("/edit/<int:id>", methods=['GET','POST'])
@login_required
@superuser_required
def edit_movie(id):
    movie =  getMovieById(id)
    movieCertificate = [(cert.name, cert.value) for cert in MovieCertificate]
    movieStatus = [(stat.name, stat.value) for stat in MovieStatus]

    if not isNone(movie):
        movieID = movie.id
        if request.method == "POST":
            poster = request.files["poster"]
            title = request.form.get("title")
            description = request.form.get("description")
            trailer = request.form.get("trailer")
            duration = request.form.get("duration")
            certificate = request.form.get("certificate")
            release = request.form.get("release")
            status = request.form.get("status")
            temp = movie
            print(temp.poster_url)
            # not using easyCheckIfInputEmpty because of BUG
            # replace in future 
            if checkIfInputEmptyVAL(title):
                emptyBoilerPlate("title")
            else:
                temp.title = title
                if checkIfInputEmptyVAL(trailer):
                    emptyBoilerPlate("trailer")
                else:
                    temp.trailer_link = trailer
                    if checkIfInputEmptyVAL(duration):
                        emptyBoilerPlate("duration")
                    else:
                        temp.duration = duration
                        if checkIfInputEmptyVAL(certificate):
                            emptyBoilerPlate("certificate")
                        else:
                            temp.certificate = certificate
                            if checkIfInputEmptyVAL(release):
                                emptyBoilerPlate("release")
                            else:
                                temp.release_date =strDateToPythonDate(release)
                                if checkIfInputEmptyVAL(status):
                                    emptyBoilerPlate("status")
                                else:
                                    temp.status = status
                                    oldPosterUrl = None
                                    # update value
                                    if poster.filename == movie.poster_url:
                                        # no change
                                        pass
                                    else:
                                        if not poster.filename == "":
                                            extension = getImageExt(poster)
                                            if(extension in getAllowedImgExt()):
                                                posterURL = upload_img(poster)
                                                oldPosterUrl = temp.poster_url
                                                temp.poster_url = posterURL
                                            else:
                                                flash(f"{extension} not allowed. Must be {getAllowedImgExt()} only!")
            if temp != None:
                commitDB()
                if not isNone(oldPosterUrl):
                    print("deleteing")
                    deleteImage(oldPosterUrl)
                flash("Edited")
            return redirect(url_for("movie.edit_movie", id=movieID))
    else:
        flash("No such movie exists")
        return redirect(url_for("movie.create_movie"))
    movie.poster_url = getImagePath(movie.poster_url)
    return render_template("edit_movie.html", movie=movie, movieCertificate=movieCertificate, movieStatus=movieStatus)