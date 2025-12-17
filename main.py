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


def get_search_type():
    search_type = input("What type of search? (1. Full, 2. Questions): ")

    if search_type != "1" and search_type != "2":
        print(f"Error: Input '{search_type}' not an option.")
        get_search_type()


def loop_keyword_seeds(seeds, search_type):
    all_keywords = []

    for kw in seeds:
        df = get_keywords(
            kw,
            limit=20,
            report_type=(
                "phrase_fullsearch" if search_type == 1 else "phrase_questions"
            ),
        )
        df["seed"] = kw
        all_keywords.append(df)

    return all_keywords


def export_keywords(df):
    keywords = pd.concat(df, ignore_index=True)
    keywords.to_csv("output.csv")


def main():
    seed_keywords = input("Enter seed keywords separated by ',': ").split(", ")
    search_type = get_search_type()

    keywords = loop_keyword_seeds(seed_keywords, search_type)
    export_keywords(keywords)


if __name__ == "__main__":
    main()
