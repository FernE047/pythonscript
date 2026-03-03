from enum import Enum
from PIL import Image

CoordData = tuple[int, int]

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLACK_4 = (0, 0, 0, 255)
BLACK_2 = (0, 255)
BLACK_1 = 0
MAX_SIZE = 200


class Direction(Enum):
    DOWN_RIGHT = 0
    DOWN = 1
    DOWN_LEFT = 2
    RIGHT = 3
    LEFT = 4
    UP_RIGHT = 5
    UP = 6
    UP_LEFT = 7


def apply_direction(coord: CoordData, direction: Direction) -> CoordData:
    x, y = coord
    if direction == Direction.DOWN_RIGHT:
        return (x + 1, y + 1)
    if direction == Direction.DOWN:
        return (x, y + 1)
    if direction == Direction.DOWN_LEFT:
        return (x - 1, y + 1)
    if direction == Direction.RIGHT:
        return (x + 1, y)
    if direction == Direction.LEFT:
        return (x - 1, y)
    if direction == Direction.UP_RIGHT:
        return (x + 1, y - 1)
    if direction == Direction.UP:
        return (x, y - 1)
    if direction == Direction.UP_LEFT:
        return (x - 1, y - 1)


def is_pixel_black(pixel: float | tuple[int, ...] | None) -> bool:
    if pixel is None:
        return False
    if isinstance(pixel, int):
        return pixel == 0
    if isinstance(pixel, float):
        return int(pixel) == 0
    if len(pixel) >= 3:
        return pixel in [BLACK, BLACK_4]
    if len(pixel) >= 1:
        return pixel in [BLACK_1, BLACK_2]
    return False


def open_image(image_path: str) -> Image.Image:
    with Image.open(image_path) as image:
        image_in_memory = image.copy()
        return image_in_memory


def main() -> None:
    current_frame = open_image("frame_000.png")
    has_black_pixels = True
    frame_index = 0
    while has_black_pixels:
        has_black_pixels = False
        next_frame = Image.new("RGBA", (MAX_SIZE, MAX_SIZE), WHITE)
        for x in range(MAX_SIZE):
            for y in range(MAX_SIZE):
                coord = (x, y)
                pixel = current_frame.getpixel(coord)
                if not is_pixel_black(pixel):
                    continue
                has_black_pixels = True
                for direction in Direction:
                    current_coord = apply_direction(coord, direction)
                    if (max(current_coord) >= MAX_SIZE) or (min(current_coord) < 0):
                        continue
                    if not is_pixel_black(current_frame.getpixel(current_coord)):
                        next_frame.putpixel(current_coord, BLACK)
        filename = f"frame_{frame_index:03d}.png"
        print(filename)
        next_frame.save(filename)
        current_frame = open_image(filename)
        frame_index += 1


if __name__ == "__main__":
    main()
