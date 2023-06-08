import sqlite3 as sl
from config import *

con = sl.connect(dbname)
with con:
    con.execute('DROP TABLE PEOPLE;')
    con.execute("""
            CREATE TABLE PEOPLE (
                id INTEGER NOT NULL,
                tmdb INTEGER NOT NULL,
                tv BOOLEAN,
                role STRING,
                constraint PK PRIMARY KEY (id, tmdb, tv, role)
            );
        """)
