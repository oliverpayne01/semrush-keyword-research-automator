# automatically export a list of filtered keywords based on seeds

# dict of seeds w/ properties for filter inclusions and exclusions
# specify match type

import os
import requests
import pandas as pd

base_url = "https://api.semrush.com/"


def get_related_keywords(phrase, db, limit=1):
    params = {
        "type": "phrase_related",
        "key": os.getenv("API_KEY"),
        "phrase": phrase,
        "database": db,
        "export_columns": "",
        "display_limit": limit,
    }

    r = requests.get(base_url + "?", params=params)
    r.raise_for_status()
    # df = pd.read_csv()
