from PIL import Image
import os

IMAGES_FOLDER = "imagens"
MAX_COLOR_CHANNELS = 4
MAX_BRIGHTNESS = 256
TRANSPARENT = (0, 0, 0, 0)
ALLOWED_IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".bmp", ".gif")
PALETTE_FOLDER = "palette"

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


def get_image_from_folder(sub_folder: str) -> list[str]:
    folder = f"{IMAGES_FOLDER}/{sub_folder}"
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
    print(f"enter the subfolder name in {IMAGES_FOLDER} folder")
    subfolder_name = input()
    images = get_image_from_folder(subfolder_name)
    for image_index, image_name in enumerate(images):
        print(f"{image_index}  -  {image_name}")
    print(f"\nchoose 0 to {len(images) - 1}")
    selected_image_index = int(input())
    selected_image_name = images[selected_image_index]
    image = open_image_as_rgba(selected_image_name)
    width, height = image.size
    color_palette: PaletteData = set()
    for x in range(width):
        for y in range(height):
            pixel = get_pixel(image, (x, y))
            color_palette.add(pixel)
    print(color_palette)
    height = int(len(color_palette) / MAX_BRIGHTNESS) + 1
    if height > 1:
        color_palette_image = Image.new("RGBA", (MAX_BRIGHTNESS, height), TRANSPARENT)
    else:
        color_palette_image = Image.new("RGBA", (len(color_palette), height), TRANSPARENT)
    for index, color in enumerate(color_palette):
        color_palette_image.putpixel((index % MAX_BRIGHTNESS, index // MAX_BRIGHTNESS), color)
    print(selected_image_name)
    print("image name for palette")
    user_input = input()
    color_palette_image.save(os.path.join(PALETTE_FOLDER, f"palette_{user_input}.png"))


if __name__ == "__main__":
    main()
