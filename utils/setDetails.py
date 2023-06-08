import pandas as pd
import requests
from threading import Thread, Semaphore
import json
from utils.utilsDB import get_watchDB, add_details
from config import *
from time import sleep

global sem, detail
sem = Semaphore()


def details(url, tmdb, tv, idx):
    global detailsdf, sem
    r = requests.get(url)
    j = json.loads(r.text)
    title = j['title']
    year = int(j['release_date'].split("-", 1)[0])
    runtime = int(j['runtime'])
    genres = ','.join(l['name'] for l in j['genres'])
    languages = ','.join(l['name'] for l in j['spoken_languages'])
    countries = ','.join(l['name'] for l in j['production_countries'])
    sem.acquire()
    detail.append((idx, tmdb, tv, title, year, runtime, genres, languages, countries))
    sem.release()


def setDetails():
    global detail
    detail = []
    url = "https://api.themoviedb.org/3/movie/{}?language=en-US&api_key="+tmdb_api_key
    url_tv = "https://api.themoviedb.org/3/tv/{}?language=en-US&api_key="+tmdb_api_key
    w = get_watchDB(False, True)
    n = 50
    for i in range(int(len(w)/n) + 1):
        th = []
        for f in w[i*n: i*n+1]:
            if f[5] == 1:
                urlx = url_tv
            else:
                urlx = url
            th.append(Thread(target=details, args=(urlx.format(f[4]), f[4], f[5], f[0])))
        for t in th:
            t.start()
        for t in th:
            t.join()
        sleep(1)
    add_details(detail)


if __name__ == '__main__':
    setDetails()
