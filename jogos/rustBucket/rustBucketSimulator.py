from enum import Enum
from PIL import Image

#TODO: Constants 

class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3
    UP_RIGHT = 4
    UP_LEFT = 5
    DOWN_RIGHT = 6
    DOWN_LEFT = 7
    DIRECTIONLESS = 8


ACTUAL_DIRECTIONS = (
    Direction.UP,
    Direction.RIGHT,
    Direction.DOWN,
    Direction.LEFT,
    Direction.UP_RIGHT,
    Direction.UP_LEFT,
    Direction.DOWN_RIGHT,
    Direction.DOWN_LEFT,
)
ORTHOGONAL_DIRECTIONS = (Direction.DOWN, Direction.LEFT, Direction.UP, Direction.RIGHT)


class EntityTypes(Enum):
    MISC = 0
    HERO = 1
    SLIME = 2
    PIG = 3
    PIG_METAL = 4
    PIG_GOLDEN = 5
    PIG_STATUE = 6
    SKULL = 7
    SKULL_STATUE = 8
    SQUID = 9
    OCTOPUS = 10
    GHOST = 11
    GREEN_CROC = 12


PIG_TYPES = (
    EntityTypes.PIG,
    EntityTypes.PIG_METAL,
    EntityTypes.PIG_GOLDEN,
    EntityTypes.PIG_STATUE,
)

CoordData = tuple[int, int]


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
    if direction == Direction.DIRECTIONLESS:
        return (x, y)


def get_pixel(image: Image.Image, coord: CoordData) -> tuple[int, ...]:
    pixel = image.getpixel(coord)
    if pixel is None:
        raise ValueError("Pixel not found")
    if isinstance(pixel, int):
        raise ValueError("Image is not in RGB mode")
    if isinstance(pixel, float):
        raise ValueError("Image is not in RGB mode")
    if len(pixel) < 3:
        raise ValueError("Image is not in RGB mode")
    return pixel


class Node:
    def __init__(
        self,
        entity_type: EntityTypes,
        coordinates: CoordData,
        traversed_path: list[Direction] | None = None,
    ):
        self.coord = coordinates
        self.type = entity_type
        if traversed_path is None:
            self.traversed_path: list[Direction] = []
        else:
            self.traversed_path = traversed_path

    def set_traversed_path(self, traversed_path: list[Direction]):
        self.traversed_path = traversed_path

    def get_path_value(self) -> int:
        if self.type in (EntityTypes.SLIME, EntityTypes.SKULL):
            cumulative_value = 0
            path_length = len(self.traversed_path)
            for index, direction in enumerate(self.traversed_path):
                if direction in (Direction.LEFT, Direction.RIGHT):
                    continue
                length_normalized = path_length - 1 - index
                cumulative_value += 2**length_normalized
            return cumulative_value
        if self.type not in PIG_TYPES:
            return len(self.traversed_path)
        raise ValueError("Entity type is a pig, use get_pig_path_value instead")

    def get_pig_path_value(self) -> list[int]:
        if self.type not in PIG_TYPES:
            raise ValueError("Entity type is not a pig")
        previous_direction = self.traversed_path[0]
        path_cost = [0]
        for current_direction in self.traversed_path:
            if current_direction == previous_direction:
                path_cost[-1] += 1
            else:
                previous_direction = current_direction
                path_cost.append(1)
        return path_cost

    def get_traversed_path(self) -> list[Direction]:
        return self.traversed_path

    def get_type(self) -> EntityTypes:
        return self.type

    def is_valid_move(self, game_map: Image.Image) -> bool:
        if self.type not in (EntityTypes.SQUID, EntityTypes.OCTOPUS):
            # if the entity is not a squid or octopus, it cannot move diagonally
            for direction in self.traversed_path:
                if direction not in ORTHOGONAL_DIRECTIONS:
                    return False
        elif self.type == EntityTypes.SQUID:
            # if the entity is a squid, it cannot move orthogonally
            for direction in self.traversed_path:
                if direction in ORTHOGONAL_DIRECTIONS:
                    return False
        if self.type == EntityTypes.GHOST:
            # if the entity is a ghost, it can move freely
            return True
        map_size = game_map.size
        #tests if the coordinate is out of bounds
        for axis_index in range(2):
            if self.coord[axis_index] < 0:
                return False
            if self.coord[axis_index] >= map_size[axis_index]:
                return False
        # tests if the coordinate is a wall (any color that is not white or red)
        pixel = get_pixel(game_map, self.coord)
        if pixel[0] != 255:
            return False
        if pixel[1] != pixel[2]:
            return False
        if pixel[1] == 0:
            return True
        if pixel[1] == 255:
            return True
        return False

    def copy_node(self, direcao: Direction) -> "Node":
        new_coord = apply_direction(self.coord, direcao)
        new_traversed_path = self.traversed_path.copy()
        new_traversed_path.append(direcao)
        return Node(self.get_type(), new_coord, new_traversed_path)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Node):
            return NotImplemented
        return self.coord == other.coord

    def __gt__(self, other: "Node") -> bool:
        if self.type not in PIG_TYPES:
            return self.get_path_value() >= other.get_path_value()
        self_value = self.get_pig_path_value()
        other_value = other.get_pig_path_value()
        if len(other_value) != len(self_value):
            return len(other_value) > len(self_value)

        def calculate_value(values: list[int]) -> int:
            cumulative_value = 0
            value_length = len(values)
            for index, value in enumerate(values):
                exponent = value_length - index
                cumulative_value += value * 2**exponent
            return cumulative_value

        return calculate_value(self_value) > calculate_value(other_value)

    def __str__(self) -> str:
        info_list: list[str] = []
        info_list.append(f"TIPO : {self.get_type()}")
        info_list.append(f"COORD : {self.coord}")
        info_list.append(f"VALUE : {self.get_path_value()}")
        traversed_path = self.traversed_path
        if self.type in PIG_TYPES:
            traversed_path = self.traversed_path[1:]
        if len(traversed_path) == 0:
            return "\n".join(info_list)
        directions_str = [str(direcao) for direcao in traversed_path]
        info_list.append(", ".join(directions_str))
        return "\n".join(info_list)


class GameEntity:
    def __init__(
        self,
        entity_type: EntityTypes,
        coordinates: CoordData,
        direction: Direction | None = None,
    ):
        self.coord = coordinates
        self.type = entity_type
        self.direction = Direction.DIRECTIONLESS
        if direction is not None:
            self.direction = direction

    def nextTurn(self, game_entities: list["GameEntity"], game_map: Image.Image) -> None:
        color = get_pixel(game_map, self.coord)
        game_map.putpixel((self.coord), (255, 255, 255, 255))
        print(self.coord)
        if self.type == EntityTypes.HERO:
            game_map.putpixel((self.coord), color)
            return
        if self.type in PIG_TYPES:
            best_path = self.get_best_path(
                game_entities[0],
                Node(self.type, self.coord, [self.direction]),
                game_map,
            )
            best_path = best_path[1:]
            print(best_path)
        else:
            best_path = self.get_best_path(
                game_entities[0], Node(self.type, self.coord), game_map
            )
            print(best_path)
        if best_path:
            next_step = best_path[0]
            self.direction = next_step
            self.coord = apply_direction(self.coord, next_step)
        print(self.coord)
        print()

    def evaluate_future_nodes(
        self,
        game_map: Image.Image,
        current_nodes: list[Node],
        previous_nodes: list[Node],
    ) -> list[Node]:
        future_nodes: list[Node] = []
        for node in current_nodes:
            for direction in ACTUAL_DIRECTIONS:
                new_node = node.copy_node(direction)
                if not new_node.is_valid_move(game_map):
                    continue
                if new_node in previous_nodes:
                    continue
                found_index: int | None = None
                for index, future_node in enumerate(future_nodes):
                    if new_node == future_node:
                        found_index = index
                        break
                if found_index is None:
                    future_nodes.append(new_node)
                    continue
                if new_node > future_nodes[found_index]:
                    future_nodes[found_index] = new_node
        return future_nodes

    def get_best_path(
        self, target_node: "GameEntity", start_node: Node, game_map: Image.Image
    ) -> list[Direction]:
        current_nodes = self.evaluate_future_nodes(game_map, [start_node], [])
        previous_nodes = [start_node]
        while target_node not in current_nodes:
            future_nodes = self.evaluate_future_nodes(
                game_map, current_nodes, previous_nodes
            )
            previous_nodes = current_nodes
            current_nodes = future_nodes
            if not current_nodes:
                return []
        for node in current_nodes:
            if node == target_node:
                return node.traversed_path
        return []


def imprime(nodes: list[Node]) -> None:
    for node in nodes:
        print(f"{node}\n")


def parse_pig(color_hue: int, coord: CoordData) -> GameEntity | None:
    color_index = color_hue // 8
    direction = Direction(color_hue % 4)
    if color_index == 16:
        # some shade of pink (255, 128, 255) to (255, 132, 255)
        return GameEntity(EntityTypes.PIG, coord, direction=direction)
    elif color_index == 11:
        # some shade of pink (255, 88, 255) to (255, 92, 255)
        return GameEntity(EntityTypes.PIG_METAL, coord, direction=direction)
    elif color_index == 6:
        # some shade of pink (255, 48, 255) to (255, 52, 255)
        return GameEntity(EntityTypes.PIG_GOLDEN, coord, direction=direction)
    elif color_index == 0:
        # some shade of pink (255, 0, 255) to (255, 4, 255)
        return GameEntity(EntityTypes.PIG_STATUE, coord, direction=direction)
    return None


def parse_pixel(color: tuple[int, ...], coord: CoordData) -> None | GameEntity:
    # function extremely confusing, but it is very optimized for performance.
    red, green, blue = color[:3]
    if red == 255:
        # red is sure to be 255
        if green == 255:
            if blue == 255:
                # not white (255, 255, 255)
                return None
            # some shade of pink (255, 0, 255) to (255, 254, 255)
            return parse_pig(color[1], coord)
        if blue != 0:
            # any shade of purple (255, 0, 1) to (255, 0, 254) is not an entity
            return None
        # blue is sure to be 0 here
        if green == 0:
            # this is red (255, 0, 0)
            hero = GameEntity(EntityTypes.HERO, coord)
            return hero
        if green != 255:
            # any shade of red (255, 1-254, 0) is not an entity
            return None
        # green is sure to be 255 here
        # here it can only be yellow (255, 255, 0)
        squid = GameEntity(EntityTypes.SQUID, coord)
        return squid
    if red != 0:
        # any shade of non-red (1-254, x, x) is not an entity
        return None
    # red is sure to be 0 here
    if blue == 255:
        # blue is sure to be 255 here
        if green == 255:
            # the color here is cyan (0,255,255)
            ghost = GameEntity(EntityTypes.GHOST, coord)
            return ghost
        if green == 127:
            # the color here is teal (0,127,255)
            skull = GameEntity(EntityTypes.SKULL, coord)
            return skull
        if green == 0:
            # the color here is blue (0,0,255)
            slime = GameEntity(EntityTypes.SLIME, coord)
            return slime
    if green == 73 and blue == 73:
        # special case, the color here is a nocturne teal (0,73,73)
        skull_statue = GameEntity(EntityTypes.SKULL_STATUE, coord)
        return skull_statue
    if blue != 0:
        # any shade of non-blue (0, x, 1-254) is not an entity
        return None
    if green == 127:
        # the color here is half green (0,127,0)
        octopus = GameEntity(EntityTypes.OCTOPUS, coord)
        return octopus
    if green == 255:
        # the color here is full green (0,255,0)
        green_croc = GameEntity(EntityTypes.GREEN_CROC, coord)
        return green_croc
    return None


def parse_map(game_map: Image.Image) -> list[GameEntity]:
    width, height = game_map.size
    game_entities: list[GameEntity] = []
    for x in range(width):
        for y in range(height):
            coord = (x, y)
            color = get_pixel(game_map, coord)
            entity = parse_pixel(color, coord)
            if entity is not None:
                if entity.type == EntityTypes.HERO:
                    game_entities.insert(0, entity)
                    continue
                game_entities.append(entity)
    return game_entities


def open_image(image_path: str) -> Image.Image:
    with Image.open(image_path) as image:
        image_in_memory = image.copy()
        return image_in_memory


def main() -> None:
    image = open_image("input.png")
    game_entities = parse_map(image)
    a = 0
    while True:
        for game_entity in game_entities[1:]:
            print("b")
            print(game_entity.type)
            game_entity.nextTurn(game_entities, image)
        image.save(f"anima/frame{a}.png")
        a += 1
        if get_pixel(image, game_entities[0].coord) not in (
            (255, 0, 0, 255),
            (255, 0, 0),
        ):
            #TODO: I probably stopped coding here. I know for a fact this project is incomplete
            break


if __name__ == "__main__":
    main()
