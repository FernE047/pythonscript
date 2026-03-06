from pathlib import Path
from PIL import Image
import shelve

IMAGE_FOLDER = Path("pokemon") / "pokedexSemFundo"
TRANSPARENT = (0, 0, 0, 0)
SPRITE_RESOLUTION = 96
DATABASE_PATH = Path("dadosPreProcessados")


def open_image_as_rgba(image_path: Path) -> Image.Image:
    with Image.open(image_path) as image:
        image_in_memory = image.copy()
        if image.mode != "RGBA":
            return image_in_memory.convert("RGBA")
        return image_in_memory


def process_sprites() -> None:
    x_heat: list[int] = []
    y_heat: list[int] = []
    z_heat: list[int] = []
    for x in range(SPRITE_RESOLUTION):
        for y in range(SPRITE_RESOLUTION):
            x_heat.append(x)
            y_heat.append(y)
            z_heat.append(0)
    for image_path in IMAGE_FOLDER.iterdir():
        print(image_path)
        pokemon = open_image_as_rgba(image_path)
        for x in range(SPRITE_RESOLUTION):
            block_x = SPRITE_RESOLUTION * x
            for y in range(SPRITE_RESOLUTION):
                if pokemon.getpixel((x, y)) != TRANSPARENT:
                    z_heat[block_x + y] += 1
    with shelve.open(DATABASE_PATH) as database:
        database["x"] = x_heat
        database["y"] = y_heat
        database["z"] = z_heat
