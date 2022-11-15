from db import db

def get_all_genres():
    sql = "SELECT id, gname FROM genres ORDER BY gname"
    return db.session.execute(sql).fetchall()

def get_my_genres(user_id):
    sql = """SELECT id, gname FROM genres 
            WHERE creator_id=:user_id ORDER BY gname"""
    return db.session.execute(sql, {"user_id":user_id}).fetchall()

def add_genre(gname, creator_id):
    sql = """INSERT INTO genres (creator_id, gname)
            VALUES (:creator_id, :name) RETURNING id"""
    genre_id = db.session.execute(sql, {"creator_id":creator_id, "gname":gname}).fetchone()[0]
    return genre_id

def remove_genre(genre_id, user_id):
    sql = "UPDATE genres WHERE id=:id AND creator_id=:user_id"
    db.session.execute(sql, {"id":genre_id, "user_id":user_id})
    db.session.commit()