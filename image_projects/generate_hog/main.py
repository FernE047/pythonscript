from colorsys import hsv_to_rgb
from enum import Enum
import os
from PIL import Image

IMAGE_FOLDER = "./images/pokedex_no_background"
ALLOWED_FILE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".bmp", ".gif")
IMAGE_OUTPUT = "./output/pokemon"
EXTENSION_OUTPUT = ".png"
INDEX_DEFAULT = 1


class Direction(Enum):
    DOWN_RIGHT = 0
    DOWN = 1
    DOWN_LEFT = 2
    LEFT = 3
    UP_LEFT = 4
    UP = 5
    UP_RIGHT = 6
    RIGHT = 7


CoordData = tuple[int, int]

DIRECTION_COUNT = len(Direction)
DIRECTION_UNIT = 1 / DIRECTION_COUNT
DIRECTION_SHIFT = DIRECTION_COUNT // 2
TONES = tuple(
    [
        int(hsv_to_rgb((n) * DIRECTION_UNIT, 1, 255)[0])
        for n in range(DIRECTION_COUNT + 1)
    ]
)


def get_pixel(image: Image.Image, coord: CoordData) -> int:
    pixel = image.getpixel(coord)
    if pixel is None:
        raise ValueError("Pixel not found")
    if isinstance(pixel, tuple):
        raise ValueError("Image is not in grayscale mode")
    if isinstance(pixel, float):
        raise ValueError("Image is not in RGB grayscale mode")
    return pixel


def open_image_as_rgba(image_path: str) -> Image.Image:
    with Image.open(image_path) as image:
        image_in_memory = image.copy()
        if image.mode != "RGBA":
            return image_in_memory.convert("RGBA")
        return image_in_memory


def get_image(index_chosen: int = INDEX_DEFAULT) -> str:
    if not os.path.exists(IMAGE_FOLDER):
        return ""
    index = 0
    for filename in os.listdir(IMAGE_FOLDER):
        _, extension = os.path.splitext(filename)
        if extension not in ALLOWED_FILE_EXTENSIONS:
            continue
        index += 1
        if index == index_chosen:
            return f"{IMAGE_FOLDER}/{filename}"
    return ""


def apply_direction(coord: CoordData | None, direction: Direction) -> CoordData:
    if coord is None:
        raise ValueError("Coordinate cannot be None")
    x, y = coord
    if direction == Direction.DOWN_RIGHT:
        return (x + 1, y + 1)
    if direction == Direction.DOWN:
        return (x, y + 1)
    if direction == Direction.DOWN_LEFT:
        return (x - 1, y + 1)
    if direction == Direction.LEFT:
        return (x - 1, y)
    if direction == Direction.UP_LEFT:
        return (x - 1, y - 1)
    if direction == Direction.UP:
        return (x, y - 1)
    if direction == Direction.UP_RIGHT:
        return (x + 1, y - 1)
    if direction == Direction.RIGHT:
        return (x + 1, y)


def convert_to_grayscale(image: Image.Image) -> Image.Image:
    return image.convert("L")


def calculate_dominant_direction(image: Image.Image, coord: CoordData) -> int:
    neighbor_pixels = [
        get_pixel(image, apply_direction(coord, direction)) for direction in Direction
    ]
    direction_weights: list[int] = []
    for direction_index in range(DIRECTION_COUNT):
        weight = 0
        for offset in range(-1, 2):
            neighbor_index = (direction_index + offset) % DIRECTION_COUNT
            weight += neighbor_pixels[neighbor_index]
        direction_weights.append(weight)
    difference_values: list[int] = []
    for direction_index in range(DIRECTION_SHIFT):
        opposite_index = (direction_index + DIRECTION_SHIFT) % DIRECTION_COUNT
        current_weight = direction_weights[direction_index]
        opposite_weight = direction_weights[opposite_index]
        difference = abs(current_weight - opposite_weight)
        difference_values.append(difference)
    max_difference = max(difference_values)
    major_differences: list[int] = []
    for direction_index in range(DIRECTION_SHIFT):
        if difference_values[direction_index] != max_difference:
            continue
        major_differences.append(direction_index)
    if len(major_differences) != 1:
        return DIRECTION_COUNT
    direction = major_differences[0]
    opposite_direction = (direction + DIRECTION_SHIFT) % DIRECTION_COUNT
    if direction_weights[direction] > direction_weights[opposite_direction]:
        return direction
    return opposite_direction


def hogify(image: Image.Image, hog_image: Image.Image) -> None:
    width, height = image.size
    for x in range(1, width - 1):
        for y in range(1, height - 1):
            coord = (x, y)
            direction_value = calculate_dominant_direction(image, coord)
            color = TONES[direction_value]
            hog_image.putpixel(coord, color)


def main() -> None:
    image = open_image_as_rgba(get_image(INDEX_DEFAULT))
    image_hog = Image.new("L", image.size, 0)
    image_grayscale = convert_to_grayscale(image)
    hogify(image_grayscale, image_hog)
    image.save(f"{IMAGE_OUTPUT}_001{EXTENSION_OUTPUT}")
    image_hog.save(f"{IMAGE_OUTPUT}_000{EXTENSION_OUTPUT}")


if __name__ == "__main__":
    main()
