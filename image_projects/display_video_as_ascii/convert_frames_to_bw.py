from pathlib import Path

from PIL import Image

LEVEL_COUNT = 8
MAX_BRIGHTNESS = 256
BRIGHTNESS_STEP = MAX_BRIGHTNESS // LEVEL_COUNT
FRAMES_FOLDER = Path("video")
DISPLAY_HEIGHT_DEFAULT = 0
DISPLAY_WIDTH_DEFAULT = 80

CoordData = tuple[int, int]


def get_pixel(image: Image.Image, coord: CoordData) -> float | int:
    pixel = image.getpixel(coord)
    if pixel is None:
        raise ValueError("Pixel not found")
    if isinstance(pixel, tuple):
        raise ValueError("Image is not in grayscale mode")
    return pixel


def open_image(image_path: Path) -> Image.Image:
    with Image.open(image_path) as image:
        image_in_memory = image.copy()
        return image_in_memory


def frame_to_text(image: Path) -> None:
    display_height = DISPLAY_HEIGHT_DEFAULT
    display_width = DISPLAY_WIDTH_DEFAULT
    color_image = open_image(image)
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
    display_image.save(image)


def convert_frames_to_bw() -> None:
    frames_raw = list(FRAMES_FOLDER.iterdir())
    frames = [
        frame
        for frame in frames_raw
        if frame.is_file() and frame.suffix.lower() in (".jpg", ".jpeg", ".png")
    ]
    for frame in frames:
        frame_to_text(frame)
