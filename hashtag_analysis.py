from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL

import json
import pandas as pd

def db_connection():
    with open('config.json', 'r') as f:
        config = json.load(f)
    return create_engine(URL(**config))

engine = db_connection()
df = pd.read_sql("SELECT hashtags FROM cavadoodle", engine)

count_histogram = {}

for eachArray in df['hashtags']:
    print(len(eachArray))
