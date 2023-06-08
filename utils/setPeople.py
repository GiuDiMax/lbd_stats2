import pandas as pd
import requests
from threading import Thread, Semaphore
import json
from utils.utilsDB import get_watchDB, add_people, add_names
from config import *
from time import sleep
import random

global sem, people
sem = Semaphore()


def credits(url, tmdb):
    global people, sem
    try:
        r = requests.get(url)
        j = json.loads(r.text)
    except:
        sleep(random.uniform(0, 1))
        credits(url, tmdb)
    pep = []
    if 'status_code' in j and not j['status_code'] == 34:
        return
    if 'cast' in j:
        for person in j['cast']:
            if '(uncredited)' not in person['character']:
                pep.append({'id': person['id'], 'name': person['name'], 'tmdb': tmdb, 'tv': False, 'role': 'a'})
    if 'crew' in j:
        for person in j['crew']:
            if person['job'] in crewlist:
                pep.append({'id': person['id'], 'name': person['name'], 'tmdb': tmdb, 'tv': False, 'role': crewlist[person['job']]})
    sem.acquire()
    people = people + pep
    sem.release()


def setPeople():
    global people
    people = []
    url = "https://api.themoviedb.org/3/movie/{}/credits?language=en-US&api_key="+tmdb_api_key
    url_tv = "https://api.themoviedb.org/3/tv/{}/credits?language=en-US&api_key="+tmdb_api_key
    w = get_watchDB(False, True)
    n = 50
    for i in range(int(len(w)/n) + 1):
        th = []
        for f in w[i*n: (i+1)*n]:
            if f[5] == 1:
                urlx = url_tv
            else:
                urlx = url
            th.append(Thread(target=credits, args=(urlx.format(f[4]), f[4])))
        for t in th:
            t.start()
        for t in th:
            t.join()
        sleep(0.5)
    df = pd.DataFrame(people)
    add_people(list(df.drop(['name'], axis=1).itertuples(index=False, name=None)))
    df = df.groupby(['id', 'name']).size().reset_index()
    add_names(list(df.drop([0], axis=1).itertuples(index=False, name=None)))


if __name__ == '__main__':
    (setPeople())
