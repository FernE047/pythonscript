# pytesseract doesn't have type hints, so we ignore it
from pathlib import Path

import pytesseract as ocr  # type: ignore
from PIL import Image
import time

WHITESPACES = (" ", "\n", "\t")
BRIGHTNESS = 255
MAX_BRIGHTNESS = BRIGHTNESS * 3
HIGHLIGHT_COLOR = (0, 0, 0)
BACKGROUND_COLOR = (255, 255, 255)
IMAGE_FOLDER = Path("images")
OUTPUT_FILE = Path("output.txt")
THRESHOLD_DEFAULT = 20
LANGUAGE = "por"

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
    for whitespace in WHITESPACES:
        if whitespace in raw_text:
            raw_text = raw_text.replace(whitespace, "")
    return raw_text


def open_image_as_rgb(image_path: Path) -> Image.Image:
    with Image.open(image_path) as image:
        image_in_memory = image.copy()
        if image.mode != "RGB":
            return image_in_memory.convert("RGB")
        return image_in_memory


def apply_threshold(image_path: Path, threshold: int) -> Image.Image:
    image = open_image_as_rgb(image_path)
    width, height = image.size
    thresholded_image = image.copy()
    threshold_value = MAX_BRIGHTNESS - threshold
    for x in range(width):
        for y in range(height):
            pixel = image.getpixel((x, y))
            if not isinstance(pixel, tuple) or len(pixel) < 3:
                continue
            pixel_sum = sum(pixel[:3])
            if pixel_sum >= threshold_value:
                thresholded_image.putpixel((x, y), HIGHLIGHT_COLOR)
            else:
                thresholded_image.putpixel((x, y), BACKGROUND_COLOR)
    return thresholded_image


def main() -> None:
    start_time = time.time()
    end_time = time.time()
    instructions = ""
    for image_path in IMAGE_FOLDER.iterdir():
        print(f"\n{image_path}")
        processing_start_time = time.time()
        better_image = apply_threshold(image_path, THRESHOLD_DEFAULT)
        phrase = ocr.image_to_string(better_image, lang=LANGUAGE)
        if not isinstance(phrase, str):
            continue
        formatted_phrase = remove_whitespace(phrase)
        end_processing_time = time.time()
        print(f"{len(formatted_phrase)}")
        print("procesamento: ")
        print_elapsed_time(end_processing_time - processing_start_time)
        print(formatted_phrase)
        instructions += f"{formatted_phrase}\n\n"
    with open(OUTPUT_FILE, "w", encoding="utf-8") as output_file:
        output_file.write(instructions)
    end_time = time.time()
    print("demorou ")
    print_elapsed_time(end_time - start_time)


if __name__ == "__main__":
    main()
