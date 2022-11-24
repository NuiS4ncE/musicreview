from app import app
from flask import render_template, request, redirect
import genres
import users
import songs
import urllib.parse

@app.route("/")
def index():
    #, genres=genres.get_all_genres()
    print("rendering frontpage")
    return render_template("index.html")

@app.route("/addgenre", methods=["get", "post"])
def add_genre():
    if request.method == "GET":
        return render_template("addgenre.html")

    if request.method == "POST":
        users.check_csrf()

        gname = request.form["gname"]
        
        if len(gname) < 1 or len(gname) > 20:
            return render_template("error.html", message="Genre name should be 1-20 characters long")

        gdesc = request.form["gdesc"]
        if len(gdesc) > 10000:
            return render_template("error.html", message="Description too long.")
        # try - catch?
        check_genre = genres.check_if_gexists(gname)
        if check_genre == "true":
            return render_template("error.html", message="Genre already exists. Name must be unique.")
        genre_url = urllib.parse.quote(gname)
        genres.add_genre(gname, gdesc, users.user_id(), genre_url)        
        print("Redirecting")
        
        return redirect("/genre/"+genre_url)

@app.route("/addsong", methods=["get", "post"])
def add_song():
    if request.method == "GET":
        return render_template("addsong.html")

    if request.method == "POST":
        users.check_csrf()

        sname = request.form["sname"]
        hyperlink = request.form["hyperlink"]
        gname = request.form["gname"]
        genre_id = request.form["genre_id"]
        
        if len(sname) < 1 or len(sname) > 200:
            return render_template("error.html", message="Song name should be 1-200 characters long")

        sdesc = request.form["sdesc"]
        if len(sdesc) > 10000:
            return render_template("error.html", message="Description too long.")
        song_id = songs.add_song(users.user_id(), genre_id, sname, gname, sdesc, hyperlink)        
        print("Redirecting")
        
        return redirect("/song/"+song_id)

def url_parse(list):
    for parses in list:
        asd

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

@app.route("/genre/<genre_url>")
def show_genre(genre_url):
    info = genres.get_genre_info_by_name(genre_url)
    #reviews = songs.get_reviews()
    gname = info[1]
    songli = songs.get_by_genre(gname)
    print("Info[0] " + str(info[0]) + " and info[1] " + str(info[1]) + " and info[2] " + str(info[2]))
    return render_template("genre.html", genre_id=info[0], gname=info[1], gdesc=info[2], songlist=songli)

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