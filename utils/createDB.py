import sqlite3 as sl
from config import *


def initializedb():
    con = sl.connect(dbname)

    with con:
        for table in ['DIARY', 'WATCH', 'TMDB', 'PEOPLE', 'NAMES']:
            try:
                con.execute('DROP TABLE ' + table + ';')
            except:
                pass


        con.execute("""
            CREATE TABLE WATCH (
                id INTEGER NOT NULL PRIMARY KEY,
                slug TEXT,
                like BOOLEAN,
                rating INTEGER
            );
            """)
        con.execute("""
            CREATE TABLE DIARY (
                id INTEGER,
                date DATE,
                like BOOLEAN,
                rating INTEGER,
                rewatch BOOLEAN,
            );
            """)

        con.execute("""
            CREATE TABLE TMDB (
                id INTEGER NOT NULL PRIMARY KEY,
                tmdb INTEGER,
                tv BOOLEAN
            );
            """)

        con.execute("""
            CREATE TABLE NAMES (
                id INTEGER NOT NULL PRIMARY KEY,
                name STRING
            );
            """)

        con.execute("""
            CREATE TABLE PEOPLE (
                id INTEGER NOT NULL,
                tmdb INTEGER NOT NULL,
                tv BOOLEAN,
                role STRING,
                constraint PK PRIMARY KEY (id, tmdb, tv, role)
            );
            """)