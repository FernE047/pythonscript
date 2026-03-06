# pytesseract doesn't have type hints, so we ignore it
import pytesseract as ocr  # type: ignore
import time
from PIL import Image
from pathlib import Path
from datetime import timedelta

IMAGE_PATH = Path("jap") / "1.png"
LANGUAGE = "jp"


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
    elapsed_time_str = str(timedelta(seconds=final_time - start_time))
    print(f"Elapsed time: {elapsed_time_str}")


if __name__ == "__main__":
    main()
