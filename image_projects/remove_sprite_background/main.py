import os
from PIL import Image

IMAGE_FOLDER = "./pokemon/pokedex_curated"
TRANSPARENT = (0, 0, 0, 0)
SPRITE_RESOLUTION = 96
FIRST_PIXEL = (0, 0)


def open_image_as_rgba(image_path: str) -> Image.Image:
    with Image.open(image_path) as image:
        image_in_memory = image.copy()
        if image.mode != "RGBA":
            return image_in_memory.convert("RGBA")
        return image_in_memory


def main() -> None:
    images = os.listdir(IMAGE_FOLDER)
    image_names = [os.path.join(IMAGE_FOLDER, image) for image in images]
    for image_number, image_name in enumerate(image_names):
        print(image_name)
        pokemon = open_image_as_rgba(image_name)
        background_color = pokemon.getpixel(FIRST_PIXEL)
        for y in range(SPRITE_RESOLUTION):
            for x in range(SPRITE_RESOLUTION):
                coord = (x, y)
                if pokemon.getpixel(coord) == background_color:
                    pokemon.putpixel(coord, TRANSPARENT)
        pokemon.save(f"./pokemon/pokedexSemFundo/pokemon_{image_number:03d}.png")


if __name__ == "__main__":
    main()
