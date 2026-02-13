from PIL import Image
from colorsys import rgb_to_hsv
from colorsys import hsv_to_rgb

# * is a wildcard
INPUT_IMAGE = "./pokedexSemFundo/pokemon_*.png"
OUTPUT_FOLDER = "./pokedexRecolorPokemons/pokemon_*"
OUTPUT_IMAGE = "./pokedexRecolorPokemons/pokemon_**/pokemon_**_*.png"
MIN_BRIGHTNESS = 0
MAX_BRIGHTNESS = 255
BACKGROUND_COLOR = (255, 255, 255, 0)
HUE_SHIFT = 12
RED_CHANNEL = 0
GREEN_CHANNEL = 1
BLUE_CHANNEL = 2
ALPHA_CHANNEL = 3
HUE_CHANNEL = 0
SATURATION_CHANNEL = 1
VALUE_CHANNEL = 2
POKEMON_COUNT = 762

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
    for pokedex_index in range(POKEMON_COUNT):
        input_image = open_image_as_rgba(
            INPUT_IMAGE.replace("*", f"{pokedex_index:03d}")
        )
        width, height = input_image.size
        save_name = OUTPUT_IMAGE.replace("**", f"{pokedex_index:03d}")
        for hue_shift_factor in range(HUE_SHIFT):
            recolor_image = Image.new("RGBA", input_image.size, BACKGROUND_COLOR)
            for x in range(width):
                for y in range(height):
                    pixel_rgb = get_pixel(input_image, (x, y))
                    if pixel_rgb[ALPHA_CHANNEL] == MIN_BRIGHTNESS:
                        continue
                    pixel_hsv = rgb_to_hsv(
                        pixel_rgb[RED_CHANNEL],
                        pixel_rgb[GREEN_CHANNEL],
                        pixel_rgb[BLUE_CHANNEL],
                    )
                    shifted_hue_hsv = list(pixel_hsv)
                    shifted_hue_hsv[HUE_CHANNEL] = (
                        shifted_hue_hsv[HUE_CHANNEL] + hue_shift_factor / HUE_SHIFT
                    )
                    shifted_hue_hsv[HUE_CHANNEL] -= shifted_hue_hsv[HUE_CHANNEL] // 1
                    updated_pixel_rgb = hsv_to_rgb(
                        shifted_hue_hsv[HUE_CHANNEL],
                        shifted_hue_hsv[SATURATION_CHANNEL],
                        shifted_hue_hsv[VALUE_CHANNEL],
                    )
                    pixel_rgb = tuple([int(n) for n in updated_pixel_rgb])
                    recolor_image.putpixel((x, y), pixel_rgb)
            image_name = save_name.replace("*", f"{hue_shift_factor:02d}")
            recolor_image.save(image_name)


if __name__ == "__main__":
    main()
