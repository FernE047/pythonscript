from PIL import Image
import os

LEVEL_COUNT = 8
MAX_BRIGHTNESS = 256
BRIGHTNESS_STEP = MAX_BRIGHTNESS // LEVEL_COUNT
FRAMES_FOLDER = "./video"

CoordData = tuple[int, int]


def get_pixel(image: Image.Image, coord: CoordData) -> float | int:
    pixel = image.getpixel(coord)
    if pixel is None:
        raise ValueError("Pixel not found")
    if isinstance(pixel, tuple):
        raise ValueError("Image is not in grayscale mode")
    return pixel


def open_image(image_path: str) -> Image.Image:
    with Image.open(image_path) as image:
        image_in_memory = image.copy()
        return image_in_memory


def frame_to_text(imagem: str) -> None:
    display_height = 0
    display_width = 80
    color_image = open_image(imagem)
    grayscale_image = color_image.convert("L")
    width, height = grayscale_image.size
    if display_height == 0:
        if width > display_width:
            aspectRatio = display_width / width
            display_height = int(height * aspectRatio)
        else:
            display_height = height
    display_image = grayscale_image.resize((display_width, display_height))
    width, height = display_image.size
    for y in range(height):
        for x in range(width):
            pixel = get_pixel(display_image, (x, y))
            step = pixel // BRIGHTNESS_STEP
            grayscale_value = step * BRIGHTNESS_STEP - 1
            display_image.putpixel((x, y), grayscale_value)
    display_image.save(imagem)


def main() -> None:
    frames_raw = os.listdir(FRAMES_FOLDER)
    frames = [f"{FRAMES_FOLDER}/{frame}" for frame in frames_raw]
    for frame in frames:
        frame_to_text(frame)


if __name__ == "__main__":
    main()
