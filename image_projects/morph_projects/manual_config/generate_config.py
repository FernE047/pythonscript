from enum import Enum
from math import sqrt
from PIL import Image
import os
import multiprocessing

CoordData = tuple[int, int]

SOURCE_FOLDER = "./parts/source"
TARGET_FOLDER = "./parts/target"
CONFIG_FOLDER = "./parts/config"
ROUNDING_EPSILON = 0.1
# euclidean distance plus a small margin
NEIGHBORS_MINIMUM_DISTANCE = sqrt(2) + ROUNDING_EPSILON
# arbitrary value to avoid connecting distant points in circular lines
NEIGHBORS_MINIMUM_DISTANCE_INDEXED = 5
# another arbitrary value to limit sorting attempts, or else we would have O(n^2)
SORTING_MINIMUM_ATTEMPTS = 4
LAYER_COUNT = 4
SMALL_PERIMETER_MAX = LAYER_COUNT
NO_SCORE_YET = float("inf")
VERTICAL_PARTITION_PARITY = 0
# Transversal order to process regions and layers, idk why but it works
REGIONS_TRANSVERSAL_ORDER = (0, 2, 1, 3)
# Layers transversal order to process regions and layers, idk why but it works
LAYERS_TRANSVERSAL_ORDER = (0, 3, 2, 1)
MAX_BRIGHTNESS = 255
MIN_BRIGHTNESS = 0
ALPHA_CHANNEL = 3
RED_CHANNEL = 0
BLUE_CHANNEL = 2
SPECIAL_BLUE_BRIGHTNESS = 200


def get_pixel(image: Image.Image, coord: CoordData) -> tuple[int, ...]:
    pixel = image.getpixel(coord)
    if pixel is None:
        raise ValueError("Pixel not found")
    if isinstance(pixel, int):
        raise ValueError("Image is not in RGBA mode")
    if isinstance(pixel, float):
        raise ValueError("Image is not in RGBA mode")
    if len(pixel) < 4:
        raise ValueError("Image is not in RGBA mode")
    return pixel


class Direction(Enum):
    DOWN_RIGHT = 0
    DOWN = 1
    DOWN_LEFT = 2
    LEFT = 3
    UP_LEFT = 4
    UP = 5
    UP_RIGHT = 6
    RIGHT = 7


ORTHOGONAL_DIRECTIONS = (Direction.DOWN, Direction.LEFT, Direction.UP, Direction.RIGHT)


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


def open_image_as_rgba(image_path: str) -> Image.Image:
    with Image.open(image_path) as image:
        image_in_memory = image.copy()
        if image.mode != "RGBA":
            return image_in_memory.convert("RGBA")
        return image_in_memory


class Line:
    def __init__(
        self, coordinates: list[CoordData] | None = None, is_cyclic: bool = False
    ) -> None:
        self.is_cyclic = is_cyclic
        if coordinates is None:
            self.coordinates: list[CoordData] = []
            self.start_coordinate = None
            self.end_coordinate = None
            return
        self.coordinates = coordinates.copy()
        if len(self.coordinates) == 0:
            self.start_coordinate = None
            self.end_coordinate = None
            return
        self.start_coordinate = self.coordinates[0]
        self.end_coordinate = self.coordinates[-1]

    def search_blue_line(self, image: Image.Image) -> None:
        while True:
            initial_coord = self.end_coordinate
            detected_coordinates: list[CoordData] = []
            for direction in Direction:
                current_coord = apply_direction(initial_coord, direction)
                if current_coord in self:
                    continue
                try:
                    pixel = get_pixel(image, current_coord)
                except IndexError:
                    continue
                if pixel[ALPHA_CHANNEL] == MIN_BRIGHTNESS:
                    continue
                if pixel[BLUE_CHANNEL] == MAX_BRIGHTNESS:
                    detected_coordinates.append(current_coord)
            if len(detected_coordinates) == 1:
                self.append(detected_coordinates[0])
                continue
            for coord in detected_coordinates:
                new_line = self.copy()
                new_line.append(coord)
                new_line.search_blue_line(image)
                if len(new_line) <= len(self):
                    continue
                self.clone(new_line)
            break

    def sort_all(self) -> None:
        lines = self.group_connected_coordinates()
        self.coordinates = []
        for line in lines:
            line.sort()
            new_line = self.add_line(line)
            self.clone(new_line)

    def group_connected_coordinates(self) -> list["Line"]:
        lines: list[Line] = []
        for coord in self.coordinates:
            neighbor_lines: list[int] = []
            for index, line in enumerate(lines):
                for line_coord in line.coordinates:
                    if get_distance(coord, line_coord) > NEIGHBORS_MINIMUM_DISTANCE:
                        continue
                    neighbor_lines.append(index)
                    break
            if len(neighbor_lines) == 0:
                lines.append(Line([coord], is_cyclic=self.is_cyclic))
                continue
            if len(neighbor_lines) == 1:
                lines[neighbor_lines[0]].append(coord)
                continue
            line = lines[neighbor_lines[0]].copy()
            for line_index in neighbor_lines[1:]:
                line = line.add_line(lines[line_index])
            for line_index in reversed(sorted(neighbor_lines)):
                lines.pop(line_index)
            line.append(coord)
            lines.append(line)
        return lines

    def sort(self) -> None:
        length = len(self)
        best_line = Line(is_cyclic=self.is_cyclic)
        for coord_index in range(min(SORTING_MINIMUM_ATTEMPTS, length)):
            test_line = self.copy()
            first_coord = self.coordinates[coord_index]
            test_line.try_to_sort(Line([first_coord], is_cyclic=self.is_cyclic))
            if len(test_line) == length:
                best_line = test_line.copy()
                break
            if len(test_line) <= len(best_line):
                continue
            best_line = test_line.copy()
        self.clone(best_line)

    def try_to_sort(self, ordered_line: "Line") -> None:
        while True:
            first_coord = ordered_line.coordinates[-1]
            coords = self.get_neighbor_coords(first_coord, exceptions=ordered_line)
            if len(coords) == 1:
                ordered_line.append(coords[0])
                continue
            if len(coords) == 0:
                if not self.is_cyclic:
                    best_line = ordered_line.copy()
                    continue
                index = self.coordinates.index(first_coord)
                if index < len(self) - 1:
                    ordered_line.append(self.coordinates[index + 1])
                    continue
                best_line = ordered_line.copy()
                continue
            initial_length = len(ordered_line)
            for coord in coords:
                neighbor_coords = self.get_neighbor_coords(
                    coord, exceptions=ordered_line
                )
                if len(neighbor_coords) != 1:
                    continue
                if neighbor_coords[0] in coords:
                    ordered_line.append(coord)
                    ordered_line.append(neighbor_coords[0])
                    break
            if len(ordered_line) != initial_length:
                continue
            best_line = ordered_line.copy()
            for coord in coords:
                new_line = self.copy()
                new_line.try_to_sort(ordered_line.add_coords([coord]))
                if len(new_line) == len(self):
                    best_line = new_line.copy()
                    break
                if len(new_line) > len(best_line):
                    best_line = new_line.copy()
            break
        self.clone(best_line)

    def get_neighbor_coords(
        self, origin_coord: CoordData, exceptions: "Line | None" = None
    ) -> list[CoordData]:
        if exceptions is None:
            exceptions = Line()
        coords: list[CoordData] = []
        for direction in Direction:
            current_coord = apply_direction(origin_coord, direction)
            if current_coord not in self:
                continue
            if current_coord in exceptions:
                continue
            if not self.is_cyclic:
                coords.append(current_coord)
                continue
            current_index = self.coordinates.index(current_coord)
            origin_index = self.coordinates.index(origin_coord)
            distance = abs(current_index - origin_index)
            if distance < NEIGHBORS_MINIMUM_DISTANCE_INDEXED:
                coords.append(current_coord)
        return coords

    def split_into_partitions(self, start_index: int) -> list["Line"]:
        partition_sizes = [0] * LAYER_COUNT
        for index in range(len(self)):
            partition_sizes[index % LAYER_COUNT] += 1
        lines: list[Line] = []
        for index in range(LAYER_COUNT):
            current_line = Line(is_cyclic=self.is_cyclic)
            partition_start = start_index + sum(partition_sizes[:index])
            partition_end = partition_start + partition_sizes[index]
            for coord in self.coordinates[partition_start:partition_end]:
                current_line.append(coord)
            if index == LAYER_COUNT - 1:
                for coord in self.coordinates[:start_index]:
                    current_line.append(coord)
            lines.append(current_line)
        return lines

    def turn_into_layers(self) -> list["Line"]:
        perimeter = len(self)
        layer_section_size = int((perimeter - ROUNDING_EPSILON) // LAYER_COUNT + 1)
        if perimeter <= SMALL_PERIMETER_MAX:
            best_layers: list[Line] = []
            for index in range(perimeter):
                best_layers.append(
                    Line([self.coordinates[index]], is_cyclic=self.is_cyclic)
                )
            while len(best_layers) != LAYER_COUNT:
                best_layers.append(
                    Line([self.coordinates[-1]], is_cyclic=self.is_cyclic)
                )
            return best_layers
        best_layers = []
        best_score = NO_SCORE_YET
        for start_section in range(layer_section_size):
            new_layers = self.split_into_partitions(start_section)
            bottommost_y = new_layers[0].calculate_mid_coord()[1]
            bottom_line = new_layers[0]
            for layer_index in range(1, LAYER_COUNT):
                if new_layers[layer_index].calculate_mid_coord()[1] <= bottommost_y:
                    continue
                bottommost_y = new_layers[layer_index].calculate_mid_coord()[1]
                bottom_line = new_layers[layer_index]
            while new_layers[0] != bottom_line:
                new_layers = [new_layers[-1]] + new_layers
                new_layers.pop()
            score = 0
            for index in range(LAYER_COUNT):
                current_layer = new_layers[index]
                first_index = current_layer.coordinates[0]
                last_index = current_layer.coordinates[-1]
                if index % 2 == VERTICAL_PARTITION_PARITY:
                    first_y = first_index[1]
                    last_y = last_index[1]
                    score += abs(last_y - first_y)
                else:
                    first_x = first_index[0]
                    last_x = last_index[0]
                    score += abs(last_x - first_x)
            if score < best_score:
                best_layers = new_layers.copy()
                best_score = score
        if (
            best_layers[1].calculate_mid_coord()[0]
            <= best_layers[3].calculate_mid_coord()[0]
        ):
            return best_layers
        new_layers = [best_layers[a] for a in LAYERS_TRANSVERSAL_ORDER]
        for line in best_layers:
            line.coordinates = list(reversed(line.coordinates))
            line.start_coordinate = line.coordinates[0]
            line.end_coordinate = line.coordinates[-1]
        return new_layers

    def calculate_mid_coord(self) -> CoordData:
        x = 0
        y = 0
        for coordinate in self.coordinates:
            x += coordinate[0]
            y += coordinate[1]
        average_x = x // len(self)
        average_y = y // len(self)
        return (average_x, average_y)

    def to_config(self, other: "Line") -> str:
        def format_coordinate(coord: CoordData) -> str:
            return f"{coord[0]},{coord[1]}"

        def format_line(coord_a: CoordData, coord_b: CoordData) -> str:
            return f"{format_coordinate(coord_a)} {format_coordinate(coord_b)}\n"

        text = ""
        if len(self) == len(other):
            for coord_source, coord_target in zip(self.coordinates, other.coordinates):
                text += format_line(coord_source, coord_target)
            return text
        line_source = self
        line_target = other
        if len(self) < len(other):
            line_source = other
            line_target = self
        coordinate_ratio = 0.0
        if len(line_source) - 1 == 0:
            coordinate_ratio = (len(line_target) - 1) / (len(line_source) - 1)
        for source_index, coord_source in enumerate(line_source.coordinates):
            target_index = int(source_index * coordinate_ratio)
            coord_target = line_target.coordinates[target_index]
            text += format_line(coord_source, coord_target)
        return text

    def clone(self, other: "Line") -> "Line":
        self.coordinates = other.coordinates.copy()
        self.start_coordinate = other.start_coordinate
        self.end_coordinate = other.end_coordinate
        self.is_cyclic = other.is_cyclic
        return self

    def copy(self) -> "Line":
        return Line(self.coordinates.copy(), is_cyclic=self.is_cyclic)

    def append(self, elemento: "Line | CoordData") -> None:
        if isinstance(elemento, Line):
            for ponto in elemento.coordinates:
                self.append(ponto)
            return
        self.coordinates.append(elemento)
        self.end_coordinate = elemento
        if self.start_coordinate is None:
            self.start_coordinate = elemento

    def __contains__(self, elemento: "CoordData") -> bool:
        if elemento in self.coordinates:
            return True
        return False

    def add_line(self, other_line: "Line") -> "Line":
        new_line = self.copy()
        new_line.coordinates += other_line.coordinates
        return new_line

    def add_coords(self, other_coords: list[CoordData]) -> "Line":
        new_line = self.copy()
        for element in other_coords:
            new_line.coordinates.append(element)
        return new_line

    def __len__(self) -> int:
        return len(self.coordinates)

    def __str__(self) -> str:
        return str(self.coordinates)


class Area:
    def __init__(self, image: Image.Image, starting_line: "Line | None" = None) -> None:
        self.image = image
        self.lines: list[Line] = []
        if starting_line is None:
            self.is_cyclic = True
            self.search_green_contour()
        else:
            self.is_cyclic = False
            self.lines.append(starting_line)
        self.search_for_lines()

    def search_green_contour(self) -> None:
        contour: list[CoordData] = []
        width, height = self.image.size
        for y in range(height):
            was_last_pixel_opaque = False
            for x in range(width):
                pixel = get_pixel(self.image, (x, y))
                is_current_pixel_opaque = pixel[ALPHA_CHANNEL] == MAX_BRIGHTNESS
                if not was_last_pixel_opaque ^ is_current_pixel_opaque:
                    was_last_pixel_opaque = is_current_pixel_opaque
                    continue
                coord = (x - 1, y)
                if is_current_pixel_opaque:
                    coord = (x, y)
                if coord not in contour:
                    contour.append(coord)
                was_last_pixel_opaque = is_current_pixel_opaque
            if was_last_pixel_opaque:
                coord = (width - 1, y)
                if coord not in contour:
                    contour.append(coord)
        for x in range(width):
            was_last_pixel_opaque = False
            for y in range(height):
                pixel = get_pixel(self.image, (x, y))
                is_current_pixel_opaque = pixel[ALPHA_CHANNEL] == MAX_BRIGHTNESS
                if not was_last_pixel_opaque ^ is_current_pixel_opaque:
                    was_last_pixel_opaque = is_current_pixel_opaque
                    continue
                coord = (x, y - 1)
                if is_current_pixel_opaque:
                    coord = (x, y)
                if coord not in contour:
                    contour.append(coord)
                was_last_pixel_opaque = is_current_pixel_opaque
            if was_last_pixel_opaque:
                coord = (x, height - 1)
                if coord not in contour:
                    contour.append(coord)
        initial_contour_line = Line(contour)
        initial_contour_line.sort_all()
        layers = initial_contour_line.turn_into_layers()
        initial_contour_line = layers[0]
        for indice in range(1, LAYER_COUNT):
            initial_contour_line.append(layers[indice])
        self.lines.append(initial_contour_line)

    def search_for_lines(self) -> None:
        previous_line_count = len(self.lines)
        while True:
            self.find_lines()
            current_line_count = len(self.lines)
            if current_line_count == previous_line_count:
                break
            previous_line_count = current_line_count

    def find_lines(self) -> None:
        current_line = Line()
        previous_line = self.lines[-1]
        for previous_coord in previous_line.coordinates:
            for direction in ORTHOGONAL_DIRECTIONS:
                current_coord = apply_direction(previous_coord, direction)
                try:
                    pixel = get_pixel(self.image, current_coord)
                except IndexError:
                    continue
                if pixel[ALPHA_CHANNEL] == 0:
                    continue
                if current_coord in current_line:
                    continue
                if current_coord in self:
                    continue
                current_line.append(current_coord)
        if len(current_line) > 0:
            current_line.sort_all()
            self.lines.append(current_line)

    def to_config(self, other: "Area") -> str:
        text = ""
        if len(self) == len(other):
            for line_source, line_target in zip(self.lines, other.lines):
                text += line_source.to_config(line_target)
            return text
        area_source = self
        area_target = other
        if len(self) < len(other):
            area_source = other
            area_target = self
        line_ratio = 0.0
        if len(area_source) - 1 == 0:
            line_ratio = (len(area_target) - 1) / (len(area_source) - 1)
        for source_index, line_source in enumerate(area_source.lines):
            target_index = int(source_index * line_ratio)
            line_target = area_target.lines[target_index]
            text += line_source.to_config(line_target)
        return text

    def __contains__(self, other: CoordData) -> bool:
        for line in self.lines:
            if other in line:
                return True
        return False

    def __len__(self) -> int:
        return len(self.lines)


class AreaRed:
    def __init__(self, image: Image.Image) -> None:
        self.image = image
        self.layer_regions: list[list[Line]] = []
        self.search_contour()
        self.search_for_layers()

    def search_contour(self) -> None:
        contour: list[CoordData] = []
        width, height = self.image.size
        for y in range(height):
            was_last_pixel_opaque = False
            for x in range(width):
                pixel = get_pixel(self.image, (x, y))
                is_current_pixel_opaque = pixel[ALPHA_CHANNEL] == MAX_BRIGHTNESS
                if not was_last_pixel_opaque ^ is_current_pixel_opaque:
                    was_last_pixel_opaque = is_current_pixel_opaque
                    continue
                coord = (x - 1, y)
                if is_current_pixel_opaque:
                    coord = (x, y)
                if coord not in contour:
                    contour.append(coord)
                was_last_pixel_opaque = is_current_pixel_opaque
            if was_last_pixel_opaque:
                coord = (width - 1, y)
                if coord not in contour:
                    contour.append(coord)
        for x in range(width):
            was_last_pixel_opaque = False
            for y in range(height):
                pixel = get_pixel(self.image, (x, y))
                is_current_pixel_opaque = pixel[ALPHA_CHANNEL] == MAX_BRIGHTNESS
                if not was_last_pixel_opaque ^ is_current_pixel_opaque:
                    was_last_pixel_opaque = is_current_pixel_opaque
                    continue
                coord = (x, y - 1)
                if is_current_pixel_opaque:
                    coord = (x, y)
                if coord not in contour:
                    contour.append(coord)
                was_last_pixel_opaque = is_current_pixel_opaque
            if was_last_pixel_opaque:
                coord = (x, height - 1)
                if coord not in contour:
                    contour.append(coord)
        initial_contour_line = Line(contour)
        initial_contour_line.sort()
        layers = initial_contour_line.turn_into_layers()
        for line in layers:
            self.layer_regions.append([line])

    def search_for_layers(self) -> None:
        previous_layer_count = len(self.layer_regions)
        while True:
            self.find_layers()
            current_layer_count = len(self.layer_regions)
            if current_layer_count == previous_layer_count:
                break
            previous_layer_count = current_layer_count

    def find_layers(self) -> None:
        for layer_index in LAYERS_TRANSVERSAL_ORDER:
            current_line = Line(is_cyclic=True)
            previous_line = self.layer_regions[layer_index][-1]
            for previous_coord in previous_line.coordinates:
                for direction in ORTHOGONAL_DIRECTIONS:
                    current_coord = apply_direction(previous_coord, direction)
                    try:
                        pixel = get_pixel(self.image, current_coord)
                    except IndexError:
                        continue
                    if pixel[ALPHA_CHANNEL] == 0:
                        continue
                    if current_coord in current_line:
                        continue
                    if current_coord in self:
                        continue
                    current_line.append(current_coord)
            if len(current_line) == 0:
                continue
            current_line.sort_all()
            self.layer_regions[layer_index].append(current_line)

    def to_config(self, other: "AreaRed") -> str:
        text = ""
        for region_index in range(LAYER_COUNT):
            self_layer = self.layer_regions[region_index]
            other_layer = other.layer_regions[region_index]
            if len(self_layer) == len(other_layer):
                for line_source, line_target in zip(self_layer, other_layer):
                    text += line_source.to_config(line_target)
                continue
            layer_source = self_layer
            layer_target = other_layer
            if len(self_layer) < len(other_layer):
                layer_source = other_layer
                layer_target = self_layer
            layer_ratio = 0.0
            if len(layer_source) - 1 != 0:
                layer_ratio = (len(layer_target) - 1) / (len(layer_source) - 1)
            for source_index, line_source in enumerate(layer_source):
                target_index = int(source_index * layer_ratio)
                line_target = layer_target[target_index]
                text += line_source.to_config(line_target)
        return text

    def __contains__(self, other: CoordData) -> bool:
        for region in self.layer_regions:
            for line in region:
                if other in line:
                    return True
        return False

    def __len__(self) -> int:
        return len(self.layer_regions)


class ImagePart:
    area: Area | AreaRed
    has_blue: bool
    has_red: bool
    blue_coord: CoordData

    def __init__(self, nome: str) -> None:
        image = open_image_as_rgba(nome)
        self.search_colors(image)
        if self.has_red:
            self.area = AreaRed(image)
        elif self.has_blue:
            line = Line([self.blue_coord])
            line.search_blue_line(image)
            self.area = Area(image, starting_line=line)
        else:
            self.area = Area(image)

    def search_colors(self, image: Image.Image) -> None:
        width, height = image.size
        self.has_red = False
        self.has_blue = False
        for x in range(width):
            for y in range(height):
                pixel = get_pixel(image, (x, y))
                if pixel[ALPHA_CHANNEL] == 0:
                    continue
                if pixel[RED_CHANNEL] == MAX_BRIGHTNESS:
                    self.has_red = True
                    return
                if pixel[BLUE_CHANNEL] == SPECIAL_BLUE_BRIGHTNESS:
                    self.has_blue = True
                    self.blue_coord = (x, y)
                    return

    def to_config(self, other: "ImagePart") -> str:
        if isinstance(self.area, Area) and isinstance(other.area, Area):
            return self.area.to_config(other.area)
        if isinstance(self.area, AreaRed) and isinstance(other.area, AreaRed):
            return self.area.to_config(other.area)
        raise Exception("Imagens incompatíveis para escrita")


def get_distance(coords_a: tuple[int, int], coords_b: tuple[int, int]) -> float:
    accumulator = 0
    for coord_a, coord_b in zip(coords_a, coords_b):
        accumulator += abs(coord_a - coord_b) ** 2
    return sqrt(accumulator)


def configPart(part_index: int) -> None:
    print(f"Processing Part : {part_index}")
    file_name = f"{part_index:03d}"
    image_name = f"{file_name}.png"
    source_part = ImagePart(f"{SOURCE_FOLDER}/{image_name}")
    target_part = ImagePart(f"{TARGET_FOLDER}/{image_name}")
    config_name = f"{CONFIG_FOLDER}/{file_name}.txt"
    with open(config_name, "w", encoding="utf-8") as file_config:
        config = source_part.to_config(target_part)
        file_config.write(config)
        print(f"\tPart Completed : {part_index}")


def main() -> None:
    total_parts = len(os.listdir(TARGET_FOLDER))
    with multiprocessing.Pool(os.cpu_count()) as cpu_pool:
        cpu_pool.map(configPart, range(total_parts))


if __name__ == "__main__":
    main()
