import sqlite3 as sl
from config import *


def add_watchDB(data):
    con = sl.connect(dbname)
    with con:
        con.execute('DELETE FROM WATCH')
    sql = 'INSERT INTO WATCH (id, slug, like, rating) values(?, ?, ?, ?)'
    with con:
        con.executemany(sql, data)


def add_diaryDB(data):
    con = sl.connect(dbname)
    with con:
        con.execute('DELETE FROM DIARY')
    sql = 'INSERT INTO DIARY (id, date, like, rewatch, rating) values(?, ?, ?, ?, ?)'
    with con:
        con.executemany(sql, data)


def add_tmdbDB(data):
    con = sl.connect(dbname)
    with con:
        con.execute('DELETE FROM DETAILS')
    sql = 'INSERT INTO DETAILS (id, tmdb, tv) values(?, ?, ?)'
    with con:
        con.executemany(sql, data)


def add_details(data):
    con = sl.connect(dbname)
    sql = ' REPLACE INTO DETAILS (id, tmdb, tv, title, year, runtime, genres, languages, countries)' \
          ' values(?, ?, ?, ?, ?, ?, ?, ?, ?) '

    with con:
        con.executemany(sql, data)


def add_people(data):
    con = sl.connect(dbname)
    with con:
        con.execute('DELETE FROM PEOPLE')
    sql = 'INSERT OR IGNORE INTO PEOPLE (id, tmdb, tv, role) values(?, ?, ?, ?)'
    with con:
        con.executemany(sql, data)


def add_names(data):
    con = sl.connect(dbname)
    with con:
        con.execute('DELETE FROM NAMES')
    sql = 'INSERT INTO NAMES (id, name) values(?, ?)'
    with con:
        con.executemany(sql, data)


def get_watchDB(slug=False, tmdb=False):
    data2 = []
    con = sl.connect(dbname)
    with con:
        if slug:
            data = con.execute('SELECT SLUG FROM WATCH')
        else:
            if tmdb:
                data = con.execute('SELECT WATCH.*, DETAILS.tmdb, DETAILS.tv '\
                                   'FROM WATCH LEFT JOIN DETAILS ON WATCH.id = DETAILS.id')
            else:
                data = con.execute('SELECT * FROM WATCH')
    for x in data:
        if slug:
            data2.append(x[0])
        else:
            data2.append(x)
    return data2
