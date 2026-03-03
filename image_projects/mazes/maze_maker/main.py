from enum import Enum
import os
from PIL import Image
from random import randint
from numpy.random import permutation

BACKGROUND_COLOR = (255, 255, 255, 255)
WALL_COLOR = (0, 0, 0, 255)
OUTPUT_IMAGE = "labyrinth.png"
MAX_DIRECTIONS = 4
DEFAULT_WIDTH = 25
DEFAULT_HEIGHT = 25


class Direction(Enum):
    DOWN = 0
    RIGHT = 1
    UP = 2
    LEFT = 3


CoordData = tuple[int, int]


def apply_direction(
    coord: CoordData, direction: Direction
) -> tuple[CoordData, CoordData]:
    x, y = coord
    if direction == Direction.DOWN:
        return ((x, y + 1), (x, y + 2))
    if direction == Direction.RIGHT:
        return ((x + 1, y), (x + 2, y))
    if direction == Direction.UP:
        return ((x, y - 1), (x, y - 2))
    if direction == Direction.LEFT:
        return ((x - 1, y), (x - 2, y))


def generate_labyrinth(labyrinth: Image.Image, open_vertices: list[CoordData]) -> None:
    if not open_vertices:
        return
    width, height = labyrinth.size
    index = randint(0, len(open_vertices) - 1)
    is_valid = False
    x, y = open_vertices[index]
    direction_order = permutation(MAX_DIRECTIONS).tolist()
    for direction_index in direction_order:
        direction = Direction(direction_index)
        path_1, path_2 = apply_direction((x, y), direction)
        if path_2[0] < 0 or path_2[0] >= width:
            continue
        if path_2[1] < 0 or path_2[1] >= height:
            continue
        if labyrinth.getpixel(path_2) != WALL_COLOR:
            continue
        labyrinth.putpixel(path_1, BACKGROUND_COLOR)
        labyrinth.putpixel(path_2, BACKGROUND_COLOR)
        open_vertices.append(path_2)
        is_valid = True
        break
    if not is_valid:
        open_vertices.pop(index)


def main() -> None:
    width = DEFAULT_WIDTH
    height = DEFAULT_HEIGHT
    if not width % 2:
        width += 1
    if not height % 2:
        height += 1
    open_vertices = [(1, 1)]
    labyrinth = Image.new("RGBA", (width, height), WALL_COLOR)
    labyrinth.putpixel((1, 1), BACKGROUND_COLOR)
    while open_vertices:
        generate_labyrinth(labyrinth, open_vertices)
    file_count = len(os.listdir())
    image_name, extension = os.path.splitext(OUTPUT_IMAGE)
    name = f"{image_name}_{file_count:03d}{extension}"
    print(name)
    labyrinth.save(name)
    labyrinth.close()


if __name__ == "__main__":
    main()
