import numpy as np
import cv2

from PIL import Image

INPUT_IMAGE_PATH = "input.jpg"
OUTPUT_IMAGE_PATH = "output.jpg"


def open_image_as_rgba(image_path: str) -> Image.Image:
    with Image.open(image_path) as image:
        image_in_memory = image.copy()
        if image.mode != "RGBA":
            return image_in_memory.convert("RGBA")
        return image_in_memory


def main() -> None:
    image = open_image_as_rgba(INPUT_IMAGE_PATH)
    np_image = np.asarray(image).astype(np.uint8)
    np_image[:, :, 0] = 0
    np_image[:, :, 2] = 0
    im = cv2.cvtColor(np_image, cv2.COLOR_RGB2GRAY)
    _, thresh = cv2.threshold(im, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    bin_image = Image.fromarray(thresh)
    bin_image.save(OUTPUT_IMAGE_PATH)


if __name__ == "__main__":
    main()