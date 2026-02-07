from enum import Enum
import os
from PIL import Image
from time import time

BACKGROUND_COLOR = (255, 255, 255, 255)
END_COLOR = (255, 0, 0, 255)
INITIAL_POSITION = (1, 1)
INPUT_MAZE = "labyrinth.png"
MAX_DIRECTIONS = 4
OPPOSITE_DIRECTION_SHIFT = MAX_DIRECTIONS // 2
DISTANCE_BETWEEN_FREE_CELLS = 2
CURRENT_INDEX = -1
PREVIOUS_INDEX = -2


class Direction(Enum):
    UNDEFINED = -1
    DOWN = 0
    RIGHT = 1
    UP = 2
    LEFT = 3


CoordData = tuple[int, int]


def apply_direction(
    coord: CoordData,
    direction: Direction,
    add_offset: int = DISTANCE_BETWEEN_FREE_CELLS,
) -> CoordData:
    x, y = coord
    if direction == Direction.UNDEFINED:
        raise ValueError("Direction cannot be UNDEFINED")
    if direction == Direction.DOWN:
        return (x, y + add_offset)
    elif direction == Direction.RIGHT:
        return (x + add_offset, y)
    elif direction == Direction.UP:
        return (x, y - add_offset)
    else:
        return (x - add_offset, y)


def get_next_direction(direction: Direction) -> Direction:
    next_value = (direction.value + 1) % MAX_DIRECTIONS
    return Direction(next_value)


def print_elapsed_time(seconds: float) -> None:
    if seconds < 0:
        seconds = -seconds
        sign = "-"
    else:
        sign = ""
    total_ms = int(round(seconds * 1000))
    ms = total_ms % 1000
    total_s = total_ms // 1000
    s = total_s % 60
    total_min = total_s // 60
    m = total_min % 60
    total_h = total_min // 60
    h = total_h % 24
    d = total_h // 24
    parts: list[str] = []

    def add(value: int, singular: str, plural: str) -> None:
        if value:
            parts.append(f"{value} {singular if value == 1 else plural}")

    add(d, "day", "days")
    add(h, "hour", "hours")
    add(m, "minute", "minutes")
    add(s, "second", "seconds")
    if ms or not parts:
        parts.append(f"{ms} millisecond" if ms == 1 else f"{ms} milliseconds")
    print(sign + ", ".join(parts))


def get_opposite_coord(coord: CoordData, direction: Direction) -> CoordData:
    opposite_direction = get_opposite_direction(direction)
    opposite_coord = apply_direction(coord, opposite_direction)
    return opposite_coord


def get_opposite_direction(direction: Direction) -> Direction:
    if direction == Direction.UNDEFINED:
        raise ValueError("Direction cannot be UNDEFINED")
    shifted_value = direction.value + OPPOSITE_DIRECTION_SHIFT
    opposite_value = shifted_value % MAX_DIRECTIONS
    opposite_direction = Direction(opposite_value)
    return opposite_direction


def is_move_valid(coord: CoordData, direction: Direction, image: Image.Image) -> bool:
    coord = apply_direction(coord, direction)
    x, y = coord
    if y < 0 or x < 0:
        return False
    width, height = image.size
    if y >= height or x >= width:
        return False
    if image.getpixel(coord) != BACKGROUND_COLOR:
        return False
    return True


def possible_directions(coord: CoordData, image: Image.Image) -> list[Direction]:
    valid_directions: list[Direction] = []
    for direction in Direction:
        if not is_move_valid(coord, direction, image):
            continue
        valid_directions.append(direction)
    return valid_directions


def main() -> None:
    labyrinth = Image.open(INPUT_MAZE)
    width, height = labyrinth.size
    target_position = (
        width - DISTANCE_BETWEEN_FREE_CELLS,
        height - DISTANCE_BETWEEN_FREE_CELLS,
    )
    coord = INITIAL_POSITION
    path = [Direction.UNDEFINED]

    def backtrack_to_previous_coord(coord: CoordData) -> CoordData:
        coord = get_opposite_coord(coord, path[PREVIOUS_INDEX])
        path.pop()
        while len(possible_directions(coord, labyrinth)) == 2:
            coord = get_opposite_coord(coord, path[PREVIOUS_INDEX])
            path.pop()
        return coord

    paths_count = 0
    iterations = 0
    start_time = time()
    while coord != target_position:
        iterations += 1
        current_direction = path[CURRENT_INDEX]
        if len(path) == 1:
            current_direction = get_next_direction(path[CURRENT_INDEX])
            path[CURRENT_INDEX] = current_direction
            if not is_move_valid(coord, current_direction, labyrinth):
                continue
            coord = apply_direction(coord, current_direction)
            path.append(Direction.UNDEFINED)
            paths_count += 1
            continue
        directions_list = possible_directions(coord, labyrinth)
        if len(directions_list) == 1:
            # se o caminho for fechado, volte para trás
            coord = backtrack_to_previous_coord(coord)
            continue
        if len(directions_list) == 2:
            # se só houver uma possibilidade siga ela
            current_direction = directions_list[1]
            if directions_list[0] != get_opposite_direction(path[PREVIOUS_INDEX]):
                current_direction = directions_list[0]
            path[CURRENT_INDEX] = current_direction
            coord = apply_direction(coord, current_direction)
            path.append(Direction.UNDEFINED)
            paths_count += 1
            continue
        if current_direction == Direction.LEFT:
            # se todas as direções foram testadas, volte para trás
            coord = backtrack_to_previous_coord(coord)
            continue
        # se tem direções faltando, vá
        current_direction = get_next_direction(path[CURRENT_INDEX])
        path[CURRENT_INDEX] = current_direction
        if current_direction == get_opposite_direction(path[PREVIOUS_INDEX]):
            continue
        if not is_move_valid(coord, current_direction, labyrinth):
            continue
        coord = apply_direction(coord, current_direction)
        path.append(Direction.UNDEFINED)
        paths_count += 1
    end_time = time()
    print(f"paths tested : {paths_count}")
    print(f"iterations made : {iterations}")
    print_elapsed_time(end_time - start_time)
    path.pop()
    coord = INITIAL_POSITION
    labyrinth.putpixel(coord, END_COLOR)
    for direction in path:
        coord = apply_direction(coord, direction)
        labyrinth.putpixel(coord, END_COLOR)
        coord = apply_direction(coord, direction)
        labyrinth.putpixel(coord, END_COLOR)
    image_name, extension = os.path.splitext(INPUT_MAZE)
    name = f"{image_name}_solved{extension}"
    print(name)
    labyrinth.save(name)
    labyrinth.close()


if __name__ == "__main__":
    main()
