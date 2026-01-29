from time import time
from typing import Literal
from PIL import Image

CellData = Literal[-1, 0, 1]
# -1 = empty cell
#  0 = unknown cell
#  1 = filled cell
BoardData = list[list[CellData]]
HintData = list[int]
HintAxysData = list[HintData]
HintsData = tuple[HintAxysData, HintAxysData]


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


def save_board_image(board: BoardData, file_name: str) -> None:
    image = Image.new("RGBA", (len(board[0]), len(board)), (255, 255, 255, 255))
    for y, column in enumerate(board):
        for x, cell in enumerate(column):
            if cell == 1:
                image.putpixel((x, y), (0, 0, 0, 255))
    image.save(f"{file_name}.png")
    image.close()


def compare_situations(
    current_states: list[int],
    hint: HintData,
    previous_cell: CellData,
    limit_index: int,
    length: int,
) -> bool:
    if hint[0] == 0:
        if current_states:
            return False
        else:
            return True
    if len(current_states) > len(hint):
        return False
    if not current_states:
        if length - (limit_index + 1) < len(hint) + sum(hint) - 1:
            return False
        return True
    index = -1
    if len(current_states) > 1:
        for index, situacao in enumerate(current_states[:-1]):
            if situacao != hint[index]:
                return False
    else:
        index = -1
    if previous_cell != 1:
        if current_states[index + 1] != hint[index + 1]:
            return False
        if len(current_states) < len(hint):
            if (
                length - (limit_index + 1)
                < len(hint[len(current_states) :])
                + sum(hint[len(current_states) :])
                - 1
            ):
                return False
    else:
        if current_states[index + 1] > hint[index + 1]:
            return False
        if current_states[index + 1] == hint[index + 1]:
            if (
                length - (limit_index + 1)
                < len(hint[len(current_states) :])
                + sum(hint[len(current_states) :])
                - 2
            ):
                return False
        else:
            if (
                length - (limit_index + 1)
                < len(hint[len(current_states) :])
                + sum(hint[len(current_states) :])
                + hint[index + 1]
                - current_states[index + 1]
                - 1
            ):
                return False
    return True


def validate_partial_columns(
    board: BoardData,
    hints: HintsData,
    maximum_y: int,
    minimum_x: int,
    maximum_x: int,
    new_row: list[CellData],
) -> bool:
    for x in range(minimum_x, maximum_x):
        hint = hints[0][x]
        sequence_counts: list[int] = []
        previous_cell: CellData = 0
        count = 0
        for y in range(maximum_y + 1):
            if y == maximum_y:
                if new_row:
                    cell_value = new_row[x - minimum_x]
                else:
                    cell_value = board[y][x]
            else:
                cell_value = board[y][x]
            if previous_cell == 1:
                if cell_value == 1:
                    count += 1
                else:
                    sequence_counts.append(count)
            else:
                if cell_value == 1:
                    count = 1
            previous_cell = cell_value
        if previous_cell == 1:
            sequence_counts.append(count)
        if not compare_situations(
            sequence_counts, hint, previous_cell, maximum_y, len(board)
        ):
            return False
    return True


def generate_row_possibilities(
    row_length: int,
    row_hints: HintData,
    board_hints: HintsData,
    board: BoardData,
    row_index: int,
) -> list[list[CellData]]:
    if len(row_hints) == 0:
        # if there are no hints, the only possibility is all empty
        return [[-1 for _ in range(row_length)]]
    if row_length == row_hints[0]:
        # if the row length matches the first hint exactly, the only possibility is all filled
        return [[1 for _ in range(row_length)]]
    if row_hints[0] == 0:
        # if the first hint is 0, the only possibility is all empty
        return [[-1 for _ in range(row_length)]]
    if len(row_hints) - 1 + sum(row_hints) == row_length:
        # if the hints exactly fill the row, create that possibility
        row_case: list[CellData] = []
        for hint_length in row_hints:
            for _ in range(hint_length):
                row_case.append(1)
            row_case.append(-1)
        # remove the last added empty cell
        row_case.pop(-1)
        return [row_case]
    row_cases: list[list[CellData]] = []
    hint_length = row_hints[0]
    if len(row_hints) == 1:
        # if there's only one hint, try all possible starting positions
        for starting_index in range(row_length - hint_length + 1):
            row_case = [-1 for _ in range(row_length)]
            for x in range(hint_length):
                row_case[starting_index + x] = 1
            if validate_partial_columns(
                board,
                board_hints,
                row_index,
                len(board_hints[0]) - row_length,
                len(board_hints[0]) - row_length + len(row_case),
                row_case,
            ):
                row_cases.append(row_case)
        return row_cases
    for starting_index in range(
        row_length - hint_length + 1 - sum(row_hints[1:]) - len(row_hints[1:])
    ):
        # if all heuristics fail, try to place the first hint at all possible starting positions and recursively generate the rest
        row_case = [-1 for _ in range(starting_index + hint_length)]
        for x in range(hint_length):
            row_case[starting_index + x] = 1
        if validate_partial_columns(
            board,
            board_hints,
            row_index,
            len(board_hints[0]) - row_length,
            len(board_hints[0]) - row_length + len(row_case) + 1,
            row_case + [-1],
        ):
            additional_possibilities = generate_row_possibilities(
                row_length - starting_index - hint_length - 1,
                row_hints[1:],
                board_hints,
                board,
                row_index,
            )
            for additional_row_possibility in additional_possibilities:
                row_cases.append(row_case + [-1] + additional_row_possibility)
    return row_cases


def solve_board(board: BoardData, hints: HintsData, row_index: int) -> BoardData | None:
    if row_index == len(board):
        return board
    global tries
    source_row = board[row_index]
    row_hints = hints[1][row_index]
    for possible_row in generate_row_possibilities(
        len(board[0]), row_hints, hints, board, row_index
    ):
        tries += 1
        board[row_index] = possible_row
        solution = solve_board(board, hints, row_index + 1)
        if solution:
            return solution
    board[row_index] = source_row
    return None


def solve_piccross_board(
    board: BoardData, hints: HintsData
) -> tuple[int, BoardData | None]:
    print()
    global tries
    tries = 0
    cuts_amount = 0
    start_time = time()
    solution_board = solve_board(board, hints, 0)
    end_time = time()
    print("\ntentativas: " + str(tries))
    elapsed_seconds = end_time - start_time
    global elapsed_time
    elapsed_time += elapsed_seconds
    print_elapsed_time(elapsed_seconds)
    if solution_board is None:
        return (cuts_amount, solution_board)
    for board_row in solution_board:
        row = ""
        for element in board_row:
            if element > 0:
                row += "#"
                continue
            if element == 0:
                row += "?"
                continue
            row += "0"
        print(row)
    return (cuts_amount, solution_board)


elapsed_time = 0.0
tries = 0
for index in range(8):
    with open(f"piccross/A{index:03d}.txt") as piccross_file:
        config = piccross_file.read()
    horizontal_hints_lines, vertical_hints_lines = config.split("#")
    horizontal_hints: HintAxysData = [
        [int(n) for n in hint.split()]
        for hint in horizontal_hints_lines[:-1].split("\n")
    ]
    vertical_hints: HintAxysData = [
        [int(n) for n in hint.split()] for hint in vertical_hints_lines[1:].split("\n")
    ]
    board: BoardData = []
    for _ in vertical_hints:
        board.append([0 for _ in horizontal_hints])
    all_hints: HintsData = (horizontal_hints, vertical_hints)
    cuts_amount, solution_board = solve_piccross_board(board, all_hints)
    print_elapsed_time(elapsed_time)
    save_board_image(board, f"piccross/A{index:03d}")
print_elapsed_time(elapsed_time)
