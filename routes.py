from app import app
from flask import render_template, request, redirect, session
import artists
import genres
import users
import songs
import urllib.parse
import requests 
from bs4 import BeautifulSoup

@app.route("/")
def index():
    # , genres=genres.get_all_genres()
    # print("rendering frontpage")
    return render_template("index.html")

@app.route("/addartist", methods=["get", "post"])
def add_artist():
    if request.method == "GET":
        artistlist = artists.get_all_artists()
        # print(str(genrelist))
        return render_template("addsong.html", artistdata=artistlist)

    if request.method == "POST":
        users.check_csrf()

        aname = request.form["aname"]
        
        if len(aname) < 1 or len(aname) > 200:
            return render_template("error.html", message="Song name should be 1-200 characters long")

        print(str(artists.check_if_exists(aname)))
        if(artists.check_if_exists(aname)):
            artist_id = artists.get_id_by_name(aname)
        else:
            artist_id = artists.add_song(users.user_id(), aname)
        # print("Redirecting")

        return redirect("/artist/"+str(artist_id))


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
        # print("genre_url in add genre: " + genre_url)
        genres.add_genre(gname, gdesc, users.user_id(), genre_url)
        # print("Redirecting")

        return redirect("/genre/"+genre_url)


@app.route("/addsong", methods=["get", "post"])
def add_song():
    if request.method == "GET":
        genrelist = genres.get_all_genres()
        # print(str(genrelist))
        return render_template("addsong.html", genredata=genrelist)

    if request.method == "POST":
        users.check_csrf()

        aname = request.form["aname"]
        sname = request.form["sname"]
        hyperlink = request.form["hyperlink"]
        gname = request.form["gname"]
        genre_id = genres.get_genre_info_by_name(gname)[0]

        if len(sname) < 1 or len(sname) > 200:
            return render_template("error.html", message="Song name should be 1-200 characters long")

        sdesc = request.form["sdesc"]
        if len(sdesc) > 10000:
            return render_template("error.html", message="Description too long.")
        # Check for Youtube link and get video id
        # print("Hyperlink " + hyperlink)
        condition = url_check(hyperlink)
        hyperlink = url_parse(hyperlink)
        creator_id = users.user_id()
        print("Artist check truth value: " + str(artists.check_if_exists(aname)[0]))
        #print("Artist id check by name: " + str(artists.get_id_by_name(aname)[0]))
        if(str(artists.check_if_exists(aname)[0]) == 'True'):
            artist_id = artists.get_id_by_name(aname)[0]
        else:
            artist_id = artists.add_artist(creator_id, genre_id, aname)
        if(str(songs.check_if_exists(sname, aname)[0]) == 'True'):
            song_id = songs.get_by_song_artist(sname, aname)[0]
            return redirect("/song/"+str(song_id))
        else:
            song_id = songs.add_song(creator_id, artist_id, genre_id, sname, sdesc, hyperlink, condition)

        return redirect("/song/"+str(song_id))


def url_check(hyperlink):
    query = urllib.parse.urlparse(hyperlink)
    print("query: " + str(query) + " query.hostname: " + str(query.hostname))
    if query.hostname.startswith("youtu.be"):
        return "youtube"
    if query.hostname in ("www.youtube.com", "youtube.com"):
        return "youtube"
    if query.hostname.startswith("soundcloud.com"):
        return "soundcloud"
    return "common"


def url_parse(hyperlink):
    # Taken and edited from:
    # https://stackoverflow.com/questions/4356538/how-can-i-extract-video-id-from-youtubes-link-in-python
    #
    query = urllib.parse.urlparse(hyperlink)
    if query.hostname.startswith("youtu.be"):
        return query.path[1:]
    if query.hostname.startswith("soundcloud.com"):
        return soundcloud_find_stream_url(hyperlink)    
    if query.hostname in ("www.youtube.com", "youtube.com"):
        if query.path.startswith("/watch"):
            p = urllib.parse.parse_qs(query.query)
            return p["v"][0]
        if query.path.startswith("/embed/"):
            return query.path.split('/')[2]
        if query.path[:3].startswith("/v/2"):
            return query.path.split("/")[2]
    return hyperlink

def soundcloud_find_stream_url(hyperlink):
    url = hyperlink
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, "html.parser")
    for link in soup.find_all("meta"):
        #print(link.get('content'))
        if("soundcloud://sounds:" in str(link.get('content'))):
            #print("Found! " + link.get('content').split(":")[2])
            return link.get('content').split(":")[2]

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
    print("genre_url in show_genre: " + genre_url)
    gname = urllib.parse.unquote(genre_url)
    print("genre name urllib.parse.unquote: " + gname)
    info = genres.get_genre_info_by_name(gname)
    # reviews = songs.get_reviews()
    songli = songs.get_by_genre(gname)
    artistli = artists.get_artists_by_genre_id(info[0])
    print(songli)
    print(artistli)
    # print("Info[0] " + str(info[0]) + " and info[1] " + str(info[1]) + " and info[2] " + str(info[2]) + " and info[3] " + str(info[3]))
    return render_template("genre.html", genre_id=info[0], gname=info[1], gdesc=info[2], songlist=songli, artistlist=artistli)


@app.route("/login", methods=["get", "post"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if not users.login(username, password):
            return render_template("error.html", message="Wrong username or password")
        # print("redirecting to frontpage")
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
        if (username == "" or (" " in username)):
            return render_template("error.html", message="Username cannot contain whitespaces")
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
    userinfo = users.get_user_info(users.user_id())
    songinfo = songs.get_by_user_id(users.user_id())
    genreinfo = genres.get_by_user_id(users.user_id())
    print(str(userinfo))
    return render_template("myinfo.html", userdata=userinfo[0], songdata=songinfo, genredata=genreinfo)


@app.route("/genres")
def show_genres():
    genredata = genres.get_all_genres()
    #print("genredata " + str(genredata))
    return render_template("genres.html", genres=genredata)

@app.route("/artists")
def show_artists():
    artistdata = artists.get_all_artists()
    return render_template("artists.html", artists=artistdata)

@app.route("/songs")
def show_songs():
    songdata = songs.get_all_songs()
    #print("songdata " + str(songdata))
    return render_template("songs.html", songs=songdata)

@app.route("/artist/<int:artist_id>")
def show_artist(artist_id):
    artist = artists.get_by_id(artist_id)
    #session['artistname'] = artist[1]
    songli = songs.get_by_artist(artist_id)
    return render_template("artist.html", songli=songli, artist=artist)

@app.route("/song/<int:song_id>")
def show_song(song_id):
    print("song_id: " + str(song_id))
    song = songs.get_by_id(song_id)
    print("song: " + str(song))
    genreinfo = genres.get_genre_info_by_name(song[2])
    print("genreinfo: " + str(genreinfo))
    artist = artists.get_by_id(song[6])
    reviews = songs.get_reviews(song_id)
    return render_template("song.html", song_id=song[0], sname=song[1], 
    gname=song[2], sdesc=song[3], hyperlink=song[4], condition=song[5], 
    aname=artist[1], artist_id=artist[0], genre_id=genreinfo[0], reviews=reviews)

@app.route("/review", methods=["post"])
def review():
    users.check_csrf()

    song_id = request.form["song_id"]
    artist_id = request.form["artist_id"]
    genre_id = request.form["genre_id"]

    stars = int(request.form["stars"])
    if stars < 1 or stars > 5:
        return render_template("error.html", message="Wrong amount of stars")

    comment = request.form["comment"]
    if len(comment) > 1000:
        return render_template("error.html", message="Comment too long")
    if comment == "":
        comment = "-"

    songs.add_review(users.user_id(), song_id, artist_id, genre_id, stars, comment)

    return redirect("/song/"+str(song_id))