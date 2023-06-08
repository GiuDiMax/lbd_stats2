from utils.createDB import initializedb
from utils.diary import get_diary
from utils.watch import get_watched
from utils.lbd_to_tmdb import lbd_to_tmdb
from utils.setPeople import setPeople
from utils.setDetails import setDetails
from config import *


initializedb()
get_watched(username)
#get_diary(username)
lbd_to_tmdb()
setDetails()
setPeople()
