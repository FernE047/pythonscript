from PIL import Image
import os

IMAGES_FOLDER = "imagens"
SUBFOLDER_DEFAULT = "pokedex_no_background"
MAX_COLOR_CHANNELS = 4
MAX_BRIGHTNESS = 256
TRANSPARENT = (0, 0, 0, 0)
ALLOWED_IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".bmp", ".gif")
PALETTE_FOLDER = "palette"
PALETTE_OUTPUT = "palette_pokemons.png"

PixelData = tuple[int, ...]
PaletteData = set[PixelData]

CoordData = tuple[int, int]


def get_pixel(image: Image.Image, coord: CoordData) -> PixelData:
    pixel = image.getpixel(coord)
    if pixel is None:
        raise ValueError("Pixel not found")
    if isinstance(pixel, int):
        raise ValueError("Image is not in RGB mode")
    if isinstance(pixel, float):
        raise ValueError("Image is not in RGB mode")
    if len(pixel) < MAX_COLOR_CHANNELS:
        raise ValueError("Image is not in RGB mode")
    return pixel


def get_image_from_folder(image_category: str) -> list[str]:
    folder = f"{IMAGES_FOLDER}/{image_category}"
    images: list[str] = []
    if os.path.exists(folder):
        for filename in os.listdir(folder):
            if filename.lower().endswith(ALLOWED_IMAGE_EXTENSIONS):
                images.append(os.path.join(folder, filename))
    return images


def open_image_as_rgba(image_path: str) -> Image.Image:
    with Image.open(image_path) as image:
        image_in_memory = image.copy()
        if image.mode != "RGBA":
            return image_in_memory.convert("RGBA")
        return image_in_memory


def main() -> None:
    images = get_image_from_folder(SUBFOLDER_DEFAULT)
    palette: PaletteData = set()
    for img in images:
        imagem = open_image_as_rgba(img)
        largura, altura = imagem.size
        for x in range(largura):
            for y in range(altura):
                pixel = get_pixel(imagem, (x, y))
                palette.add(pixel)
    altura = int(len(palette) / MAX_BRIGHTNESS) + 1
    if altura > 1:
        paletteImg = Image.new("RGBA", (MAX_BRIGHTNESS, altura), TRANSPARENT)
    else:
        paletteImg = Image.new("RGBA", (len(palette), altura), TRANSPARENT)
    for index, color in enumerate(palette):
        paletteImg.putpixel((index % MAX_BRIGHTNESS, index // MAX_BRIGHTNESS), color)
    paletteImg.save(os.path.join(PALETTE_FOLDER, PALETTE_OUTPUT))


if __name__ == "__main__":
    main()
