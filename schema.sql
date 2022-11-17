CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT,
    password TEXT, 
    role INTEGER
);

CREATE TABLE genres (
    id SERIAL PRIMARY KEY,
    creator_id INTEGER REFERENCES users,
    gname TEXT,
    gdesc TEXT,
    CONSTRAINT gname_unique UNIQUE (gname)
);

CREATE TABLE songs ( 
    ID SERIAL PRIMARY KEY,
    genre_id INTEGER REFERENCES genres,
    creator_id INTEGER REFERENCES users,
    sname TEXT,
    genre TEXT,
    sdesc TEXT,
    hyperlink TEXT
);

CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    song_id INTEGER REFERENCES songs,
    stars INTEGER, 
    comment TEXT
);