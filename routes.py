from app import app
from flask import render_template, request, redirect
import genres
import users

@app.route("/")
def index():
    return render_template("index.html", genres=genres.get_all_genres())

@app.route("/add", methods=["get", "post"])
def add_genre():
    if request.method == "GET":
        return render_template("addgenre.html")

    if request.method == "POST":
        users.check_csrf()

        gname = request.form["gname"]
        if len(gname) < 1 or len(gname) > 20:
            return render_template("error.html", message="Genre name should be 1-20 characters long")

        genre_id = genres.add_genre(gname, users.user_id())
        return render_template("/genre/"+str(genre_id))

@app.route("/remove", methods=["get", "post"])
def remove_genre():
    if request.method == "GET":
        my_genres = genres.get_my_genres(users.user_id())
        return render_template("remove.html", list=my_genres)

    if request.method == "POST":
        users.check_csrf()

        if "genre" in request.form:
            genre = request.form["genre"]
            genres.remove_genre(genre, users.user_id())

            return redirect("/")

@app.route("/genre/<str:gname>")
def show_genre(gname):
    info = genres.get_genre_info(gname)
    reviews = genres.get_reviews()