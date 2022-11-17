from db import db


def get_song_info(song_id):
    sql = """SELECT s.name, u.name FROM songs s, users u
    WHERE s.id=:song_id AND u.creator_id=u.id"""
    return db.session.execute(sql, {"song_id": song_id}).fetchone()[0]

def get_reviews(song_id):
    sql = """SELECT u.name, r.stars, r.comment FROM reviews r, users u 
    WHERE r.user_id=u.id AND r.song_id=:song_id ORDER BY r.id"""
    return db.session.execute(sql, {"song_id": song_id}).fetchall()