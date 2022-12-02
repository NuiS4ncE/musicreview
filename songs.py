from db import db


def get_song_info(song_id):
    sql = """SELECT s.name, u.name FROM songs s, users u
    WHERE s.id=:song_id AND u.creator_id=u.id"""
    return db.session.execute(sql, {"song_id": song_id}).fetchone()

def get_reviews(song_id):
    sql = """SELECT u.name, r.stars, r.comment FROM reviews r, users u 
    WHERE r.user_id=u.id AND r.song_id=:song_id ORDER BY r.id"""
    return db.session.execute(sql, {"song_id": song_id}).fetchall()

def get_by_genre(gname):
    sql = """SELECT s.id, s.sname, s.sdesc FROM songs s, genres g 
    WHERE g.gname=:gname ORDER BY s.sname"""
    return db.session.execute(sql, {"gname": gname}).fetchall()

def add_song(creator_id, genre_id, sname, gname, sdesc, hyperlink, condition):
    sql = """INSERT INTO songs (creator_id, genre_id, sname, gname, sdesc, hyperlink, condition)
            VALUES (:creator_id, :genre_id, :sname, :gname, :sdesc, :hyperlink, :condition) RETURNING id"""
    genre_id = db.session.execute(sql, {"creator_id":creator_id, "genre_id":genre_id, "sname":sname, 
    "gname":gname, "sdesc":sdesc, "hyperlink":hyperlink, "condition":condition}).fetchone()[0]
    db.session.commit()
    return genre_id

def get_all_songs():
    sql = """SELECT id, sname, gname FROM songs ORDER BY sname"""
    return db.session.execute(sql).fetchall()

def get_by_id(song_id):
    sql = """SELECT id, sname, gname, sdesc, hyperlink, condition FROM songs WHERE id=:song_id"""
    return db.session.execute(sql, {"song_id": song_id}).fetchone()
