# pytesseract doesn't have type hints, so we ignore it
import pytesseract as ocr  # type: ignore
import numpy as np
import cv2
import time
import os

from PIL import Image

IMAGE_FOLDER = "images"
WHITESPACES = [" ", "\n", "\t"]
ALLOWED_FILE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".bmp", ".gif")
LANGUAGE = "eng"


def get_image_from_folder(image_category: str) -> list[str]:
    folder = f"{IMAGE_FOLDER}/{image_category}"
    images: list[str] = []
    if not os.path.exists(folder):
        return images
    for filename in os.listdir(folder):
        if filename.lower().endswith(ALLOWED_FILE_EXTENSIONS):
            images.append(os.path.join(folder, filename))
    return images


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


def open_image_as_rgb(image_path: str) -> Image.Image:
    with Image.open(image_path) as image:
        image_in_memory = image.copy()
        if image.mode != "RGB":
            return image_in_memory.convert("RGB")
        return image_in_memory


def enhance_image(image_name: str) -> Image.Image:
    image = open_image_as_rgb(image_name)
    np_image = np.asarray(image).astype(np.uint8)
    np_image[:, :, 0] = 0
    np_image[:, :, 2] = 0
    im = cv2.cvtColor(np_image, cv2.COLOR_RGB2GRAY)
    _, thresh = cv2.threshold(im, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    bin_image = Image.fromarray(thresh)
    return bin_image


def remove_whitespace(input_text: str) -> str:
    for whitespace_character in WHITESPACES:
        if whitespace_character in input_text:
            input_text = input_text.replace(whitespace_character, "")
    return input_text


def main() -> None:
    start_time = time.time()
    print(f"enter the sub_folder name in '{IMAGE_FOLDER}' folder:")
    sub_folder = input()
    print("how many images to read?")
    user_input = input()
    try:
        quantity = int(user_input)
        images = get_image_from_folder(sub_folder)[:quantity]
    except ValueError:
        images = get_image_from_folder(sub_folder)
    for image_name in images:
        print(f"\n{image_name}")
        image = enhance_image(image_name)
        phrase = ocr.image_to_string(image, lang=LANGUAGE)
        if not isinstance(phrase, str):
            continue
        formatted_phrase = remove_whitespace(phrase)
        print(f"{len(formatted_phrase)}\n")
        print(formatted_phrase)
    final_time = time.time()
    print_elapsed_time(final_time - start_time)


if __name__ == "__main__":
    main()
