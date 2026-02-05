from enum import Enum
from io import TextIOWrapper
from math import sqrt
from PIL import Image

FIRST_IMAGE_PATH = "./inicial.png"
LAST_IMAGE_PATH = "./final.png"
CONFIG_FILE_PATH = "./config.txt"
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
OPAQUE_ALPHA_VALUE = 255
TRANSPARENT_ALPHA_VALUE = 0

CoordData = tuple[int, int]
LayerData = list["Line"]


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


def apply_direction(coord: CoordData, direction: Direction) -> CoordData:
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


def get_distance(coords_a: tuple[int, int], coords_b: tuple[int, int]) -> float:
    soma = 0
    for coord_a, coord_b in zip(coords_a, coords_b):
        soma += abs(coord_a - coord_b) ** 2
    return sqrt(soma)


def is_neighbors(coord_a: CoordData, coord_b: CoordData) -> bool:
    return get_distance(coord_a, coord_b) <= NEIGHBORS_MINIMUM_DISTANCE


def get_pixel_alpha(pixel: float | tuple[int, ...] | None) -> int:
    if pixel is None:
        return TRANSPARENT_ALPHA_VALUE
    if isinstance(pixel, int):
        return OPAQUE_ALPHA_VALUE
    if isinstance(pixel, float):
        return OPAQUE_ALPHA_VALUE
    if len(pixel) == 4:
        return pixel[3]
    return OPAQUE_ALPHA_VALUE


class Line:
    def __init__(
        self, coordinates: list[CoordData] | None = None, is_circular: bool = False
    ) -> None:
        self.coordinates: list[CoordData] = []
        if coordinates is not None:
            self.coordinates = coordinates.copy()
        self.is_circular = is_circular

    def sort_all_coordinates(self) -> None:
        line_groups = self.group_connected_coordinates()
        self.coordinates = []
        for line_group in line_groups:
            line_group.sort()
            new_line = self.add_line(line_group)
            self.clone(new_line)

    def group_connected_coordinates(self) -> list["Line"]:
        lines: list["Line"] = []
        for coord in self.coordinates:
            neighbor_lines: list[int] = []
            for line_index, line in enumerate(lines):
                for line_coord in line.coordinates:
                    if is_neighbors(coord, line_coord):
                        neighbor_lines.append(line_index)
                        break
            if len(neighbor_lines) == 0:
                lines.append(Line([coord], is_circular=self.is_circular))
                continue
            if len(neighbor_lines) == 1:
                lines[neighbor_lines[0]].append(coord)
                continue
            line = lines[neighbor_lines[0]].copy()
            for line_index in neighbor_lines[1:]:
                line.add_line(lines[line_index])
            for line_index in reversed(sorted(neighbor_lines)):
                lines.pop(line_index)
            line.append(coord)
            lines.append(line)
        return lines

    def sort(self) -> None:
        length = len(self)
        best_line = Line(is_circular=self.is_circular)
        for n in range(min(SORTING_MINIMUM_ATTEMPTS, length)):
            test_line = self.copy()
            first_coordinate = self.coordinates[n]
            test_line.try_to_sort(
                Line([first_coordinate], is_circular=self.is_circular)
            )
            if len(test_line) == length:
                best_line = test_line.copy()
                break
            if len(test_line) > len(best_line):
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
                if not self.is_circular:
                    best_line = ordered_line.copy()
                    break
                index = self.coordinates.index(first_coord)
                if index == len(self) - 1:
                    best_line = ordered_line.copy()
                    break
                ordered_line.append(self.coordinates[index + 1])
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
        self,
        origin_coord: CoordData,
        exceptions: "Line | list[CoordData] | None" = None,
    ) -> list[CoordData]:
        if exceptions is None:
            exceptions = []
        coords: list[CoordData] = []
        origin_index = self.coordinates.index(origin_coord)
        for direction in Direction:
            current_coord = apply_direction(origin_coord, direction)
            if current_coord not in self:
                continue
            current_index = self.coordinates.index(current_coord)
            if current_coord in exceptions:
                continue
            if not self.is_circular:
                coords.append(current_coord)
                continue
            if abs(current_index - origin_index) < NEIGHBORS_MINIMUM_DISTANCE_INDEXED:
                coords.append(current_coord)
        return coords

    def split_into_partitions(
        self, partition_count: int, start_index: int
    ) -> LayerData:
        partition_sizes = [0] * partition_count
        for index in range(len(self)):
            partition_sizes[index % partition_count] += 1
        lines: list[Line] = []
        for index in range(partition_count):
            current_line = Line(is_circular=self.is_circular)
            partition_start = start_index + sum(partition_sizes[:index])
            partition_end = partition_start + partition_sizes[index]
            for coord in self.coordinates[partition_start:partition_end]:
                current_line.append(coord)
            if index == partition_count - 1:
                for coord in self.coordinates[:start_index]:
                    current_line.append(coord)
            lines.append(current_line)
        return lines

    def turn_into_layers(self) -> LayerData:
        perimeter = len(self)
        layer_section_size = int((perimeter - ROUNDING_EPSILON) // LAYER_COUNT + 1)
        if perimeter <= SMALL_PERIMETER_MAX:
            best_layers: LayerData = []
            for index in range(perimeter):
                best_layers.append(
                    Line([self.coordinates[index]], is_circular=self.is_circular)
                )
            while len(best_layers) != LAYER_COUNT:
                best_layers.append(
                    Line([self.coordinates[-1]], is_circular=self.is_circular)
                )
            return best_layers
        best_layers = []
        best_score = NO_SCORE_YET
        for start_section in range(layer_section_size):
            new_layers = self.split_into_partitions(LAYER_COUNT, start_section)
            first_layer = new_layers[0]
            bottommost_y = first_layer.calculate_mid_coord()[1]
            bottom_line = first_layer
            for layer_index in range(1, LAYER_COUNT):
                current_layer = new_layers[layer_index]
                current_y = current_layer.calculate_mid_coord()[1]
                if current_y <= bottommost_y:  # y increases downwards
                    continue
                bottommost_y = current_y
                bottom_line = current_layer
            while first_layer != bottom_line:  # TODO: implement __ne__ between Lines
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
        new_layers = [best_layers[a] for a in (0, 3, 2, 1)]
        for line in best_layers:
            line.coordinates = list(reversed(line.coordinates))
        return new_layers

    def calculate_mid_coord(self) -> CoordData:
        x = 0
        y = 0
        for coordinate in self.coordinates:
            x += coordinate[0]
            y += coordinate[1]
        average_x_coordinate = x // len(self)
        average_y_coordinate = y // len(self)
        return (average_x_coordinate, average_y_coordinate)

    def write_to_file(self, other_line: "Line", file: TextIOWrapper) -> None:
        def format_coordinate(coord: CoordData) -> str:
            return f"{coord[0]},{coord[1]}"

        def write_line(coord_a: CoordData, coord_b: CoordData) -> None:
            file.write(f"{format_coordinate(coord_a)} {format_coordinate(coord_b)}\n")

        if len(self) == len(other_line):
            for coord_source, coord_target in zip(
                self.coordinates, other_line.coordinates
            ):
                write_line(coord_source, coord_target)
            return
        line_source = self
        line_target = other_line
        if len(self) < len(other_line):
            line_source = other_line
            line_target = self
        coordinate_ratio = 0.0
        if len(line_source) - 1 != 0:
            coordinate_ratio = (len(line_target) - 1) / (len(line_source) - 1)
        for source_index, coord_source in enumerate(line_source.coordinates):
            target_index = int(source_index * coordinate_ratio)
            coord_target = line_target.coordinates[target_index]
            write_line(coord_source, coord_target)

    def copy(self) -> "Line":
        return Line(self.coordinates, is_circular=self.is_circular)

    def clone(self, other: "Line") -> None:
        # clone is different from copy, clone changes the current object
        self.coordinates = other.coordinates.copy()
        self.is_circular = other.is_circular

    def append(self, elemento: "Line | CoordData") -> None:
        if isinstance(elemento, Line):
            for ponto in elemento.coordinates:
                self.append(ponto)
            return
        self.coordinates.append(elemento)

    def __contains__(self, elemento: CoordData) -> bool:
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
    def __init__(self, image: Image.Image) -> None:
        self.image = image
        self.layer_regions: list[list[Line]] = []
        self.search_contour()
        self.search_for_layers()

    def search_contour(self) -> None:
        countour: list[CoordData] = []
        width, height = self.image.size
        for y in range(height):
            was_last_pixel_opaque = False
            for x in range(width):
                pixel = self.image.getpixel((x, y))
                is_current_pixel_opaque = get_pixel_alpha(pixel) == OPAQUE_ALPHA_VALUE
                if not was_last_pixel_opaque ^ is_current_pixel_opaque:
                    was_last_pixel_opaque = is_current_pixel_opaque
                    continue
                coord = (x - 1, y)
                if is_current_pixel_opaque:
                    coord = (x, y)
                if coord not in countour:
                    countour.append(coord)
                was_last_pixel_opaque = is_current_pixel_opaque
            if was_last_pixel_opaque:
                coord = (width - 1, y)
                if coord not in countour:
                    countour.append(coord)
        for x in range(width):
            was_last_pixel_opaque = False
            for y in range(height):
                pixel = self.image.getpixel((x, y))
                is_current_pixel_opaque = get_pixel_alpha(pixel) == OPAQUE_ALPHA_VALUE
                if not was_last_pixel_opaque ^ is_current_pixel_opaque:
                    was_last_pixel_opaque = is_current_pixel_opaque
                    continue
                coord = (x, y - 1)
                if is_current_pixel_opaque:
                    coord = (x, y)
                if coord not in countour:
                    countour.append(coord)
                was_last_pixel_opaque = is_current_pixel_opaque
            if was_last_pixel_opaque:
                coord = (x, height - 1)
                if coord not in countour:
                    countour.append(coord)
        linhaInicial = Line(countour)
        linhaInicial.sort()
        layers = linhaInicial.turn_into_layers()
        for line in layers:
            self.layer_regions.append([line])

    def search_for_layers(self) -> None:
        changed = True
        while changed:
            changed = self.find_layers()

    def find_layers(self) -> bool:
        # try to expand each layer region by finding neighboring pixels
        has_changes_occurred = False
        for region_index in LAYERS_TRANSVERSAL_ORDER:
            current_line = Line(is_circular=True)
            previous_line = self.layer_regions[region_index][-1]
            for previous_coord in previous_line.coordinates:
                for direction in ORTHOGONAL_DIRECTIONS:
                    current_coord = apply_direction(previous_coord, direction)
                    try:
                        pixel = self.image.getpixel(current_coord)
                    except IndexError:
                        continue
                    if get_pixel_alpha(pixel) == TRANSPARENT_ALPHA_VALUE:
                        continue
                    if current_coord in current_line:
                        continue
                    if current_coord not in self:
                        current_line.append(current_coord)
            if len(current_line) == 0:
                continue
            current_line.sort_all_coordinates()
            self.layer_regions[region_index].append(current_line)
            has_changes_occurred = True
        return has_changes_occurred

    def write_region_data(self, other: "Area", file: TextIOWrapper) -> None:
        for indice in range(LAYER_COUNT):
            source_regions = self.layer_regions[indice]
            target_regions = other.layer_regions[indice]
            source_size = len(source_regions)
            target_size = len(target_regions)
            if source_size == target_size:
                for self_line, other_line in zip(source_regions, target_regions):
                    self_line.write_to_file(other_line, file)
                return
            elif source_size > target_size:
                region_scale = 0.0
                if source_size - 1 != 0:
                    region_scale = (target_size - 1) / (source_size - 1)
                for region_index in range(source_size):
                    source_line = source_regions[region_index]
                    target_index = int(region_index * region_scale)
                    target_line = target_regions[target_index]
                    source_line.write_to_file(target_line, file)
                return
            region_scale = 0.0
            if target_size - 1 != 0:
                region_scale = (source_size - 1) / (target_size - 1)
            for region_index in range(target_size):
                source_index = int(region_index * region_scale)
                source_line = source_regions[source_index]
                target_line = target_regions[region_index]
                source_line.write_to_file(target_line, file)

    def __contains__(self, coord: CoordData) -> bool:
        for layer_region in self.layer_regions:
            for layer in layer_region:
                if coord in layer:
                    return True
        return False

    def get_largest_region_size(self) -> int:
        largest_size = float("-inf")
        for layer_region in self.layer_regions:
            if len(layer_region) > largest_size:
                largest_size = len(layer_region)
        return int(largest_size)


def main() -> None:
    print("Fazendo Analise : ")
    initial_image = Image.open(FIRST_IMAGE_PATH)
    initial_area = Area(initial_image)
    initial_image.close()
    last_image = Image.open(LAST_IMAGE_PATH)
    last_area = Area(last_image)
    last_image.close()
    with open(CONFIG_FILE_PATH, "w", encoding="utf-8") as config_file:
        initial_area.write_region_data(last_area, config_file)
        print("\nAnalise Terminada : ")


if __name__ == "__main__":
    main()
