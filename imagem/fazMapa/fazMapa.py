from PIL import Image
import random
import os

OCEAN_COLOR = (0, 128, 255, 255)
LAND_COLOR = (0, 255, 74, 255)
SAND_COLOR = (255, 204, 102, 255)
DEFAULT_WIDTH = 100
DEFAULT_HEIGHT = 100
DEFAULT_SEED = 20
DEFAULT_PERCENTAGE = 50
MAX_LAND_PERCENTAGE = 90





def find_available_land(is_x_first: bool, size_a: int, size_b_range: tuple[int, int, int], mapa: Image.Image) -> list[tuple[int, int]]:
    first_b, last_b, step_b = size_b_range
    available_spaces: list[tuple[int, int]] = []
    for a in range(size_a):
        is_ocean = True
        for b in range(first_b, last_b, step_b):
            coords = (b, a)
            if is_x_first:
                coords = (a, b)
            color = mapa.getpixel(coords)
            if color == LAND_COLOR:
                is_ocean = False
                continue
            if is_ocean:
                continue
            available_spaces.append(coords)
            is_ocean = True
    return available_spaces


def get_available_coords(mapa: Image.Image) -> list[tuple[int, int]]:
    tamanho = mapa.size
    available_spaces: list[tuple[int, int]] = []
    available_spaces += find_available_land(True, tamanho[0], (0, tamanho[1], 1), mapa)
    available_spaces += find_available_land(True, tamanho[0], (tamanho[1] - 1, -1, -1), mapa)
    available_spaces += find_available_land(False, tamanho[1], (0, tamanho[0], 1), mapa)
    available_spaces += find_available_land(False, tamanho[1], (tamanho[0] - 1, -1, -1), mapa)
    unique_spaces: list[tuple[int, int]] = []
    for coord in available_spaces:
        if coord not in unique_spaces:
            unique_spaces.append(coord)
    return unique_spaces

def get_user_int(prompt: str, default: int) -> int:
    print(prompt)
    try:
        value = int(input())
        if value <= 0:
            return default
        return value
    except:
        return default


def main() -> None:
    while True:
        print("\nenter the data to create the map\n")
        print("map name")
        name = input()
        width = get_user_int("width", DEFAULT_WIDTH)
        height = get_user_int("height", DEFAULT_HEIGHT)
        seed = get_user_int("seed", DEFAULT_SEED)
        land_percentage = get_user_int("land coverage percentage", DEFAULT_PERCENTAGE)
        if land_percentage > MAX_LAND_PERCENTAGE:
            land_percentage = MAX_LAND_PERCENTAGE
        if seed >= width * height * land_percentage / 100:
            seed = DEFAULT_SEED
        size = (width, height)
        map_image = Image.new("RGBA", size, OCEAN_COLOR)
        land_count = seed
        seed_map_with_land(width, height, land_count, map_image)
        os.makedirs(name)
        map_image.save(os.path.join(name, "map_0.png"))
        map_iteration = 1
        map_area = width * height
        percentages = make_percentages(land_count, map_area)
        land_coverage = percentages[1]
        while land_coverage < MAX_LAND_PERCENTAGE:
            for terrain_patch in get_available_coords(map_image):
                if choose_is_land(percentages):
                    map_image.putpixel(terrain_patch, LAND_COLOR)
                    land_count += 1
            percentages = make_percentages(land_count, map_area)
            land_coverage = percentages[1]
            print(f"map : {map_iteration}\npercentage : {land_coverage}%\n")
            map_image.save(os.path.join(name, f"map_{map_iteration}.png"))
            map_iteration += 1
        print("\nmap done!!\n")
        print("to exit, type 0")
        if input() == "0":
            break

def make_percentages(land_count: int, total_area: int) -> tuple[float, float]:
    land_percentage = (land_count * 100) / total_area
    ocean_percentage = 100 - land_percentage
    return (ocean_percentage, land_percentage)

def choose_is_land(percentages: tuple[float, float]) -> int:
    return random.choices([0, 1], percentages)[0]

def seed_map_with_land(width: int, height: int, seed: int, map_image: Image.Image) -> None:
    for _ in range(seed):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        map_image.putpixel((x, y), LAND_COLOR)


if __name__ == "__main__":
    main()