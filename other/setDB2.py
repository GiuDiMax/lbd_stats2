import sqlite3 as sl
from config import *

con = sl.connect(dbname)
with con:
    con.execute('DROP TABLE TMDB;')
    con.execute("""
        CREATE TABLE TMDB (
            id INTEGER NOT NULL PRIMARY KEY,
            tmdb INTEGER,
            tv BOOLEAN
        );
        """)
