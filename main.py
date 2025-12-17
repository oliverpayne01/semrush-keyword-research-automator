import os
import requests
import pandas as pd
import io

base_url = "https://api.semrush.com/"


def get_keywords(phrase: str, limit=1, report_type="phrase_fullsearch"):
    params = {
        "type": report_type,
        "key": os.getenv("API_KEY"),
        "phrase": phrase,
        "database": "us",
        "export_columns": "Ph,Nq",
        "display_limit": limit,
    }

    response = requests.get(base_url + "?", params)
    response.raise_for_status()
    return pd.read_csv(io.StringIO(response.text), sep=";")


def main():
    seed_keywords = input("Enter seed keywords separated by ',': ").split(", ")

    def get_keywords_from_seeds():
        all_keywords = []

        for kw in seed_keywords:
            df_broad = get_keywords(kw, limit=10)
            df_broad["seed"] = kw
            all_keywords.append(df_broad)

            df_questions = get_keywords(kw, limit=10, report_type="phrase_questions")
            df_questions["seed"] = kw
            all_keywords.append(df_questions)

            keywords_raw = pd.concat(all_keywords, ignore_index=True)
            # print(keywords_raw.head())
            keywords_raw.to_csv("output.csv")

    get_keywords_from_seeds()


if __name__ == "__main__":
    main()
