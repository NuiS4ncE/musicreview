from db import db

def get_all_artists():
    sql = "SELECT id, aname FROM artists ORDER BY aname"
    return db.session.execute(sql).fetchall()

def add_artist(creator_id, genre_id, aname):
    sql = """INSERT INTO artists (creator_id, genre_id, aname)
            VALUES (:creator_id, :genre_id, :aname) RETURNING id"""
    artist_id = db.session.execute(sql, {"creator_id":creator_id, "genre_id":genre_id, "aname":aname}).fetchone()[0]
    db.session.commit()
    return artist_id

def get_by_id(artist_id):
    sql = """SELECT id, aname FROM artists WHERE id=:artist_id"""
    artist = db.session.execute(sql, {"artist_id":artist_id}).fetchone()
    return artist