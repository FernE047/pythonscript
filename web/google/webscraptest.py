import requests
import bs4
import re

AVAILABLE_CHARS = list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")
GOOGLE_URL = "https://www.google.com.br/search?q="


def get_search_result_count(search_query: str) -> int:
    url = f"{GOOGLE_URL}{search_query}"
    response = requests.get(url)
    while response.status_code != requests.codes.ok:
        response = requests.get(url)
    google_soup = bs4.BeautifulSoup(response.text, features="html.parser")
    tags = google_soup.select("#resultStats")
    result_count_regex = re.compile(r"\d{1,3}")
    result_stats_text = tags[0].getText()
    if result_stats_text:
        result_count_text = result_count_regex.findall(result_stats_text)
        return int("".join(result_count_text))
    return 0


def find_zero_term(term: str, level: int = 0, current_level: int = 0) -> str | None:
    for char in AVAILABLE_CHARS:
        term += char
        print(term)
        if current_level < level:
            current_level += 1
            recursive_result = find_zero_term(term, level, current_level)
            if recursive_result is not None:
                return recursive_result
        result_count = get_search_result_count(term)
        print(f"result count : {result_count}")
        if result_count == 0:
            return term
        term = term[:-1]
    return None


def search(search_term: str) -> str:
    level = 0
    final_search_term = find_zero_term(search_term, level, 0)
    while final_search_term is None:
        level += 1
        final_search_term = find_zero_term(search_term, level, 0)
    return final_search_term


def main() -> None:
    print("enter the search query : ")
    initial_term = input()
    search_results = search(initial_term)
    print(f"\n\nresults :\n{search_results}")


if __name__ == "__main__":
    main()
