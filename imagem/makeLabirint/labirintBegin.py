from enum import Enum
import os
from PIL import Image

BACKGROUND_COLOR = (255, 255, 255, 255)
WALL_COLOR = (0, 0, 0, 255)
COLORS = {
    0: (255, 255, 0, 255),
    1: (0, 0, 255, 255),
    2: (0, 255, 0, 255),
    3: (255, 0, 0, 255),
}
INPUT_FILE = "labyrinth.png"


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
    if direction == Direction.RIGHT:
        return (x + 1, y)
    if direction == Direction.UP:
        return (x, y - 1)
    if direction == Direction.LEFT:
        return (x - 1, y)


def main() -> None:
    labyrinth_image = Image.open(INPUT_FILE)
    largura, altura = labyrinth_image.size
    for x in range(1, largura - 1, 2):
        for y in range(1, altura - 1, 2):
            coord = (x, y)
            orthogonal_neighbors: list[CoordData] = []
            if labyrinth_image.getpixel(coord) != BACKGROUND_COLOR:
                continue
            for direction in Direction:
                new_coord = apply_direction(coord, direction)
                if labyrinth_image.getpixel(new_coord) != WALL_COLOR:
                    continue
                orthogonal_neighbors.append(new_coord)
            color_index = len(orthogonal_neighbors)
            labyrinth_image.putpixel(coord, COLORS[color_index])
    file_count = len(os.listdir())
    image_name, extension = os.path.splitext(INPUT_FILE)
    output_name = f"{image_name}_{file_count:03d}{extension}"
    labyrinth_image.save(output_name)
    labyrinth_image.close()


if __name__ == "__main__":
    main()
