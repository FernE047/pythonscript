import requests
import bs4
import re
import time

# this script is based on a game I used to play. The idea is to find the lowest search term that has 0 results. For example, if you start with "a", it will check "a ", "aA", "aB", ..., "aZ", "aa", "ab", ..., and so on, until it finds a term that has 0 results. Then it will return the lowest term found.

GOOGLE_URL = "https://www.google.com.br/search?q="
RESULTS_TAG = "#resultStats"
POSSIBLE_CHARS = tuple("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")


def connect(url: str) -> requests.Response:
    response = requests.get(url)
    while response.status_code != requests.codes.ok:
        response = requests.get(url)
    return response


def fetch_site_data(url: str) -> bs4.ResultSet[bs4.element.Tag]:
    response = connect(url)
    site_soup = bs4.BeautifulSoup(response.text, features="html.parser")
    tags = site_soup.select(RESULTS_TAG)
    return tags


def get_search_results_count(search_query: str) -> int:
    fetched_data = fetch_site_data(f"{GOOGLE_URL}{search_query}")
    result_count_regex = re.compile(r"\d{1,3}")
    raw_result_text = fetched_data[0].getText()
    if raw_result_text:
        result_count_matches = result_count_regex.findall(raw_result_text)
        return int("".join(result_count_matches))
    return 0


def fetch_google_results(search: str) -> bs4.ResultSet[bs4.element.Tag]:
    response = connect(f"{GOOGLE_URL}{search}")
    results = bs4.BeautifulSoup(response.text, features="html.parser")
    search_results = results.select(".r")
    return search_results


def find_zero_search(search_term: str) -> None:
    result_counts: list[int] = []
    lowest_count_index = 0
    for char in POSSIBLE_CHARS:
        result_counts.append(0)
    for char_index, char in enumerate(POSSIBLE_CHARS):
        search_chars = list(search_term)
        search_chars.append(char)
        search_term = str("".join(search_chars))
        print(search_term)
        results_count = get_search_results_count(search_term)
        if results_count == 0:
            print(f"\n\n The Term {search_term} has 0 results")
            return 
        if results_count == 1:
            urls = fetch_google_results(search_term)
            for url in urls:
                print(url)
        result_counts[char_index] = results_count
        if results_count <= result_counts[lowest_count_index]:
            lowest_count_index = char_index
        search_chars = list(search_term)
        del search_chars[(len(search_chars) - 1)]
        search_term = "".join(search_chars)
    search_chars = list(search_term)
    search_chars.append(POSSIBLE_CHARS[lowest_count_index])
    search_term = str("".join(search_chars))
    return find_zero_search(search_term)


def main() -> None:
    print("enter the initial term:")
    initial_term = input()
    start_time = time.time()
    find_zero_search(initial_term)
    end_time = time.time()
    real_time = end_time - start_time
    print(f"it took {real_time} seconds")


if __name__ == "__main__":
    main()
