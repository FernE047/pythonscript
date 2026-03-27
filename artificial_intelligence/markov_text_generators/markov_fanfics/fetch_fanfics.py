from pathlib import Path
from typing import cast
import requests
import bs4
import time

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
FANFIC_URL = "https://www.spiritfanfiction.com/categorias/"
MAX_PAGES = 100
STORIES_PER_PAGE = 10
TITLE_PREFIX = "Fanfic "
STORIES_FOLDER = Path("stories")
STORIES_FOLDER.mkdir(exist_ok=True)
TITLE_PREFIX_LENGTH = 20
SLEEP_BETWEEN_PAGES = 10
TITLE_SEPARATOR = " : "
NOT_ALLOWED_CHARS = ("\n", "\r", TITLE_SEPARATOR)


def sanitize_input(text: str) -> str:
    for char in NOT_ALLOWED_CHARS:
        text = text.replace(char, " ")
    while text.find("  ") != -1:
        text = text.replace("  ", " ")
    return text.strip()


def connect(url: str) -> requests.Response:
    response = requests.get(url)
    while response.status_code != requests.codes.ok:
        response = requests.get(url)
    return response

def fetch_page(url:str, page_number: int) -> None:
    response = connect(f"{url}{page_number}")
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
        stories_amount = len(list(STORIES_FOLDER.iterdir()))
        with open(STORIES_FOLDER / f"fanfic{stories_amount:04d}.txt", "w") as file:
            try:
                file.write(f"{titles[index]}{TITLE_SEPARATOR}{summary[index]}")
                print(f"{titles[index]}\n")
            except IndexError as _:
                pass
    time.sleep(SLEEP_BETWEEN_PAGES)

def fetch_category(category: str) -> None:
    url = f"{FANFIC_URL}{category}?pagina="
    for page_number in range(1, MAX_PAGES + 1):
        print(f"Fetching page {page_number} of category {category}...")
        fetch_page(url, page_number)


def fetch_and_save_fanfics() -> None:
    for category in FANFIC_CATEGORIES:
        fetch_category(category)

if __name__ == "__main__":
    fetch_and_save_fanfics()
