from pathlib import Path
from PIL import Image

# pytesseract doesn't have type hints, so we ignore it
import pytesseract as ocr  # type: ignore
import time

MENU_COLOR = (100, 191, 96)
MENU_BOX = (34, 909, 671, 1072)
INPUT_PATH = Path("jap") / "1.png"
CROPPED_IMAGE_PATH = Path("image_cropped.png")


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


def open_image(image_path: Path) -> Image.Image:
    with Image.open(image_path) as image:
        image_in_memory = image.copy()
        return image_in_memory


def find_pixel_coordinates(path: Path) -> None:
    image = open_image(path)
    larg, alt = image.size
    for x in range(larg):
        for y in range(alt):
            pixel = image.getpixel((x, y))
            if pixel == MENU_COLOR:
                print((x, y))


def main() -> None:
    start_time = time.time()
    print(f"\n{INPUT_PATH}")
    image = open_image(INPUT_PATH)
    image_crop = image.crop(MENU_BOX)
    image_crop.save(CROPPED_IMAGE_PATH)
    phrase = ocr.image_to_string(image_crop, lang="jp")
    print(phrase)
    final_time = time.time()
    print("it took ")
    print_elapsed_time(final_time - start_time)


if __name__ == "__main__":
    main()
