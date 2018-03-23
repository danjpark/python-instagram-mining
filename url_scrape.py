from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL

import json
import pandas as pd

def db_connection():
    with open('config.json', 'r') as f:
        config = json.load(f)
    return create_engine(URL(**config))

engine = db_connection()
df = pd.read_sql("SELECT * FROM test_table", engine)

print(df)


d = [{'id': 4,
      'name': 'Grace',
      'age': 30}]

pd.DataFrame(d).to_sql('test_table', engine, if_exists='append', index=False)
