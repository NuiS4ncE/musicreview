from db import db

def get_all_genres():
    sql = "SELECT id, gname FROM genres ORDER BY gname"
    return db.session.execute(sql).fetchall()

def get_my_genres(user_id):
    sql = """SELECT id, gname FROM genres 
            WHERE creator_id=:user_id ORDER BY gname"""
    return db.session.execute(sql, {"user_id":user_id}).fetchall()

def add_genre(gname, gdesc, creator_id):
    sql = """INSERT INTO genres (creator_id, gname, gdesc)
            VALUES (:creator_id, :gname, :gdesc) RETURNING gname"""
    genre_id = db.session.execute(sql, {"creator_id":creator_id, "gname":gname, "gdesc":gdesc}).fetchone()[0]
    return genre_id

def remove_genre(genre_id, user_id):
    sql = "UPDATE genres WHERE id=:id AND creator_id=:user_id"
    db.session.execute(sql, {"id":genre_id, "user_id":user_id})
    db.session.commit()

def get_genre_info(gname):
    sql = """SELECT gname, gdesc FROM genres WHERE gname=:gname"""
    return db.session.execute(sql, {"gname":gname}).fetchone()

