import asyncio
import requests
import lxml
from bs4 import BeautifulSoup, SoupStrainer
from utilsDB import add_watchDB


async def fetch_page(url):
    response = requests.get(url)
    return response.content


async def scrape_films_data(page):
    films_list = []
    soup = BeautifulSoup(page, 'lxml', parse_only=SoupStrainer('li', {'class': 'poster-container'}))
    films = soup.find_all('li', class_='poster-container')
    for film in films:
        film_data = {}
        film_data['id'] = film.div['data-film-id']
        film_data['slug'] = film.div['data-film-slug'].split("/")[-2]
        film_data['like'] = len(film.p.find_all('span', {'class': 'like'})) > 0
        film_data['rating'] = 0
        try:
            if 'rated' in film.p.span['class'][-1]:
                film_data['rating'] = int(film.p.span['class'][-1].split("-", 1)[1])
        except:
            pass
        films_list.append(film_data)
    return films_list


async def main(username):
    base_url = "https://letterboxd.com/"+username+"/films/"
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


def get_watched(username):
    loop = asyncio.get_event_loop()
    data = loop.run_until_complete(main(username))
    data2 = []
    for element in data:
        data2.append((element['id'], element['slug'], element['like'], element['rating']))
    add_watchDB(data2)
    return data


if __name__ == '__main__':
    #print(get_watched('giudimax'))
    print(len(get_watched('giudimax')))


