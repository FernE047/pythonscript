import requests
import bs4
import random

# google changed way too much, this script is not working anymore

def get_response_from_site(url: str) -> requests.Response:
    response = requests.get(url)
    while response.status_code != requests.codes.ok:
        response = requests.get(url)
    return response


def search_google(query: str, adicao: str) -> bs4.ResultSet[bs4.element.Tag]:
    google_search = get_response_from_site(
        f"https://www.google.com.br/search?q={query}{adicao}"
    )
    google_search_soup = bs4.BeautifulSoup(google_search.text, features="html.parser")
    results = google_search_soup.select(".r")
    return results


def tamanho_para_titulo():
    population = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 17]
    weight = [1, 1, 6, 16, 35, 63, 49, 33, 30, 28, 39, 37, 30, 15, 5, 1]
    return random.choices(population, weights=weight)[0]


def procura_texto_em_lista(word: str, list_str: list[str]) -> int:
    try:
        return list_str.index(word)
    except ValueError:
        return -1


def main() -> None:
    while True:
        print("\n\nenter a term to search for fanfics in fanfiction.com.br\n")
        term = input().lower()
        title_size = tamanho_para_titulo()
        print(f"title size : {title_size} words")
        results = search_google(term, "+site%3A%2Ffanfiction.com.br%2F")
        title: list[str] = [term]
        titles: list[str] = []
        while len(title) <= title_size:
            for info in results:
                result_title_tag = info.select(".LC20lb")
                if result_title_tag:
                    result_title = result_title_tag[0].get_text().lower()
                    text_index = procura_texto_em_lista(term, result_title.split())
                    del text_index  # only to stop lint complains
                    titles += [result_title]
        print("\ntitulo\n")


if __name__ == "__main__":
    main()
