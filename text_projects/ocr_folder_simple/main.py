# pytesseract doesn't have type hints, so we ignore it
import pytesseract as ocr  # type: ignore
from pathlib import Path
import time
from datetime import timedelta
from PIL import Image

IMAGE_FOLDER = Path("images")
WHITESPACES = [" ", "\n", "\t"]


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
    elapsed_time_str = str(timedelta(seconds=final_time - start_time))
    print(f"Elapsed time: {elapsed_time_str}")



if __name__ == "__main__":
    main()