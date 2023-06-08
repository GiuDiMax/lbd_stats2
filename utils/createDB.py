import sqlite3 as sl
from config import *
import os


def initializedb():
    os.remove(dbname)
    con = sl.connect(dbname)

    with con:
        for table in ['DIARY', 'WATCH', 'DETAILS', 'PEOPLE', 'NAMES']:
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
                rewatch BOOLEAN
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

        con.execute("""
                CREATE TABLE DETAILS (
                    id INTEGER NOT NULL PRIMARY KEY,
                    tmdb INTEGER NOT NULL,
                    tv BOOLEAN,
                    title STRING,
                    year INTEGER,
                    runtime INTEGER,
                    genres STRING,
                    languages STRING,
                    countries STRING
                );
            """)