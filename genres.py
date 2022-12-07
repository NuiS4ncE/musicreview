from db import db

def get_all_genres():
    sql = "SELECT id, gname, gdesc, genre_url FROM genres ORDER BY gname"
    return db.session.execute(sql).fetchall()

def get_my_genres(user_id):
    sql = """SELECT id, gname FROM genres 
            WHERE creator_id=:user_id ORDER BY gname"""
    return db.session.execute(sql, {"user_id":user_id}).fetchall()

def add_genre(gname, gdesc, creator_id, genre_url):
    sql = """INSERT INTO genres (creator_id, gname, gdesc, genre_url)
            VALUES (:creator_id, :gname, :gdesc, :genre_url) RETURNING id"""
    genre_id = db.session.execute(sql, {"creator_id":creator_id, "gname":gname, "gdesc":gdesc, "genre_url":genre_url}).fetchone()[0]
    db.session.commit()
    return genre_id

def remove_genre(genre_id, user_id):
    sql = "UPDATE genres WHERE id=:id AND creator_id=:user_id"
    db.session.execute(sql, {"id":genre_id, "user_id":user_id})
    db.session.commit()

def get_genre_info(genre_id):
    sql = """SELECT id, gname, gdesc FROM genres WHERE id=:genre_id"""
    return db.session.execute(sql, {"id":genre_id}).fetchone()

def get_genre_info_by_name(gname):
    sql = """SELECT id, gname, gdesc, genre_url FROM genres WHERE gname=:gname"""
    return db.session.execute(sql, {"gname":gname}).fetchone()

def get_genre_info_by_url(genre_url):
    sql = """SELECT id, gname, gdesc, genre_url FROM genres WHERE genre_url=:genre_url"""
    return db.session.execute(sql, {"genre_url":genre_url}).fetchone()

def check_if_gexists(gname):
    sql = """SELECT EXISTS (SELECT 1 FROM genres WHERE gname=:gname)"""
    return db.session.execute(sql, {"gname":gname}).fetchone()

def get_by_user_id(user_id):
    sql = """SELECT gname FROM genres 
    WHERE genres.creator_id=:user_id"""
    return db.session.execute(sql, {"user_id":user_id}).fetchall()
