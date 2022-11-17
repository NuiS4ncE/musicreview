from app import app
from flask import render_template, request, redirect
import genres
import users
import songs

@app.route("/")
def index():
    #, genres=genres.get_all_genres()
    print("rendering frontpage")
    return render_template("index.html")

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

@app.route("/genre/<gname>")
def show_genre(gname):
    info = genres.get_genre_info(gname)
    reviews = songs.get_reviews()

@app.route("/login", methods=["get", "post"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if not users.login(username, password):
            return render_template("error.html", message="Wrong username or password")
        print("redirecting to frontpage")
        return redirect("/")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["get", "post"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        if len(username) < 1 or len(username) > 20:
            return render_template("error.html", message="Username has to be 1 to 20 characters long")
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="Passwords are not the same")
        if password1 == "":
            return render_template("error.html", message="No password set")

        if not users.register(username, password1):
            return render_template("error.html", message="Something went wrong! Could not register!")
        return redirect("/")

@app.route("/myinfo")
def show_myinfo():
    myinfo = users.get_user_info(users.user_id())
    return render_template("myinfo.html", data=myinfo)

@app.route("/genres")
def show_genres():
    genredata = genres.get_all_genres()
    return render_template("genres.html", data=genredata)