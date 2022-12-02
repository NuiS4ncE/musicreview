CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL,
    password TEXT NOT NULL, 
    role INTEGER
);

CREATE TABLE genres (
    id SERIAL PRIMARY KEY,
    creator_id INTEGER REFERENCES users,
    gname TEXT NOT NULL,    
    gdesc TEXT NOT NULL,
    genre_url TEXT,
    CONSTRAINT gname_unique UNIQUE (gname)
);

CREATE TABLE songs ( 
    id SERIAL PRIMARY KEY,
    genre_id INTEGER REFERENCES genres,
    creator_id INTEGER REFERENCES users,
    sname TEXT NOT NULL,
    gname TEXT NOT NULL,
    sdesc TEXT NOT NULL,
    hyperlink TEXT NOT NULL
);

CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    song_id INTEGER REFERENCES songs,
    stars INTEGER, 
    comment TEXT NOT NULL
);