from typing import Literal
from urllib.parse import quote, urlparse
from PIL import Image
import requests
import bs4
import os

RED = (255, 0, 0, 255)
BLACK = (0, 0, 0, 255)


def filter_site_name(url: str) -> str:
    parsed = urlparse(url if "://" in url else f"https://{url}")
    host = parsed.netloc or parsed.path
    if host.startswith("www."):
        host = host[4:]
    return host.split(".")[0]


def remove_extra_spaces(text: str) -> str:
    while text.find("  ") != -1:
        text = text.replace("  ", " ")
    return text.lower().strip()


def clean_soup(soup: bs4.ResultSet[bs4.element.Tag]) -> str:
    allowed_chars = (
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 éáíóúãàêÉÀç"
    )
    allowed = set(list(allowed_chars))
    raw = " ".join(tag.get_text(" ", strip=False) for tag in soup)
    filtered_text = "".join(ch for ch in raw if ch in allowed or ch.isspace())
    return remove_extra_spaces(filtered_text)


def fetch_website(site: str) -> requests.Response:
    response = requests.get(site)
    while response.status_code != requests.codes.ok:
        response = requests.get(site)
    return response


def google_search(
    search: str, adicao: str = "%20full%20lyrics"
) -> bs4.ResultSet[bs4.element.Tag]:
    response = fetch_website(f"https://www.google.com.br/search?q={search}{adicao}")
    response_soup = bs4.BeautifulSoup(response.text, features="html.parser")
    search_results = response_soup.select(".r")
    return search_results


def get_site_type(site: str) -> Literal["artist", "album"] | None:
    if site.find("/artists/") != -1:
        return "artist"
    if site.find("/albums/") != -1:
        return "album"
    return None


def find_genius_url(
    search_results: bs4.ResultSet[bs4.element.Tag],
    search_word: Literal["artist", "album"] = "album",
) -> str:
    for search_result in search_results:
        anchor_list = search_result.select("a")
        if len(anchor_list) == 0:
            continue
        anchor = anchor_list[0]
        href_result = anchor.get("href")
        if not isinstance(href_result, str):
            continue
        site = filter_site_name(href_result)
        print(site)
        if site != "genius":
            continue
        if search_word != "album":
            return href_result
        criteria_match = get_site_type(site)
        if criteria_match is None:
            continue
        if criteria_match == search_word:
            return href_result
    return ""


def get_specific_tag(url: str, tag_descriptor: str) -> bs4.ResultSet[bs4.element.Tag]:
    response = fetch_website(url)
    parsed_html = bs4.BeautifulSoup(response.text, features="html.parser")
    tag_elements = parsed_html.select(tag_descriptor)
    return tag_elements

def generate_lyrics_image(url:str, output_path:str="imagens/") -> None:
    title_tag = get_specific_tag(url, ".header_with_cover_art-primary_info-title")
    track_title = clean_soup(title_tag)
    print(f"{track_title}\n")
    lyrics_tags = get_specific_tag(url, ".lyrics")
    lyrics = clean_soup(lyrics_tags)
    print(f"{lyrics}\n")
    words = lyrics.split(" ")
    word_count = len(words)
    if word_count == 0:
        print("No lyrics found\n")
        return
    print(f"Word count: {word_count}\n")
    image = Image.new("RGBA", (word_count, word_count), BLACK)
    for x in range(word_count):
        for y in range(word_count):
            if words[x] == words[y]:
                image.putpixel((x, y), RED)
    filename = f"./{output_path}{track_title}.png"
    image.save(filename)
    print(f"Successfully created {filename}\n\n")


def fetch_all_genius_urls(result_set: bs4.ResultSet[bs4.element.Tag]) -> list[str]:
    genius_urls: list[str] = []
    for html_element in result_set:
        anchors = html_element.select("a")
        if len(anchors) == 0:
            continue
        anchor = anchors[0]
        href_result = anchor.get("href")
        if not isinstance(href_result, str):
            continue
        site = filter_site_name(href_result)
        if site == "genius":
            genius_urls.append(href_result)
    return genius_urls


def generate_album_images(url: str, album: str) -> None:
    create_directory(f"album/{album}")
    track_number = 1
    site_tags = get_specific_tag(url, ".u-display_block")
    lyrics_urls = fetch_all_genius_urls(site_tags)
    for url in lyrics_urls:
        generate_lyrics_image(url, output_path=f"album/{album}/{track_number:03d}-")
        track_number += 1


def generate_artist_images(url: str, artist: str) -> None:
    create_directory(f"artist/{artist}")
    track_number = 1
    site_tags = get_specific_tag(url, ".mini_card")
    lyrics_urls = fetch_all_genius_urls(site_tags)
    for url in lyrics_urls:
        generate_lyrics_image(url, output_path=f"artist/{artist}/{track_number:03d}-")
        track_number += 1


def create_directory(directory_path: str) -> None:
    directory_path = f"./{directory_path}"
    os.mkdir(directory_path)


def get_artist_from_album(url: str) -> str | None:
    album_site = fetch_website(url)
    album_soup = bs4.BeautifulSoup(album_site.text, features="html.parser")
    artist_data = album_soup.select(
        ".header_with_cover_art-primary_info-primary_artist"
    )
    if len(artist_data) == 0:
        return None
    tag = artist_data[0]
    href_result = tag.get("href")
    if not isinstance(href_result, str):
        return None
    return href_result


def main() -> None:
    album = False
    artist = False
    while True:
        print(
            "\nenter the music/album/artist (prefix with 'album ' or 'artist ', no prefix for music) or 0 to exit:"
        )
        user_input = input()
        if user_input == "0":
            return
        search_term = user_input.lower()
        if search_term[:5] == "album":
            search_term = search_term[6:]
            album = True
        if search_term[:6] == "artist":
            search_term = search_term[7:]
            artist = True
        encoded_search = quote(search_term)
        if album:
            search_results = google_search(
                encoded_search, adicao="%20albums+site%3Ahttps%3A%2F%2Fgenius.com%2F"
            )
            url = find_genius_url(search_results, search_word="album")
            generate_album_images(url, search_term)
        elif artist:
            search_results = google_search(
                encoded_search, adicao="%20artist+site%3Ahttps%3A%2F%2Fgenius.com%2F"
            )
            url = find_genius_url(search_results, search_word="artist")
            if get_site_type(url) != "artist":
                url_test = get_artist_from_album(url)
                if url_test is None:
                    print("Artist not found, proceeding with original URL.")
                else:
                    url = url_test
            generate_artist_images(url, search_term)
        else:
            search_results = google_search(
                encoded_search, adicao="+site%3Ahttps%3A%2F%2Fgenius.com%2F"
            )
            url = find_genius_url(search_results)
            generate_lyrics_image(url)


if __name__ == "__main__":
    main()
