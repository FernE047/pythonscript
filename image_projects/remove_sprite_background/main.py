from pathlib import Path
from PIL import Image

POKEMON_FOLDER = Path("pokemon")
IMAGE_FOLDER = POKEMON_FOLDER / "pokedex_curated"
TRANSPARENT = (0, 0, 0, 0)
SPRITE_RESOLUTION = 96
FIRST_PIXEL = (0, 0)


def open_image_as_rgba(image_path: Path) -> Image.Image:
    with Image.open(image_path) as image:
        image_in_memory = image.copy()
        if image.mode != "RGBA":
            return image_in_memory.convert("RGBA")
        return image_in_memory


def main() -> None:
    image_names = [
        IMAGE_FOLDER / image
        for image in IMAGE_FOLDER.iterdir()
        if image.suffix in (".png", ".jpg", ".jpeg")
    ]
    output_folder = POKEMON_FOLDER / "pokedexSemFundo"
    output_folder.mkdir(exist_ok=True)
    for image_number, image_name in enumerate(image_names):
        print(image_name)
        pokemon = open_image_as_rgba(image_name)
        background_color = pokemon.getpixel(FIRST_PIXEL)
        for y in range(SPRITE_RESOLUTION):
            for x in range(SPRITE_RESOLUTION):
                coord = (x, y)
                if pokemon.getpixel(coord) == background_color:
                    pokemon.putpixel(coord, TRANSPARENT)

        pokemon.save(output_folder / f"pokemon_{image_number:03d}.png")


if __name__ == "__main__":
    main()
