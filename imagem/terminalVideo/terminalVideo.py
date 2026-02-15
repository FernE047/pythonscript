from PIL import Image
import os

BRIGHTNESS_LEVELS = [" ", "▫", "□", "O", "░", "▒", "▓", "█"]
LEVEL_COUNT = len(BRIGHTNESS_LEVELS)
MAX_BRIGHTNESS = 256
BRIGHTNESS_STEP = MAX_BRIGHTNESS // LEVEL_COUNT
FRAMES_FOLDER = "./video"
DISPLAY_HEIGHT_DEFAULT = 0
DISPLAY_WIDTH_DEFAULT = 60
CLEAR_COMMAND = "cls" if os.name == "nt" else "clear"

CoordData = tuple[int, int]


def get_pixel(image: Image.Image, coord: CoordData) -> int:
    pixel = image.getpixel(coord)
    if pixel is None:
        raise ValueError("Pixel not found")
    if isinstance(pixel, tuple):
        raise ValueError("Image is not in grayscale mode")
    if isinstance(pixel, float):
        raise ValueError("Image is not in RGB grayscale mode")
    return pixel


def open_image(image_path: str) -> Image.Image:
    with Image.open(image_path) as image:
        image_in_memory = image.copy()
        return image_in_memory


def frame_to_text(image: str) -> str:
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
    image_text = ""
    for y in range(height):
        image_row = ""
        for x in range(width):
            pixel = get_pixel(display_image, (x, y))
            step = pixel // BRIGHTNESS_STEP
            current_level = BRIGHTNESS_LEVELS[step]
            image_row += current_level
        image_text += f"{image_row}\n"
    return image_text


def main() -> None:
    frames_raw = os.listdir(FRAMES_FOLDER)
    frames = [f"{FRAMES_FOLDER}/{frame}" for frame in frames_raw]
    for frame in frames:
        frame_text = frame_to_text(frame)
        backspace_count = len(frame_text)
        os.system(CLEAR_COMMAND)
        backspaces = backspace_count * "\b"
        print(f"{frame_text}{backspaces}", end="", flush=True)


if __name__ == "__main__":
    main()
