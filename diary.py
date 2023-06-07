import asyncio
import requests
import lxml
from bs4 import BeautifulSoup, SoupStrainer
import sqlite3 as sl
from utilsDB import add_diaryDB


async def fetch_page(url):
    response = requests.get(url)
    return response.content


async def scrape_films_data(page):
    films_list = []
    soup = BeautifulSoup(page, 'lxml', parse_only=SoupStrainer('tr', {'class': 'diary-entry-row'}))
    films = soup.find_all('tr', class_='diary-entry-row')
    for film in films:
        film_data = {}
        film_data['id'] = film.find('td', class_='td-film-details').div['data-film-id']
        film_data['rating'] = int(film.find('td', class_='td-rating').input['value'])
        film_data['like'] = 'icon-liked' in film.find('td', class_='td-like').div.span.span['class']
        film_data['rewatch'] = 'icon-status-off' not in film.find('td', class_='td-rewatch')['class']
        films_list.append(film_data)
    return films_list


async def main(username):
    base_url = "https://letterboxd.com/"+username+"/films/diary/"
    response = await fetch_page(base_url)
    soup = BeautifulSoup(response, 'lxml', parse_only=SoupStrainer('li', {'class': 'paginate-page'}))
    pages = int(soup.find_all('li', class_='paginate-page')[-1].text)
    #pages = 2
    tasks = []
    for page in range(1, pages + 1):
        url = base_url + "page/" + str(page)
        tasks.append(fetch_page(url))

    pages = await asyncio.gather(*tasks)

    films_data = []
    for page in pages:
        films_data += await scrape_films_data(page)

    return films_data


def get_diary(username):
    loop = asyncio.get_event_loop()
    data = loop.run_until_complete(main(username))
    data2 = []
    for element in data:
        data2.append((element['id'], element['like'], element['rewatch'], element['rating']))
    add_diaryDB(data2)
    return data


if __name__ == '__main__':
    print(len(get_diary('giudimax')))
