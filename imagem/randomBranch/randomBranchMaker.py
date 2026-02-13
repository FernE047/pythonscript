import shelve
from PIL import Image
from numpy.random import shuffle
from enum import Enum

# this code generates a random spiral image with a random number of branches

BLACK = (0, 0, 0, 255)
WHITE = (255, 255, 255, 255)
RED = (255, 0, 0, 255)
MIN_BRANCH = 2
DATABASE_PATH = "./numero"


class Direction(Enum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3


def calculate_min_max(values: list[int], is_horizontal: bool) -> tuple[int, int]:
    if is_horizontal:
        offset_value = 0
    else:
        offset_value = 1
    current_position = 0
    minimum_position = 0
    maximum_position = 0
    for index in range(offset_value, len(values), 2):
        if index % 2:
            adjusted_index = index - 1
        else:
            adjusted_index = index
        if adjusted_index % 4 == 0:
            current_position += values[adjusted_index]
        else:
            current_position -= values[adjusted_index]
        if current_position < minimum_position:
            minimum_position = current_position
        if current_position > maximum_position:
            maximum_position = current_position
    return (minimum_position, maximum_position)


def main() -> None:
    while True:
        try:
            print("enter the maximum number of branches")
            max_branches = int(input())
            break
        except ValueError:
            print("invalid number, try again")
    with shelve.open(DATABASE_PATH) as database:
        if "image_index" not in database:
            database["image_index"] = 0
        image_index = database["image_index"]
        branch_lengths = [
            branch_length for branch_length in range(MIN_BRANCH, max_branches + 1)
        ]
        shuffle(branch_lengths)
        print(branch_lengths)
        width_min_max = calculate_min_max(branch_lengths, True)
        height_min_max = calculate_min_max(branch_lengths, False)
        initial_position = (-width_min_max[0], -height_min_max[0])
        width = width_min_max[1] - width_min_max[0] + 1
        height = height_min_max[1] - height_min_max[0] + 1
        print(height)
        print(width)
        spiral = Image.new("RGBA", (width, height), WHITE)
        print(f"altura :  {height}")
        print(f"largura : {width}")
        print(f"inicial : {initial_position}")
        spiral.putpixel(initial_position, RED)
        current_position = list(initial_position)
        for branch_index, branch_length in enumerate(branch_lengths):
            direction = Direction(branch_index % 4)
            if direction == Direction.RIGHT:
                for _ in range(branch_length):
                    current_position[0] += 1
                    spiral.putpixel((current_position[0], current_position[1]), BLACK)
            elif direction == Direction.DOWN:
                for _ in range(branch_length):
                    current_position[1] += 1
                    spiral.putpixel((current_position[0], current_position[1]), BLACK)
            elif direction == Direction.LEFT:
                for _ in range(branch_length):
                    current_position[0] -= 1
                    spiral.putpixel((current_position[0], current_position[1]), BLACK)
            else:
                for _ in range(branch_length):
                    current_position[1] -= 1
                    spiral.putpixel((current_position[0], current_position[1]), BLACK)
        image_index += 1
        spiral.save(f"./imagem{image_index}.png")
        database["image_index"] = image_index


if __name__ == "__main__":
    main()
