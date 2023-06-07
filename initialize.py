from createDB import initializedb
from diary import get_diary
from watch import get_watched
from lbd_to_tmdb import lbd_to_tmdb
from threading import Thread

user = 'giudimax'
initializedb()

t1 = Thread(target=get_watched, args=(user, ))
t2 = Thread(target=get_diary, args=(user, ))
t1.start()
t2.start()
t1.join()
t2.join()
lbd_to_tmdb()