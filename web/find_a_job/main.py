from typing import Literal, TypedDict, cast, overload
import webbrowser

from bs4 import ResultSet
from bs4.element import Tag

MAX_PAGE = 10


class jobListingData(TypedDict):
    title: str
    site: str
    description: str


@overload
def choose_from_options(
    prompt: str, options: list[str], mode: Literal["text"]
) -> str: ...


@overload
def choose_from_options(
    prompt: str, options: list[str], mode: Literal["number"]
) -> int: ...


def choose_from_options(
    prompt: str, options: list[str], mode: Literal["text", "number"] = "text"
) -> str | int:
    while True:
        for index, option in enumerate(options):
            print(f"{index} - {option}")
        user_choice = input(prompt)
        try:
            if mode == "number":
                return int(user_choice)
            else:
                return options[int(user_choice)]
        except (ValueError, IndexError):
            user_choice = input("not valid, try again: ")


def get_tag_site(url: str, css_selector: str) -> ResultSet[Tag]:
    import requests
    import bs4

    response = requests.get(url)
    response.raise_for_status()
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    information = soup.select(css_selector)
    return information


def filter_job_listing(information: ResultSet[Tag]) -> list[jobListingData]:
    job_listings: list[jobListingData] = []
    for info in information:
        if not info.select(".descricao-vaga"):
            continue
        title = cast(str, info.get("title", ""))
        site = cast(str, info.get("href", ""))
        description = ""
        description_tag = info.find("p")
        if description_tag:
            description = description_tag.get_text(strip=True)
        job_listings.append({"title": title, "site": site, "description": description})
    return job_listings


def is_keywords_in_job(
    job: jobListingData,
    search_terms: list[str],
    keys: list[Literal["title", "description"]],
) -> bool:
    for term in search_terms:
        term = term.lower()
        for key in keys:
            text = job[key].lower()
            words = text.split(" ")
            if term in words:
                return True
    return False


def refine_job_results(
    jobs: list[jobListingData],
    search_terms: list[str],
    keys: list[Literal["title", "description"]],
) -> list[jobListingData]:
    refined_jobs: list[jobListingData] = []
    for job in jobs:
        if is_keywords_in_job(job, search_terms, keys):
            refined_jobs.append(job)
    return refined_jobs


def main() -> None:
    sites = [
        "http://empregacampinas.com.br/page/{}/?s=est%C3%A1gio",
        "http://empregacampinas.com.br/categoria/vaga/page/{}/",
    ]
    choice = choose_from_options("", ["estágio", "emprego", "tudo"], mode="number")
    if choice < 2:
        sites = [sites[choice]]
    search_locations = ["Campinas", "Sumaré", "Sumare"]
    search_keywords = [
        "e-commerce",
        "TI",
        "tecnologia",
        "programador",
        "programadores",
        "Web",
    ]
    browser = webbrowser.get(
        "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"
    )
    final_job_listings: list[jobListingData] = []
    for site in sites:
        for page in range(1, MAX_PAGE + 1):
            information = get_tag_site(site.format(page), ".thumbnail")
            vagasDisponiveis = filter_job_listing(information)
            if search_locations:
                vagasDisponiveis = refine_job_results(
                    vagasDisponiveis, search_locations, ["title"]
                )
            if search_keywords:
                vagasDisponiveis = refine_job_results(
                    vagasDisponiveis, search_keywords, ["title", "description"]
                )
            final_job_listings.extend(vagasDisponiveis)
    while True:
        options = [job["title"] for job in final_job_listings]
        choice = choose_from_options(
            "choose : ", options + ["all", "exit"], mode="number"
        )
        if choice < len(options):
            browser.open(final_job_listings[choice]["site"])
            final_job_listings.pop(choice)
            continue
        choice -= len(options)
        if choice != 0:
            return
        for job in final_job_listings:
            browser.open(job["site"])


if __name__ == "__main__":
    main()
