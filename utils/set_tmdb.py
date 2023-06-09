import asyncio
import requests
import lxml
from bs4 import BeautifulSoup, SoupStrainer
from utils.utilsDB import add_tmdbDB, get_watchDB


async def fetch_page(url):
    response = requests.get(url)
    return response.content


async def scrape_page(page):
    movie = {}
    soup = BeautifulSoup(page, 'lxml', parse_only=SoupStrainer('div'))
    movie['id'] = soup.find('div', class_='film-poster')['data-film-id']
    for link in soup.find_all('a', class_='micro-button'):
        if 'tmdb' in link['data-track-action'].lower():
            if link['href'].split('/')[-3] == 'movie':
                movie['tmdb'] = int(link['href'].split('/')[-2])
            else:
                movie['tmdb_tv'] = int(link['href'].split('/')[-2])
            break
    return movie


async def main(pages):
    tasks = []
    movies = []
    for page in pages:
        tasks.append(fetch_page(page))

    responses = await asyncio.gather(*tasks)

    scrape_tasks = []
    for response in responses:
        scrape_tasks.append(scrape_page(response))

    results = await asyncio.gather(*scrape_tasks)

    for result in results:
        movies.append(result)
    return movies


def get_tmdb():
    base_url = "https://letterboxd.com/film/"
    urls = []
    watch = get_watchDB(True)
    for film in watch:
        urls.append(base_url + film)
    loop = asyncio.get_event_loop()
    data = loop.run_until_complete(main(urls))
    data2 = []
    for element in data:
        if 'tmdb_tv' in element:
            data2.append((element['id'], element['tmdb_tv'], True))
        else:
            data2.append((element['id'], element['tmdb'], False))
    add_tmdbDB(data2)
    return data


def get_tmdb2(lista):
    base_url = "https://letterboxd.com/film/"
    urls = []
    for film in lista:
        urls.append(base_url + film)
    loop = asyncio.get_event_loop()
    data = loop.run_until_complete(main(urls))
    return data


if __name__ == '__main__':
    print(len(get_tmdb()))