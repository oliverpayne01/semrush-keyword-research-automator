import os
import requests
import pandas as pd
import io
import datetime

# Add input to select script entry point (create keyword exclusion list, research)

base_url = "https://api.semrush.com/"


def get_seed_keywords():
    seed_keywords = input("Enter seed keywords (separated by ','): ").split(",")

    print("Seeds: ")
    for seed in seed_keywords:
        cleaned_seed = seed.strip()
        print(f"\t{cleaned_seed}")

    confirm_input = input("Confirm selection (Y / N): ").upper()
    if confirm_input == "N":
        get_seed_keywords()
        return

    return seed_keywords


def get_search_type():
    search_type_input = input("What type of search? (1. Full, 2. Questions): ")

    if search_type_input != "1" and search_type_input != "2":
        print(f"Error: Input '{search_type_input}' not an option.")
        get_search_type()
        return

    search_types = {1: "phrase_fullsearch", 2: "phrase_questions"}
    return search_types[int(search_type_input)]


def get_display_limit():
    display_limit_input = str(input("Enter maximum row limit: "))
    if display_limit_input.isdigit():
        if int(display_limit_input) > 0:
            return int(display_limit_input)

    print("Input must be an integer greater than 0")
    get_display_limit()


def get_keyword_exclusions():
    keyword_exclusions_raw = (
        input("Enter keywords to exclude (separated by ','): ")
        .replace(", ", ",")
        .split(",")
    )
    keyword_exclusions_parsed = f"%2D%7CPh%7CCo%7C"

    for kw_exclusion in keyword_exclusions_raw:
        keyword_exclusions_parsed += kw_exclusion

    return keyword_exclusions_parsed

    # | %7C
    # %2D | Ph | Co | <values>
    # display_filter - sign | field | operation | value1;value2
    # Co (containing) - Operation


def get_keywords_from_seeds(seeds, search_type, keyword_exclusions=None):
    keywords = []

    for kw in seeds:
        df = get_keywords(
            kw,
            limit=20,
            report_type=(
                "phrase_fullsearch" if search_type == 1 else "phrase_questions"
            ),
            # keyword_exclusions=f"%2B%7CPh%7CCo%7C[{kw}]{keyword_exclusions}",
        )
        df["seed"] = kw
        # df.loc[df["Intent"] == 0, "Intent"] = "commercial"
        # df.loc[df["Intent"] == 1, "Intent"] = "informational"
        # df.loc[df["Intent"] == 3, "Intent"] = "transactional"
        keywords.append(df)

    return keywords


def get_keywords(
    phrase: str, limit=1, report_type="phrase_fullsearch", display_filter=""
):
    params = {
        "type": report_type,
        "key": os.getenv("API_KEY"),
        "phrase": phrase,
        "database": "us",
        "export_columns": "Ph,In,Nq",
        "display_limit": limit,
        "display_filter": display_filter,
    }

    response = requests.get(base_url + "?", params)
    response.raise_for_status()
    return pd.read_csv(io.StringIO(response.text), sep=";")


def clean_data():
    print("called")


def export_keywords(df):
    keywords = pd.concat(df, ignore_index=True)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    keywords.to_csv(f"output_{timestamp}.csv")


def main(keywords=[]):
    seed_keywords = get_seed_keywords()
    search_type = get_search_type()
    limit = get_display_limit()

    api_unit_consumption = 0
    if search_type == "phrase_fullsearch":
        api_unit_consumption = len(seed_keywords) * limit * 20
    elif search_type == "phrase_questions":
        api_unit_consumption = len(seed_keywords) * limit * 40
    confirm_request_input = input(
        f"Max API unit consumption is estimated at {api_unit_consumption}. Proceed? (Y / N): "
    ).upper()
    if confirm_request_input == "N":
        main()
        return

    # keyword_exclusions = get_keyword_exclusions()

    keywords = get_keywords_from_seeds(seed_keywords, search_type)

    search_again_input = input(
        "Would you like to perform another search? (Y / N): "
    ).upper()
    if search_again_input == "Y":
        main(keywords)
        return

    export_keywords(keywords)


if __name__ == "__main__":
    main()
