import pandas as pd
import requests
from threading import Thread, Semaphore
import json
from utils.utilsDB import get_watchDB, add_people, add_names
from config import *

global sem, detailsdf
sem = Semaphore()


def details(url, tmdb):
    global detailsdf, sem
    r = requests.get(url)
    j = json.loads(r.text)
    det = []

    sem.acquire()
    detailsdf = detailsdf + det
    sem.release()


def setPeople():
    global detailsdf
    detailsdf = []
    url = "https://api.themoviedb.org/3/movie/{}/credits?language=en-US&api_key="+tmdb_api_key
    url_tv = "https://api.themoviedb.org/3/tv/{}/credits?language=en-US&api_key="+tmdb_api_key
    th = []
    for f in get_watchDB(False, True):
        if f[2] == 1:
            urlx = url_tv
        else:
            urlx = url
        th.append(Thread(target=details, args=(urlx.format(f[5]), f[5])))
    for t in th:
        t.start()
    for t in th:
        t.join()


if __name__ == '__main__':
    (setPeople())
