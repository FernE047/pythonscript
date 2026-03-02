import requests
import bs4
import re
import time

# this script is based on a game I used to play. The idea is to find the longest search term that has more results than the previous one. For example, if you start with "a", it will check "a ", "aA", "aB", ..., "aZ", "aa", "ab", ..., and so on, until it finds a term that has fewer results than the previous one. Then it will return the longest term found.


def connect(url: str) -> requests.Response:
    response = requests.get(url)
    while response.status_code != requests.codes.ok:
        response = requests.get(url)
    return response


def fetch_site_data(url: str, css_selector: str) -> bs4.ResultSet[bs4.element.Tag]:
    response = connect(url)
    site_soup = bs4.BeautifulSoup(response.text, features="html.parser")
    tags = site_soup.select(css_selector)
    return tags


def get_search_results_count(search_query: str) -> int:
    fetched_data = fetch_site_data(
        f"https://www.google.com.br/search?q={search_query}", "#resultStats"
    )
    result_count_regex = re.compile(r"\d{1,3}")
    raw_result_text = fetched_data[0].getText()
    if raw_result_text:
        result_count_matches = result_count_regex.findall(raw_result_text)
        return int("".join(result_count_matches))
    return 0


def find_longest_term(search_term: str, current_longest_count: int = 0) -> None:
    possible_search_chars = list(
        " ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    )
    search_results_count: list[int] = []
    max_results_index = 0
    for char in possible_search_chars:
        search_results_count.append(0)
    for char_index, char in enumerate(possible_search_chars):
        search_chars = list(search_term)
        search_chars.append(char)
        search_term = str("".join(search_chars))
        print(f"Searching for '{search_term}'...")
        result_count = get_search_results_count(search_term)
        print(f"{result_count} results")
        search_results_count[char_index] = result_count
        if result_count >= search_results_count[max_results_index]:
            max_results_index = char_index
        search_chars = list(search_term)
        del search_chars[(len(search_chars) - 1)]
        search_term = "".join(search_chars)
    if search_results_count[max_results_index] <= current_longest_count:
        print(f"\n\n The Term {search_term} has {current_longest_count} results")
        return
    search_chars = list(search_term)
    search_chars.append(possible_search_chars[max_results_index])
    search_term = str("".join(search_chars))
    find_longest_term(search_term, search_results_count[max_results_index])


def main() -> None:
    print("enter the initial term:")
    initial_term = input()
    start_time = time.time()
    find_longest_term(initial_term)
    end_time = time.time()
    real_time = end_time - start_time
    print(f"it took {real_time} seconds")


if __name__ == "__main__":
    main()
