import os
from db import db
from flask import abort, request, session 
from werkzeug.security import check_password_hash, generate_password_hash

def login(username, password):
    sql = "SELECT password, id, FROM users WHERE username=:username"
    result = db.session.execute(sql, {"name":username})
    username = result.fetchone()
    if not username:
        return False
    if not check_password_hash(username[0], password):
        return False
    session["user_id"] = username[1]
    session["username"] = username
    session["csrf_token"] = os.urandom(16).hex()
    return True

def logout():
    del session["user_id"]
    del session["username"]
    
def register(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = """INSERT INTO users (username, password)
        VALUES (:username, :password"""
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
    except:
        return False
    return login(username, password)

def user_id():
    return session.get("user_id", 0)

def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

def get_user_info(user_id):
    sql = """SELECT id, sname FROM songs 
            WHERE creator_id=:user_id ORDER BY sname"""
    songs = db.session.execute(sql, {"user_id": user_id}).fetchall()
    sql = """SELECT id, gname FROM genres
            WHERE creator_id=:user_id ORDER BY gname"""
    genres = db.session.execute(sql, {"user_id": user_id}).fetchall()
    print(songs)
    print(genres)
    userData = []
    #for song in songs:
        #userData.append((song[]))
    return userData