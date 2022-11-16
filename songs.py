from db import db


def get_song_info(song_id):
    sql = """SELECT s.name, u.name FROM songs s, users u
    WHERE s.id=:song_id AND u.creator_id=u.id"""
    return db.session.execute(sql, {"song_id": song_id}).fetchone()[0]

