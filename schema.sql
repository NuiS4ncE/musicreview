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

CREATE TABLE artists (
    id SERIAL PRIMARY KEY,
    genre_id INTEGER REFERENCES genres,
    creator_id INTEGER REFERENCES users,
    aname TEXT NOT NULL
);

CREATE TABLE songs ( 
    id SERIAL PRIMARY KEY,
    genre_id INTEGER REFERENCES genres,
    creator_id INTEGER REFERENCES users,
    artist_id INTEGER REFERENCES artists,
    sname TEXT NOT NULL,
    gname TEXT NOT NULL,
    sdesc TEXT NOT NULL,
    hyperlink TEXT NOT NULL,
    condition TEXT NOT NULL
);

CREATE TABLE songsgenres ( 
    genre_id INTEGER REFERENCES genres,
    song_id INTEGER REFERENCES songs
);

CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    genre_id INTEGER REFERENCES genres,
    song_id INTEGER REFERENCES songs,
    artist_id INTEGER REFERENCES artists,
    stars INTEGER, 
    comment TEXT NOT NULL
);