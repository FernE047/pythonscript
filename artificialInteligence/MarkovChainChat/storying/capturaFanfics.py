from typing import cast
import requests
import bs4
import time
import os

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


fanfic_categories = [
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
for category in fanfic_categories:
    url = f"https://www.spiritfanfiction.com/categorias/{category}?pagina="
    for pagina in range(1, 101):
        response = connect(f"{url}{pagina}")
        parsed_html = bs4.BeautifulSoup(response.text, features="html.parser")
        summary_tags = parsed_html.select(".limit_height")
        summary = [sanitize_input(summary_tag.getText()) for summary_tag in summary_tags]
        links = parsed_html.select(".link")
        titles:list[str] = []
        for link in links:
            title_tag = link.get("title")
            if title_tag is None:
                continue
            title = cast(str, title_tag)
            if title.find("Fanfic ") != -1:
                titles.append(title[20:])
        for index in range(10):
            stories_amount = len(os.listdir("stories"))
            with open(f"stories/fanfic{stories_amount:04d}.txt", "w") as file:
                try:
                    file.write(f"{titles[index]} : {summary[index]}")
                    print(titles[index], end="\n\n")
                except IndexError as _:
                    pass
        time.sleep(10)
