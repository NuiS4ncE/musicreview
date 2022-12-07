from db import db


def get_song_info(song_id):
    sql = """SELECT s.sname, u.username FROM songs s, users u
    WHERE s.id=:song_id AND u.creator_id=u.id"""
    return db.session.execute(sql, {"song_id": song_id}).fetchone()

def get_reviews(song_id):
    sql = """SELECT u.username, r.stars, r.comment FROM reviews r, users u 
    WHERE r.creator_id=u.id AND r.song_id=:song_id ORDER BY r.id"""
    return db.session.execute(sql, {"song_id": song_id}).fetchall()

def get_by_genre(gname):
    sql = """SELECT s.id, s.sname, s.sdesc FROM songs s, genres g 
    WHERE g.gname=:gname ORDER BY s.sname"""
    return db.session.execute(sql, {"gname": gname}).fetchall()

def add_song(creator_id, artist_id, genre_id, sname, sdesc, hyperlink, condition):
    sql = """INSERT INTO songs (creator_id, artist_id, genre_id, sname, sdesc, hyperlink, condition)
            VALUES (:creator_id, :artist_id, :genre_id, :sname, :sdesc, :hyperlink, :condition) RETURNING id"""
    song_id = db.session.execute(sql, {"creator_id":creator_id,
    "artist_id":artist_id, "genre_id":genre_id, "sname":sname, "sdesc":sdesc, 
    "hyperlink":hyperlink, "condition":condition}).fetchone()[0]
    db.session.commit()
    sql = """INSERT INTO songsgenres (genre_id, song_id) VALUES (:genre_id, :song_id)"""
    db.session.execute(sql, {"genre_id":genre_id, "song_id":song_id})
    db.session.commit()
    return song_id

def get_all_songs():
    sql = """SELECT s.id, s.sname, g.gname FROM songs s, genres g, songsgenres sg 
    WHERE s.id = sg.song_id AND g.id = sg.genre_id"""
    return db.session.execute(sql).fetchall()

def get_by_id(song_id):
    print("song_id in get_by_id: " + str(song_id))
    sql = """SELECT s.id, s.sname, g.gname, s.sdesc, s.hyperlink, s.condition, s.artist_id 
    FROM songs s, genres g, songsgenres sg
    WHERE s.id=:song_id AND sg.song_id =:song_id"""
    return db.session.execute(sql, {"song_id":song_id}).fetchone()

def get_by_artist(artist_id):
    sql= """SELECT s.id, s.sname, g.gname 
    FROM songs s, genres g, songsgenres sg
    WHERE s.artist_id=:artist_id AND sg.genre_id=g.id AND sg.song_id=s.id"""
    return db.session.execute(sql, {"artist_id":artist_id}).fetchall()

def add_review(creator_id, song_id, artist_id, genre_id, stars, comment):
    sql = """INSERT INTO reviews (creator_id, song_id, artist_id, genre_id, stars, comment)
    VALUES (:creator_id, :song_id, :artist_id, :genre_id, :stars, :comment)"""
    db.session.execute(sql, {"creator_id":creator_id, "song_id":song_id, "artist_id":artist_id, "genre_id":genre_id, "stars":stars, "comment":comment})
    db.session.commit()

def get_by_user_id(user_id):
    sql = """SELECT s.id AS song_id, s.sname, a.id AS artist_id, a.aname 
    FROM artists a, songs s 
    WHERE a.creator_id=:user_id AND s.artist_id=a.id"""
    return db.session.execute(sql, {"user_id":user_id}).fetchall()