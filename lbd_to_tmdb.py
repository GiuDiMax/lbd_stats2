import pandas as pd
import pickle
from get_tmdb import get_tmdb2


def lbd_to_tmdb(diary=False, year=0):
    if diary:
        with open('diary', 'rb') as file:
            diary = pd.DataFrame(pickle.load(file))
    else:
        with open('watch', 'rb') as file:
            watch = pd.DataFrame(pickle.load(file))
    with open('links', 'rb') as file:
        links = pd.DataFrame(pickle.load(file))

    links["id"] = pd.to_numeric(links["id"], errors='ignore', downcast='unsigned')
    watch["id"] = pd.to_numeric(watch["id"], downcast='unsigned')

    df = pd.merge(watch, links, on='id', how='left', indicator=True)
    mancanti = df[df['_merge'] == 'left_only']

    mancanti2 = []
    for index, row in mancanti.iterrows():
        mancanti2.append(row['slug'])

    if len(mancanti) > 0:
        new = pd.DataFrame(get_tmdb2(mancanti2[:2]))
        new["id"] = pd.to_numeric(new["id"])
        new = pd.merge(watch, new, on='id', how='right', indicator=True)
        df = pd.concat([df, new])

    film = []
    tv = []
    #print(df)
    for index, row in df.iterrows():
        if str(row['tmdb']) != 'nan':
            film.append({'tmdb': int(row['tmdb']), 'r': row['rating'], 'slug': row['slug']})
        else:
            tv.append({'tmdb': int(row['tmdb_tv']), 'r': row['rating'], 'slug': row['slug']})
    return film, tv


if __name__ == "__main__":
    lbd_to_tmdb()