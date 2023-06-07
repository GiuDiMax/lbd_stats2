import pandas as pd
import pickle
from utils.set_tmdb import get_tmdb2
from utils.utilsDB import add_tmdbDB, get_watchDB


def lbd_to_tmdb():
    watch = []
    for w in get_watchDB():
        watch.append({'id': w[0]})
    watch = pd.DataFrame(watch)
    with open('utils\\links', 'rb') as file:
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

    data2 = []
    for index, row in df.iterrows():
        if str(row['tmdb']) != 'nan':
            data2.append((row['id'], row['tmdb'], False))
        else:
            data2.append((row['id'], row['tmdb_tv'], True))
    add_tmdbDB(data2)
    return data2


if __name__ == "__main__":
    lbd_to_tmdb()