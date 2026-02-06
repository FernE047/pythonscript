from enum import Enum
import os
from PIL import Image
from random import randint
from numpy.random import permutation

BACKGROUND_COLOR = (255, 255, 255, 255)
WALL_COLOR = (0, 0, 0, 255)
STRUCTURES_COLORS = (BACKGROUND_COLOR, WALL_COLOR)
START_COLOR = (0, 0, 255, 255)
END_COLOR = (255, 0, 0, 255)
OUTPUT_IMAGE = "labyrinth.png"
MAX_DIRECTIONS = 4
DEFAULT_WIDTH = 1000
DEFAULT_HEIGHT = 1000
DEFAULT_PATHS_TO_SOLVE = 50


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


def generate_labyrinth(
    labyrinth: Image.Image,
    open_vertices: list[CoordData],
    color: tuple[int, int, int, int],
) -> None:
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
        labyrinth.putpixel(path_1, color)
        labyrinth.putpixel(path_2, color)
        open_vertices.append(path_2)
        is_valid = True
        break
    if not is_valid:
        open_vertices.pop(index)


def generate_paths(image: Image.Image) -> None:
    width, height = image.size
    vertices: list[CoordData] = []
    for x in range(3, width, 2):
        for y in range(1, height, 2):
            pixel_a = image.getpixel((x, y))
            pixel_b = image.getpixel((x - 2, y))
            if pixel_a == pixel_b:
                continue
            if (x - 1, y) in vertices:
                continue
            vertices.append((x - 1, y))
    for x in range(1, width, 2):
        for y in range(3, height, 2):
            pixel_a = image.getpixel((x, y))
            pixel_b = image.getpixel((x, y - 2))
            if pixel_a == pixel_b:
                continue
            if (x, y - 1) in vertices:
                continue
            vertices.append((x, y - 1))
    vertices = permutation(vertices).tolist()
    paths_to_solve = DEFAULT_PATHS_TO_SOLVE
    if paths_to_solve > len(vertices):
        paths_to_solve = len(vertices)
    for index in range(paths_to_solve):
        image.putpixel(vertices[index], BACKGROUND_COLOR)


def correct_labyrinth_colors(image: Image.Image) -> None:
    width, height = image.size
    for x in range(width):
        for y in range(height):
            if image.getpixel((x, y)) not in STRUCTURES_COLORS:
                image.putpixel((x, y), BACKGROUND_COLOR)


def main() -> None:
    width = DEFAULT_WIDTH
    height = DEFAULT_HEIGHT
    if not width % 2:
        width += 1
    if not height % 2:
        height += 1
    open_vertices_start = [(1, 1)]
    open_vertices_end = [(width - 2, height - 2)]
    labyrinth = Image.new("RGBA", (width, height), WALL_COLOR)
    labyrinth.putpixel((1, 1), START_COLOR)
    labyrinth.putpixel((width - 2, height - 2), END_COLOR)
    while open_vertices_start or open_vertices_end:
        generate_labyrinth(labyrinth, open_vertices_start, START_COLOR)
        generate_labyrinth(labyrinth, open_vertices_end, END_COLOR)
    generate_paths(labyrinth)
    correct_labyrinth_colors(labyrinth)
    file_count = len(os.listdir())
    image_name, extension = os.path.splitext(OUTPUT_IMAGE)
    name = f"{image_name}_{file_count:03d}{extension}"
    print(name)
    labyrinth.save(name)
    labyrinth.close()


if __name__ == "__main__":
    main()
