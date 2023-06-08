import pandas as pd
import requests
from threading import Thread, Semaphore
import json
from utils.utilsDB import get_watchDB, add_details
from config import *
from time import sleep
import random

global sem, detail
sem = Semaphore()


def details(url, tmdb, tv, idx):
    global detailsdf, sem
    try:
        r = requests.get(url)
        j = json.loads(r.text)
    except:
        sleep(random.uniform(0, 1))
        details(url, tmdb, tv, idx)
    if 'status_code' in j and j['status_code'] == 34:
        return
    if 'title' in j:
        title = j['title']
    else:
        title = j['name']
    if 'release_date' in j:
        year = int(j['release_date'].split("-", 1)[0])
    else:
        year = int(j['first_air_date'].split("-", 1)[0])
    if 'runtime' in j:
        runtime = int(j['runtime'])
    else:
        try:
            runtime = int(j['episode_run_time'][0]) * int(j['number_of_episodes'])
        except:
            runtime = 60 * int(j['number_of_episodes'])
    genres = ','.join(l['name'] for l in j['genres'])
    languages = ','.join(l['english_name'] for l in j['spoken_languages'])
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
        for f in w[i*n: (i+1)*n]:
            if f[5] == 1:
                urlx = url_tv
            else:
                urlx = url
            th.append(Thread(target=details, args=(urlx.format(f[4]), f[4], f[5], f[0])))
        for t in th:
            t.start()
        for t in th:
            t.join()
        sleep(0.5)
    add_details(detail)


if __name__ == '__main__':
    setDetails()
