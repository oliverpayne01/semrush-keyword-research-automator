# automatically export a list of filtered keywords based on seeds

# dict of seeds w/ properties for filter inclusions and exclusions

import os
import requests
import pandas as pd
import io

base_url = "https://api.semrush.com/"


def get_related_keywords(phrase, db, limit=1):
    params = {
        "type": "phrase_fullsearch",
        "key": os.getenv("API_KEY"),
        "phrase": phrase,
        "database": db,
        "export_columns": "Ph,Nq",
        "display_limit": limit,
    }

    response = requests.get(base_url + "?", params)
    response.raise_for_status()
    return pd.read_csv(io.StringIO(response.text), sep=";")


df = get_related_keywords("surety bonds in arizona", "us")
print(df.head())
