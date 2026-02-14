from os import listdir
from PIL import Image
from time import time

# this script is an attempt to map game levels gameplays into a single level map image. biggest enemy: parallax. I never made it work, but it was fun to try. maybe one day i will try again with a better approach, but for now, this is the code that i have.

#TODO: ugly code. make it better, faster, stronger. (quote by daft punk)

PIXEL_CHANNELS = 4
MAX_BRIGHTNESS = 255
VIDEO_FOLDER = "./video"
FRAMES_FOLDER = f"{VIDEO_FOLDER}/"
SEARCH_DISTANCE_DEFAULT = 20
BACKGROUND_COLOR = (255, 255, 255, 0)

CoordData = tuple[int, int]
PixelData = tuple[int, ...]


def get_pixel(image: Image.Image, coord: CoordData) -> PixelData:
    pixel = image.getpixel(coord)
    if pixel is None:
        raise ValueError("Pixel not found")
    if isinstance(pixel, int):
        raise ValueError("Image is not in RGB mode")
    if isinstance(pixel, float):
        raise ValueError("Image is not in RGB mode")
    if len(pixel) < 4:
        raise ValueError("Image is not in RGB mode")
    return pixel


class SearchConfig:
    def __init__(self, search_distance: int) -> None:
        self.set_distance(search_distance)

    def set_distance(self, search_distance: int) -> None:
        self.search_distance = search_distance
        self.total_distance = search_distance * 2 + 1
        self.step_y = self.total_distance
        self.step_x = self.total_distance

    def get_values(self) -> tuple[int, int, int, int]:
        return self.search_distance, self.total_distance, self.step_y, self.step_x


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
    print(f"{sign}{', '.join(parts)}")


def open_frame(image_path: str) -> Image.Image:
    with Image.open(image_path) as image:
        image_in_memory = image.copy()
        if image.mode != "RGBA":
            return image_in_memory.convert("RGBA")
        return image_in_memory


def calculate_pixel_similarity(pixel_a: PixelData, pixel_b: PixelData) -> float:
    total = 1.0
    for pixel_channel in range(PIXEL_CHANNELS):
        distance = abs(pixel_a[pixel_channel] - pixel_b[pixel_channel])
        similarity_ratio = 1 - distance / MAX_BRIGHTNESS
        total *= similarity_ratio
    return total


def find_optimal_index(
    approved_similarity: list[list[float]],
    totals: list[list[int]],
    search_config: SearchConfig,
) -> CoordData:
    search_distance, _, step_y, step_x = search_config.get_values()
    max_value = 0.0
    max_index = (search_distance, search_distance)
    for x in range(step_x):
        x_offset = x - step_x
        similarity_row = approved_similarity[x]  # optimization
        totals_row = totals[x]  # optimization
        for y in range(step_y):
            y_offset = y - step_y
            value = similarity_row[y] / totals_row[y]
            if value >= max_value:
                max_value = value
                max_index = (x_offset, y_offset)
    return max_index


def compare_frames(
    mapa: Image.Image,
    frame: Image.Image,
    posicao: CoordData,
    search_config: SearchConfig,
) -> CoordData:
    search_distance, total_distance, step_y, step_x = search_config.get_values()
    approved_similarity = [
        [0.0 for _ in range(total_distance)] for _ in range(total_distance)
    ]
    totals = [[0 for _ in range(total_distance)] for _ in range(total_distance)]
    for y in range(0, frame.size[1], step_y):
        for x in range(0, frame.size[0], step_x):
            current_pixel = get_pixel(frame, (x, y))
            if current_pixel[2] == max(current_pixel):
                continue
            for vertical_offset in range(-search_distance, search_distance + 1):
                y_offset = posicao[1] + y + vertical_offset
                if y_offset < 0:
                    continue
                if y_offset >= mapa.size[1]:
                    break
                for horizontal_offset in range(-search_distance, search_distance + 1):
                    x_offset = posicao[0] + x + horizontal_offset
                    if x_offset < 0:
                        continue
                    if x_offset >= mapa.size[0]:
                        break
                    reference_pixel = get_pixel(mapa, (x_offset, y_offset))
                    if reference_pixel[2] != max(reference_pixel):
                        horizontal_index = horizontal_offset + search_distance
                        vertical_index = vertical_offset + search_distance
                        similarity = calculate_pixel_similarity(
                            current_pixel, reference_pixel
                        )
                        approved_similarity[horizontal_index][vertical_index] += (
                            similarity
                        )
                        totals[horizontal_index][vertical_index] += 1
    indice = find_optimal_index(approved_similarity, totals, search_config)
    return indice


def expand_map(
    source_map: Image.Image,
    expansion_image: Image.Image,
    current_coordinates: CoordData,
    position_adjustment: CoordData,
) -> tuple[Image.Image, CoordData]:
    map_size = source_map.size
    expansion_size = expansion_image.size
    new_x = current_coordinates[0] + position_adjustment[0]
    new_y = current_coordinates[1] + position_adjustment[1]
    new_coord = (new_x, new_y)
    if min(new_coord) >= 0:
        new_size = list(map_size).copy()
        for a in range(2):
            if new_coord[a] + expansion_size[a] > map_size[a]:
                new_size[a] = new_coord[a] + expansion_size[a]
        new_size_tuple = tuple(new_size)
        assert len(new_size_tuple) == 2
        new_map = Image.new("RGBA", new_size_tuple, BACKGROUND_COLOR)
        new_map.paste(source_map, (0, 0))
        transparent_expansion = Image.new("RGBA", new_map.size, BACKGROUND_COLOR)
        transparent_expansion.paste(expansion_image, new_coord)
        new_map = Image.alpha_composite(transparent_expansion, new_map)
        return (new_map, new_coord)
    new_size = list(map_size).copy()
    for a in range(2):
        if new_coord[a] < 0:
            new_size[a] = map_size[a] - new_coord[a]
        else:
            new_size[a] = new_coord[a] + expansion_size[a]
    new_size_tuple = tuple(new_size)
    assert len(new_size_tuple) == 2
    new_map = Image.new("RGBA", new_size_tuple, BACKGROUND_COLOR)
    adjusted_coord = list(new_coord).copy()
    for a in range(2):
        if adjusted_coord[a] < 0:
            adjusted_coord[a] = 0
    for a in range(2):
        if adjusted_coord[a] > 0:
            adjusted_coord[a] = 0
        else:
            adjusted_coord[a] -= position_adjustment[a]
    adjusted_coord_tuple = tuple(adjusted_coord)
    assert len(adjusted_coord_tuple) == 2
    new_map.paste(source_map, adjusted_coord_tuple)
    transparent_expansion = Image.new("RGBA", new_map.size, BACKGROUND_COLOR)
    transparent_expansion.paste(expansion_image, new_coord)
    new_map = Image.alpha_composite(transparent_expansion, new_map)
    return (new_map, new_coord)


def main() -> None:
    search_config = SearchConfig(SEARCH_DISTANCE_DEFAULT)
    total_start_time = time()
    image_map = open_frame(f"{FRAMES_FOLDER}{listdir(VIDEO_FOLDER)[0]}")
    coord = (0, 0)
    start_time = time()
    total_frame_count = len(listdir(VIDEO_FOLDER))
    for n, frame in enumerate(listdir(VIDEO_FOLDER)):
        current_frame = open_frame(f"{FRAMES_FOLDER}{frame}")
        position_adjustments = compare_frames(
            image_map, current_frame, coord, search_config
        )
        while (
            max([abs(a) for a in position_adjustments]) == search_config.search_distance
        ):
            search_distance = max([abs(a) for a in position_adjustments]) + 1
            search_config.set_distance(search_distance)
            print(f"new search distance : {search_distance}")
            position_adjustments = compare_frames(
                image_map, current_frame, coord, search_config
            )
        image_map, coord = expand_map(
            image_map, current_frame, coord, position_adjustments
        )
        fim = time()
        duracao = fim - start_time
        start_time = time()
        print(f"{n} : ")
        print_elapsed_time(duracao * (total_frame_count - n))
        image_map.save("mapa.png")
    fimTotal = time()
    duracao = fimTotal - total_start_time
    print_elapsed_time(duracao)
    image_map.save("mapa.png")


if __name__ == "__main__":
    main()
