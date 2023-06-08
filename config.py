import sys
import configparser

dbname = sys.path[1] + '\\letterboxd.db'
ini = sys.path[1] + '\\config.ini'
crewlist = {
    'Director': 'd',
    'Screenplay': 'w',
}

config = configparser.ConfigParser()
try:
    config.read(ini)
    tmdb_api_key = config['DEFAULT']['tmdb_api_key']
    username = config['DEFAULT']['username']
except:
    config = configparser.ConfigParser()
    username = input("Insert username: ")
    tmdb_api_key = input("Insert tmdb api key: ")
    config['DEFAULT']['username'] = username
    config['DEFAULT']['tmdb_api_key'] = tmdb_api_key
    with open(ini, 'w') as file:
        config.write(file)
