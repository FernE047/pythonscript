# pytesseract doesn't have type hints, so we ignore it
import pytesseract as ocr  # type: ignore
import time
from PIL import Image
from pathlib import Path

IMAGE_PATH = Path("jap") / "1.png"
LANGUAGE = "jp"


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


def open_image_as_rgba(image_path: Path) -> Image.Image:
    with Image.open(image_path) as image:
        image_in_memory = image.copy()
        if image.mode != "RGBA":
            return image_in_memory.convert("RGBA")
        return image_in_memory


def main() -> None:
    start_time = time.time()
    print(f"\n{IMAGE_PATH}")
    image = open_image_as_rgba(IMAGE_PATH)
    phrase = ocr.image_to_string(image, lang=LANGUAGE)
    print(phrase)
    final_time = time.time()
    print_elapsed_time(final_time - start_time)


if __name__ == "__main__":
    main()
