import os
import requests
import pandas as pd
import io

base_url = "https://api.semrush.com/"


def get_keywords(phrase: str, limit=1):
    params = {
        "type": "phrase_fullsearch",
        "key": os.getenv("API_KEY"),
        "phrase": phrase,
        "database": "us",
        "export_columns": "Ph,Nq",
        "display_limit": limit,
    }

    response = requests.get(base_url + "?", params)
    response.raise_for_status()
    return pd.read_csv(io.StringIO(response.text), sep=";")


# loop over seed keywords and get keywords containing the seed (broad match)
seed_keywords = [
    "surety bonds",
    "small business insurance",
    "business liability insurance",
]

all_keywords = []
for kw in seed_keywords:
    df = get_keywords(kw, limit=20)
    df["seed"] = kw
    all_keywords.append(df)

keywords_raw = pd.concat(all_keywords, ignore_index=True)
# print(keywords_raw.head())
keywords_raw.to_csv("output.csv")
