import sqlite3 as sl
from config import *

con = sl.connect(dbname)
with con:
    con.execute('DROP TABLE PEOPLE;')
    con.execute("""
        CREATE TABLE PEOPLE (
            moviepersonID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            personID INTEGER,
            tmdb INTEGER,
            tv BOOLEAN,
            role STRING
        );
        """)
