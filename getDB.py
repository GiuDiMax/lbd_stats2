import pandas as pd
import pickle
from lbd_to_tmdb import lbd_to_tmdb
import requests
from threading import Thread, Semaphore
import json

global sem, t_cast
sem = Semaphore()


def credits(url, rating, slug):
    global t_cast, sem
    r = requests.get(url)
    j = json.loads(r.text)
    cast = []
    if 'cast' in j:
        for person in j['cast']:
            if '(uncredited)' not in person['character']:
                cast.append({'id': person['id'], 'rating': rating, 'name': person['name']})
        sem.acquire()
        t_cast = t_cast + cast
        sem.release()


def credits_tv(url, rating, slug):
    global t_cast, sem
    r = requests.get(url)
    j = json.loads(r.text)
    cast = []
    if 'cast' in j:
        for person in j['cast']:
            if '(uncredited)' not in person['character']:
                cast.append({'id': person['id'], 'rating': rating, 'name': person['name']})
        sem.acquire()
        t_cast = t_cast + cast
        sem.release()


def main():
    global t_cast
    t_cast = []
    key = '6fff7e293df6a808b97101a26c86a545'
    film, tv = lbd_to_tmdb()
    url = "https://api.themoviedb.org/3/movie/{}/credits?language=en-US&api_key="+key
    url_tv = "https://api.themoviedb.org/3/tv/{}/credits?language=en-US&api_key="+key
    th = []
    for f in film:
        th.append(Thread(target=credits, args=(url.format(f['tmdb']), f['r'], f['slug'])))
    for t in tv:
        th.append(Thread(target=credits_tv, args=(url_tv.format(t['tmdb']), t['r'], t['slug'])))
    for t in th:
        t.start()
    for t in th:
        t.join()


    df = pd.DataFrame(t_cast)
    #df1 = df.groupby(['id']).size().reset_index(name='n').sort_values(by=['n'], ascending=False)
    #df = df.groupby(['id']).size().reset_index(name='n').sort_values(by=['n'], ascending=False)
    df = df.groupby(['id', 'name']) \
        .agg({'id': 'size', 'rating': 'mean'}) \
        .rename(columns={'id': 'count', 'rating': 'avg'})
    sum = df.sort_values(by=['count', 'avg'], ascending=[False, False]).head(25).reset_index()
    top = df[df['count'] > 3].sort_values(by=['avg', 'count'], ascending=[False, False]).head(25).reset_index()
    print(sum)
    print("\n")
    print(top)

main()
