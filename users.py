import os
from db import db
from flask import abort, request, session 
from werkzeug.security import check_password_hash, generate_password_hash

def login(username, password):
    sql = "SELECT password, id FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    #print("in login function")
    if not user:
        return False
    if not check_password_hash(user[0], password):
        return False
    #print("session cast next")
    session["user_id"] = user[1]
    session["username"] = username
    session["csrf_token"] = os.urandom(16).hex()
    #print("session casts done, next returning true")
    return True

def logout():
    del session["user_id"]
    del session["username"]
    
def register(username, password):
    hash_value = generate_password_hash(password)
    #print("In users.register() function")
    try:
        sql = """INSERT INTO users (username, password)
        VALUES (:username, :password)"""
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
    sql = """SELECT username, sname, gname, aname FROM users 
    INNER JOIN songs ON songs.creator_id=:user_id 
    INNER JOIN genres ON genres.creator_id=:user_id 
    INNER JOIN artists ON artists.creator_id=:user_id"""
    userInfo = db.session.execute(sql, {"user_id": user_id}).fetchall()
    print(userInfo)
    return userInfo