from pathlib import Path


HTML_FILE = Path("mimimidias - Youtube.html")
OUTPUT_FILE = Path("mimimidiasLINK.txt")
NOT_ALLOWED_CHARS = (" ", "\n", "\t", '"')
END_TITLE = '"'
TITLE_TAG = "title="
HREF_TAG = "href="

def read_char(html_content: list[str]) -> str:
    return html_content.pop(0)


def read_word(html_content: list[str]) -> str:
    word = ""
    char = read_char(html_content)
    while char not in NOT_ALLOWED_CHARS:
        word += char
        char = read_char(html_content)
    return word


def find_next_occurrence(html_content: list[str], search_term: str) -> None:
    current_word = read_word(html_content)
    while current_word != search_term:
        current_word = read_word(html_content)


def extract_title(html_content: list[str]) -> str:
    title = ""
    char = read_char(html_content)
    while (char) and (char != END_TITLE):
        title += char
        char = read_char(html_content)
    return title


def main() -> None:
    with open(HTML_FILE, "r", encoding="utf8") as html_file:
        html_content = list(html_file.read())
    titles: list[str] = []
    while True:
        try:
            find_next_occurrence(html_content, TITLE_TAG)
            find_next_occurrence(html_content, HREF_TAG)
            title = extract_title(html_content)
            print(title)
            titles.append(title)
        except Exception:
            break
    with open(OUTPUT_FILE, "w", encoding="utf8") as title_file:
        title_file.write("\n".join(titles))


if __name__ == "__main__":
    main()
