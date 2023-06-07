import sqlite3 as sl
from config import *


def initializedb():
    con = sl.connect(dbname)

    with con:
        for table in ['DIARY', 'WATCH', 'TMDB']:
            try:
                con.execute('DROP TABLE ' + table + ';')
            except:
                pass


    with con:
        con.execute("""
            CREATE TABLE WATCH (
                id INTEGER NOT NULL PRIMARY KEY,
                slug TEXT,
                like BOOLEAN,
                rating INTEGER
            );
            """)

    with con:
        con.execute("""
            CREATE TABLE DIARY (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                movie_id INTEGER,
                like BOOLEAN,
                rewatch BOOLEAN,
                rating INTEGER
            );
            """)

    with con:
        con.execute("""
            CREATE TABLE TMDB (
                id INTEGER NOT NULL PRIMARY KEY,
                tmdb INTEGER,
                tv BOOLEAN
            );
            """)
