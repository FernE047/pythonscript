import os
from PIL import Image
import shelve

IMAGE_FOLDER = "./pokemon/pokedexSemFundo"
TRANSPARENT = (0, 0, 0, 0)
SPRITE_RESOLUTION = 96
DATABASE_LOCATION = "./dadosPreProcessados"


def open_image_as_rgba(image_path: str) -> Image.Image:
    with Image.open(image_path) as image:
        image_in_memory = image.copy()
        if image.mode != "RGBA":
            return image_in_memory.convert("RGBA")
        return image_in_memory


def main() -> None:
    images = os.listdir(IMAGE_FOLDER)
    image_names = [os.path.join(IMAGE_FOLDER, image) for image in images]
    x_heat: list[int] = []
    y_heat: list[int] = []
    z_heat: list[int] = []
    for x in range(SPRITE_RESOLUTION):
        for y in range(SPRITE_RESOLUTION):
            x_heat.append(x)
            y_heat.append(y)
            z_heat.append(0)
    for image_path in image_names:
        print(image_path)
        pokemon = open_image_as_rgba(image_path)
        for x in range(SPRITE_RESOLUTION):
            block_x = SPRITE_RESOLUTION * x
            for y in range(SPRITE_RESOLUTION):
                if pokemon.getpixel((x, y)) != TRANSPARENT:
                    z_heat[block_x + y] += 1
    with shelve.open(DATABASE_LOCATION) as database:
        database["x"] = x_heat
        database["y"] = y_heat
        database["z"] = z_heat


if __name__ == "__main__":
    main()
