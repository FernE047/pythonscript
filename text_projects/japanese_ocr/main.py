from pathlib import Path
from PIL import Image

# pytesseract doesn't have type hints, so we ignore it
import pytesseract as ocr  # type: ignore
import time
from datetime import timedelta

MENU_COLOR = (100, 191, 96)
MENU_BOX = (34, 909, 671, 1072)
INPUT_PATH = Path("jap") / "1.png"
CROPPED_IMAGE_PATH = Path("image_cropped.png")


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
    elapsed_time_str = str(timedelta(seconds=final_time - start_time))
    print(f"Elapsed time: {elapsed_time_str}")


if __name__ == "__main__":
    main()
