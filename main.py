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
        "export_columns": "Ph,In,Nq",
        "display_limit": limit,
    }

    response = requests.get(base_url + "?", params)
    response.raise_for_status()
    return pd.read_csv(io.StringIO(response.text), sep=";")


def main():
    seed_keywords = input("Enter seed keywords separated by ',': ").split(", ")
    search_type = input("What type of search? (1. Full, 2. Questions): ")

    def get_keywords_from_seeds():
        all_keywords = []

        for kw in seed_keywords:
            df = get_keywords(
                kw,
                limit=1,
                report_type=(
                    "phrase_fullsearch" if search_type == 1 else "phrase_questions"
                ),
            )
            df["seed"] = kw
            all_keywords.append(df)

            keywords_raw = pd.concat(all_keywords, ignore_index=True)
            keywords_raw.to_csv("output.csv")

    get_keywords_from_seeds()


if __name__ == "__main__":
    main()

# Comparison (vs, difference)

# Informational
# Commercial
# Transactional

# add option for exclusions
# add option to export directly to a google sheet (would require OAuth)

# get top 5 "product / service keywords"
