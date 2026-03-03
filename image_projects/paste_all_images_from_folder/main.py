import os
from PIL import Image
import random

SPRITE_RESOLUTION = 96
SPRITE_SIZE = (SPRITE_RESOLUTION, SPRITE_RESOLUTION)
HEATMAP_COLOR = (0, 255, 255, 255)
TRANSPARENT = (0, 0, 0, 0)
IMAGE_FOLDER = "./pokemon/pokedexSemFundo"
OUTPUT_NAME = "./paçoca.png"

PixelData = tuple[int, ...]
CoordData = tuple[int, int]


def get_pixel(image: Image.Image, coord: CoordData) -> PixelData:
    pixel = image.getpixel(coord)
    if pixel is None:
        raise ValueError("Pixel not found")
    if isinstance(pixel, int):
        raise ValueError("Image is not in RGB mode")
    if isinstance(pixel, float):
        raise ValueError("Image is not in RGB mode")
    if len(pixel) < 4:
        raise ValueError("Image is not in RGB mode")
    return pixel


def open_image_as_rgba(image_path: str) -> Image.Image:
    with Image.open(image_path) as image:
        image_in_memory = image.copy()
        if image.mode != "RGBA":
            return image_in_memory.convert("RGBA")
        return image_in_memory


def main() -> None:
    images = os.listdir(IMAGE_FOLDER)
    images_names = [os.path.join(IMAGE_FOLDER, image) for image in images]
    heatMap = Image.new("RGBA", SPRITE_SIZE, HEATMAP_COLOR)
    random.shuffle(images_names)
    for image_index, imagemCaminho in enumerate(images_names):
        print(image_index, end=",")
        pokemon = open_image_as_rgba(imagemCaminho)
        for y in range(SPRITE_RESOLUTION):
            for x in range(SPRITE_RESOLUTION):
                color = get_pixel(pokemon, (x, y))
                if color != TRANSPARENT:
                    heatMap.putpixel((x, y), color)
    heatMap.save(OUTPUT_NAME)


if __name__ == "__main__":
    main()
