from typing import cast
import requests
import bs4
import time
import os

FANFIC_CATEGORIES = [
    "naruto",
    "boku-no-hero-academia-my-hero-academia",
    "fairy-tail",
    "shingeki-no-kyojin-attack-on-titan",
    "haikyuu",
    "outros",
    "one-piece",
    "saint-seiya",
    "pokemon",
    "dragon-ball",
    "demon-slayer-kimetsu-no-yaiba",
    "the-seven-deadly-sins-nanatsu-no-taizai",
    "death-note",
    "jojo-no-kimyou-na-bouken-jojos-bizarre-adventure",
    "jujutsu-kaisen",
    "kuroko-no-basuke",
    "hunter-x-hunter",
    "tokyo-ghoul",
    "yuri-on-ice",
    "yakusoku-no-neverland-the-promised-neverland",
    "high-school-dxd",
    "sword-art-online",
]
MAX_PAGES = 100
STORIES_PER_PAGE = 10
TITLE_PREFIX = "Fanfic "
TITLE_PREFIX_LENGTH = 20
SLEEP_BETWEEN_PAGES = 10


def sanitize_input(text: str) -> str:
    text = text.replace("\n", " ")
    text = text.replace("\r", " ")
    while text.find("  ") != -1:
        text = text.replace("  ", " ")
    return text.strip()


def connect(url: str) -> requests.Response:
    response = requests.get(url)
    while response.status_code != requests.codes.ok:
        response = requests.get(url)
    return response


def main() -> None:
    for category in FANFIC_CATEGORIES:
        url = f"https://www.spiritfanfiction.com/categorias/{category}?pagina="
        for pagina in range(1, MAX_PAGES + 1):
            response = connect(f"{url}{pagina}")
            parsed_html = bs4.BeautifulSoup(response.text, features="html.parser")
            summary_tags = parsed_html.select(".limit_height")
            summary = [
                sanitize_input(summary_tag.getText()) for summary_tag in summary_tags
            ]
            links = parsed_html.select(".link")
            titles: list[str] = []
            for link in links:
                title_tag = link.get("title")
                if title_tag is None:
                    continue
                title = cast(str, title_tag)
                if title.find(TITLE_PREFIX) != -1:
                    titles.append(title[TITLE_PREFIX_LENGTH:])
            for index in range(STORIES_PER_PAGE):
                stories_amount = len(os.listdir("stories"))
                with open(f"stories/fanfic{stories_amount:04d}.txt", "w") as file:
                    try:
                        file.write(f"{titles[index]} : {summary[index]}")
                        print(f"{titles[index]}\n")
                    except IndexError as _:
                        pass
            time.sleep(SLEEP_BETWEEN_PAGES)


if __name__ == "__main__":
    main()
