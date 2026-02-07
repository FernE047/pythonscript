from enum import Enum
import os
from PIL import Image

BACKGROUND_COLOR = (255, 255, 255, 255)
WALL_COLOR = (0, 0, 0, 255)
END_COLOR = (255, 0, 0, 255)
INITIAL_POSITION = (1, 1)
INPUT_MAZE = "labyrinth.png"
MAX_DIRECTIONS = 4
OPPOSITE_DIRECTION_SHIFT = MAX_DIRECTIONS // 2
DISTANCE_BETWEEN_FREE_CELLS = 2


class Direction(Enum):
    DOWN = 0
    RIGHT = 1
    UP = 2
    LEFT = 3


CoordData = tuple[int, int]


def apply_direction(coord: CoordData, direction: Direction) -> CoordData:
    x, y = coord
    if direction == Direction.DOWN:
        return (x, y + 1)
    elif direction == Direction.RIGHT:
        return (x + 1, y)
    elif direction == Direction.UP:
        return (x, y - 1)
    else:
        return (x - 1, y)


def is_maze_solved(labyrinth: Image.Image, coord_to_check: CoordData) -> bool:
    return labyrinth.getpixel(coord_to_check) == END_COLOR


def get_opposite_direction(direction: Direction) -> Direction:
    shifted_value = direction.value + OPPOSITE_DIRECTION_SHIFT
    opposite_value = shifted_value % MAX_DIRECTIONS
    opposite_direction = Direction(opposite_value)
    return opposite_direction


def labyrinth_solver(
    labyrinth: Image.Image, coord: CoordData, path: list[Direction]
) -> None:
    width, height = labyrinth.size
    final = (width - DISTANCE_BETWEEN_FREE_CELLS, height - DISTANCE_BETWEEN_FREE_CELLS)
    if is_maze_solved(labyrinth, coord):
        return
    for direction in Direction:
        if direction == get_opposite_direction(path[-1]):
            continue
        path.append(direction)
        test_coord = apply_direction(coord, direction)
        next_coord = apply_direction(test_coord, direction)
        try:
            next_pixel = labyrinth.getpixel(next_coord)
            next_pixel = labyrinth.getpixel(test_coord)
        except Exception:
            path.pop()
            continue
        if next_pixel == BACKGROUND_COLOR:
            if next_coord == final:
                labyrinth.putpixel(next_coord, END_COLOR)
            else:
                labyrinth_solver(labyrinth, next_coord, path)
        if is_maze_solved(labyrinth, coord):
            labyrinth.putpixel(test_coord, END_COLOR)
            labyrinth.putpixel(next_coord, END_COLOR)
            break
        path.pop()


def main() -> None:
    labyrinth = Image.open(INPUT_MAZE)
    path = [
        Direction.DOWN
    ]  # starts with DOWN, because we skip the opposite of the last direction, and the opposite of DOWN is UP, which is never the first direction to try
    labyrinth_solver(labyrinth, INITIAL_POSITION, path)
    image_name, extension = os.path.splitext(INPUT_MAZE)
    name = f"{image_name}_solved{extension}"
    print(name)
    labyrinth.save(name)
    labyrinth.close()


if __name__ == "__main__":
    main()
