import sqlite3 as sl
from config import *
import pandas as pd

query = """
SELECT * FROM PEOPLE p
GROUP BY p.personID
"""

con = sl.connect(dbname)
with con:
    df = pd.read_sql_query(query, con)
print(df)
