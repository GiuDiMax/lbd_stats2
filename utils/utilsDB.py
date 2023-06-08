import sqlite3 as sl
from config import *


def cleanDB():
    con = sl.connect(dbname)
    with con:
        con.execute('DELETE FROM DIARY')
        con.execute('DELETE FROM WATCH')
        con.execute('DELETE FROM TMDB')


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
        con.execute('DELETE FROM TMDB')
    sql = 'INSERT INTO TMDB (id, tmdb, tv) values(?, ?, ?)'
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
        if tmdb:
            data = con.execute('SELECT * FROM WATCH LEFT JOIN TMDB ON WATCH.id = TMDB.id')
        else:
            data = con.execute('SELECT * FROM WATCH')
    for x in data:
        if slug:
            data2.append(x[0])
        else:
            data2.append(x)
    return data2
