# it gives option for bigger android patterns, but right now it only works for 3x3, because we only implemented one middle slot rules

ALLOW_PRINT = False
TOTAL_SLOTS = 9
SLOTS_PER_LINE = 3
MINIMAL_CONFIGURATION_DEGREE = 4
MIDDLE_SLOTS = (4,)
EDGE_SLOTS = (1, 3, 5, 7)
CORNER_SLOTS = (0, 2, 6, 8)
EMPTY_SLOT = 0
HORIZONTAL_SYMMETRY = (2, 0, 8, 6)
VERTICAL_SYMMETRY = (6, 8, 0, 2)
OBSTACLES = ((1, 3), (1, 5), (7, 3), (7, 5))
CORNER_SYMMETRY_MAP = {0: 0, 2: 1, 6: 2, 8: 3}


def calculate_configuration_degree(configuration_grid: list[int]) -> int:
    configuration_degree = 0
    for cell_value in configuration_grid:
        if cell_value != 0:
            configuration_degree += 1
    return configuration_degree


def is_corner(corner_index: int) -> int:
    return CORNER_SYMMETRY_MAP.get(corner_index, -1)


def render_board(configuration_grid: list[int]) -> None:
    board = ""
    for index, cell_value in enumerate(configuration_grid):
        board += str(cell_value)
        if index % SLOTS_PER_LINE == SLOTS_PER_LINE - 1:
            board += "\n"
    print(board)


def is_move_valid(
    configuration_grid: list[int], last_move: int, proposed_move: int
) -> bool:
    if configuration_grid[proposed_move]:
        return False
    if last_move == proposed_move:
        return False
    if (proposed_move in MIDDLE_SLOTS) or (last_move in MIDDLE_SLOTS):
        return True
    opposite_positions = tuple(reversed(range(TOTAL_SLOTS)))
    if proposed_move in EDGE_SLOTS:
        if configuration_grid[4] == EMPTY_SLOT:
            return True
        return last_move != opposite_positions[proposed_move]
    if last_move in EDGE_SLOTS:
        return True
    if last_move == opposite_positions[proposed_move]:
        return configuration_grid[4] == EMPTY_SLOT
    cantoDestino = is_corner(proposed_move)
    if last_move == VERTICAL_SYMMETRY[cantoDestino]:
        obstacle = OBSTACLES[cantoDestino][1]
        return configuration_grid[obstacle] != EMPTY_SLOT
    if last_move == HORIZONTAL_SYMMETRY[cantoDestino]:
        obstacle = OBSTACLES[cantoDestino][0]
        return configuration_grid[obstacle] != EMPTY_SLOT
    return True


def count_valid_configurations(
    configuration_grid: list[int], last_index: int, valid_configuration_count: int
) -> int:
    configuration_degree = calculate_configuration_degree(configuration_grid)
    if configuration_degree >= MINIMAL_CONFIGURATION_DEGREE:
        valid_configuration_count += 1
        if ALLOW_PRINT:
            render_board(configuration_grid)
            print(f"{valid_configuration_count}\n")
    if configuration_degree == TOTAL_SLOTS:
        return valid_configuration_count
    for slot_index in range(TOTAL_SLOTS):
        if not is_move_valid(configuration_grid, last_index, slot_index):
            continue
        updated_configuration = configuration_grid.copy()
        updated_configuration[slot_index] = configuration_degree + 1
        valid_configuration_count = count_valid_configurations(
            updated_configuration, slot_index, valid_configuration_count
        )
    return valid_configuration_count


def main() -> None:
    valid_configuration_count = 0
    for slot_position in range(TOTAL_SLOTS):
        password_configuration = [EMPTY_SLOT] * TOTAL_SLOTS
        password_configuration[slot_position] = 1
        valid_configuration_count = count_valid_configurations(
            password_configuration, slot_position, valid_configuration_count
        )
        print(slot_position)
    print(str(valid_configuration_count))


if __name__ == "__main__":
    main()
