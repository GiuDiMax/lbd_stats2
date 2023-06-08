import sqlite3 as sl
from config import *

query = """
SELECT * FROM TMDB
"""

con = sl.connect(dbname)
with con:
    data = con.execute(query)

for line in data:
    print(line)
