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
                like BOOLEAN,
                rewatch BOOLEAN,
                rating INTEGER
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
                personID INTEGER,
                tmdb INTEGER,
                tv BOOLEAN,
                role STRING
            );
            """)