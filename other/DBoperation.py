import sqlite3 as sl
from config import *

con = sl.connect(dbname)
with con:
    #con.execute('DROP TABLE PEOPLE;')
    con.execute("""
            CREATE TABLE DETAILS (
                tmdb INTEGER NOT NULL PRIMARY KEY,
                title STRING,
                year INTEGER,
                runtime INTEGER,
                genres STRING,
                languages STRING,
                countries STRING
            );
        """)
