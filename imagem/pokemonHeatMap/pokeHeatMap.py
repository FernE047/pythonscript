import os
from PIL import Image

IMAGE_FOLDER = "./pokemon/pokedexSemFundo"
OUTPUT_IMAGE = "./heatMap.png"
TRANSPARENT = (0, 0, 0, 0)
BACKGROUND_COLOR = (0, 255, 255, 255)  # color: cyan
SPRITE_RESOLUTION = 96
SPRITE_SIZE = (SPRITE_RESOLUTION, SPRITE_RESOLUTION)
MAX_BRIGHTNESS = 255
MIN_BRIGHTNESS = 0
RED_CHANNEL = 0
GREEN_CHANNEL = 1
BLUE_CHANNEL = 2


def open_image_as_rgba(image_path: str) -> Image.Image:
    with Image.open(image_path) as image:
        image_in_memory = image.copy()
        if image.mode != "RGBA":
            return image_in_memory.convert("RGBA")
        return image_in_memory


def main() -> None:
    imagens = os.listdir(IMAGE_FOLDER)
    imagensCaminho = [os.path.join(IMAGE_FOLDER, imagem) for imagem in imagens]
    heatMap = Image.new("RGBA", SPRITE_SIZE, BACKGROUND_COLOR)
    for imagemCaminho in imagensCaminho:
        print(imagemCaminho)
        pokemon = open_image_as_rgba(imagemCaminho)
        for y in range(SPRITE_RESOLUTION):
            for x in range(SPRITE_RESOLUTION):
                coord = (x, y)
                if pokemon.getpixel(coord) == TRANSPARENT:
                    continue
                color = heatMap.getpixel(coord)
                if color is None:
                    raise ValueError("Pixel not found")
                if isinstance(color, float):
                    raise ValueError("Image is not in RGB mode")
                if isinstance(color, int):
                    raise ValueError("Image is not in RGB mode")
                if color[BLUE_CHANNEL] > MIN_BRIGHTNESS:
                    blue = color[BLUE_CHANNEL] - 1
                    heatMap.putpixel(
                        coord, (MIN_BRIGHTNESS, MAX_BRIGHTNESS, blue, MAX_BRIGHTNESS)
                    )
                elif color[RED_CHANNEL] < MAX_BRIGHTNESS:
                    red = color[RED_CHANNEL] + 1
                    heatMap.putpixel(
                        coord, (red, MAX_BRIGHTNESS, MIN_BRIGHTNESS, MAX_BRIGHTNESS)
                    )
                elif color[GREEN_CHANNEL] > MIN_BRIGHTNESS:
                    green = color[GREEN_CHANNEL] - 1
                    heatMap.putpixel(
                        coord, (MAX_BRIGHTNESS, green, MIN_BRIGHTNESS, MAX_BRIGHTNESS)
                    )
    heatMap.save(OUTPUT_IMAGE)


if __name__ == "__main__":
    main()
