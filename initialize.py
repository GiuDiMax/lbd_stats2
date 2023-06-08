from utils.createDB import initializedb
from utils.diary import get_diary
from utils.watch import get_watched
from utils.lbd_to_tmdb import lbd_to_tmdb
from keys import username
from utils.setPeople import setPeople

initializedb()
get_watched(username)
get_diary(username)
lbd_to_tmdb()
setPeople()