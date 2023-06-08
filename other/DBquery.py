import sqlite3 as sl
from config import *

query = """
SELECT * FROM PEOPLE p LEFT JOIN NAMES n ON p.personID = n.id
"""

con = sl.connect(dbname)
with con:
    data = con.execute(query)

for line in data:
    print(line)
