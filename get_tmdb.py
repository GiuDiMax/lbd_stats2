import asyncio
import requests
import lxml
from bs4 import BeautifulSoup, SoupStrainer
import pickle
import time


async def fetch_page(url):
    response = requests.get(url)
    return response.content


async def scrape_page(page):
    movie = {}
    soup = BeautifulSoup(page, 'lxml', parse_only=SoupStrainer('div'))
    movie['id'] = soup.find('div', class_='film-poster')['data-film-id']
    for link in soup.find_all('a', class_='micro-button'):
        if 'tmdb' in link['data-track-action'].lower():
            movie['tmdb'] = int(link['href'].split('/')[-2])
            movie['type'] = link['href'].split('/')[-3]
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
    with open('watch', 'rb') as file:
        watch = pickle.load(file)
    for film in watch:
        urls.append(base_url + film['slug'])
    loop = asyncio.get_event_loop()
    data = loop.run_until_complete(main(urls))
    with open("tmdb", 'wb') as file:
        pickle.dump(data, file)
    return data


if __name__ == '__main__':
    print(len(get_tmdb()))