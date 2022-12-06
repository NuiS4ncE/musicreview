# Musicreview 

Sovellus testattavissa osoitteessa: https://musicreview.fly.dev/

Sovelluksella voit arvostella ja kommentoida musiikkivideoita ja kappaleita. 

## Ominaisuudet

Sovelluksen ominaisuuksia tällä hetkellä ovat: 

* Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen 
* Käyttäjä voi lisätä kappaleen, antaa sille arvosanan ja kirjoittaa arvion 
* Käyttäjä voi lisätä ulkoisen linkin kappaleeseen
* Sovellus tukee embed-muodossa YouTube- ja SoundCloud-linkkejä
* Käyttäjä voi lisätä musiikin tyylilajin ("genren") 
* Käyttäjä voi lisätä artistin
* Käyttäjä voi tarkastella lisäämiään tyylilajeja, artisteja ja kappaleita 


Sovellukseen lisättävät ominaisuudet: 
* Käyttäjä voi kommentoida kappaleen arviota 
* Käyttäjä voi poistaa lisäämänsä kappaleen 

## Paikallinen suoritus ja testaus

Paikallisesti ohjelmaa voi testata seuraavasti: 
1. Kloonaa repo `git clone git@github.com:NuiS4ncE/musicreview.git`
2. Poista `db.py`-moduulista rivin 5 kohta `.replace("://", "ql://", 1)`.
3. Luo oma `.env`, jonne luo omat ympäristömuuttujat `SECRET_KEY=` ja `DATABASE_URL=`.
4. Aja terminaalissa `pip install requirements.txt`. 
5. Aja terminaalissa `source venv/bin/activate` sekä luo terminaalissa PostgreSQL-tietokannan taulut `pgsql < schema.sql`.
6. Lopuksi aja terminaalissa `flask run`.