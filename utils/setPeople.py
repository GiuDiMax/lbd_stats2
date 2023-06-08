import pandas as pd
import requests
from threading import Thread, Semaphore
import json
from utils.utilsDB import get_watchDB, add_people, add_names
from config import *
from keys import tmdb_api_key

global sem, people
sem = Semaphore()


def credits(url, tmdb):
    global people, sem
    r = requests.get(url)
    j = json.loads(r.text)
    pep = []
    if 'cast' in j:
        for person in j['cast']:
            if '(uncredited)' not in person['character']:
                pep.append({'id': person['id'], 'name': person['name'], 'tmdb': tmdb, 'tv': False, 'role': 'a'})
        sem.acquire()
        people = people + pep
        sem.release()
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
    th = []
    for f in get_watchDB(False, True):
        if f[2] == 1:
            urlx = url_tv
        else:
            urlx = url
        th.append(Thread(target=credits, args=(urlx.format(f[5]), f[5])))
    for t in th:
        t.start()
    for t in th:
        t.join()

    df = pd.DataFrame(people)
    add_people(list(df.drop(['name'], axis=1).itertuples(index=False, name=None)))
    df = df.groupby(['id', 'name']).size().reset_index()
    add_names(list(df.drop([0], axis=1).itertuples(index=False, name=None)))


if __name__ == '__main__':
    (setPeople())
