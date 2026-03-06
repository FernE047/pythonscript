# pytesseract doesn't have type hints, so we ignore it
import pytesseract as ocr  # type: ignore
from pathlib import Path
import time

from PIL import Image

IMAGE_FOLDER = Path("images")
WHITESPACES = [" ", "\n", "\t"]



def print_elapsed_time(seconds: float) -> None:
    if seconds < 0:
        seconds = -seconds
        sign = "-"
    else:
        sign = ""
    total_ms = int(round(seconds * 1000))
    ms = total_ms % 1000
    total_s = total_ms // 1000
    s = total_s % 60
    total_min = total_s // 60
    m = total_min % 60
    total_h = total_min // 60
    h = total_h % 24
    d = total_h // 24
    parts: list[str] = []

    def add(value: int, singular: str, plural: str) -> None:
        if value:
            parts.append(f"{value} {singular if value == 1 else plural}")

    add(d, "day", "days")
    add(h, "hour", "hours")
    add(m, "minute", "minutes")
    add(s, "second", "seconds")
    if ms or not parts:
        parts.append(f"{ms} millisecond" if ms == 1 else f"{ms} milliseconds")
    print(f"{sign}{', '.join(parts)}")


def remove_whitespace(raw_text: str) -> str:
    for whitespace_char in WHITESPACES:
        if whitespace_char in raw_text:
            raw_text = raw_text.replace(whitespace_char, "")
    return raw_text


def open_image(image_path: Path) -> Image.Image:
    with Image.open(image_path) as image:
        image_in_memory = image.copy()
        return image_in_memory


def main() -> None:
    start_time = time.time()
    for image_path in IMAGE_FOLDER.iterdir():
        print(f"\n{image_path}")
        phrase = ocr.image_to_string(open_image(image_path), lang="por")
        if not isinstance(phrase, str):
            continue
        formatted_phrase = remove_whitespace(phrase)
        print(f"{len(phrase)}")
        print(f"{len(formatted_phrase)}\n")
        print(formatted_phrase)
    final_time = time.time()
    print_elapsed_time(final_time - start_time)



if __name__ == "__main__":
    main()