from typing import Literal, cast
from time import time
import os

menuModeOptions = Literal[0, 1, 2, 3]
userInputOptions = Literal[
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "p",
    "l",
    "L",
    "c",
    "C",
    "q",
    "Q",
    "o",
    "s",
    "e",
]
CellData = Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
SudokuGridData = list[list[CellData]]
CoordData = tuple[int, int]
BoardData = tuple[SudokuGridData, list[CoordData]]


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


def main_menu() -> menuModeOptions:
    options = ["sair", "Input Manual", "Import Sudoku Txt", "Loop Import Folder"]
    while True:
        for i, option in enumerate(options):
            print(f"{i} - {option}")
        user_choice = input("escolha uma opcao:")
        try:
            choice_index = int(user_choice)
            if 0 <= choice_index < 4:
                return cast(menuModeOptions, choice_index)
            else:
                raise ValueError
        except (ValueError, IndexError):
            user_choice = input("not valid, try again: ")


def create_sudoku_board_from_input() -> BoardData:
    sudoku: list[CellData] = [0 for _ in range(81)]
    filled_cells_count = 0
    while filled_cells_count < 81:
        user_input = input("")
        for char in user_input:
            if char == "p":
                if filled_cells_count > 0:
                    filled_cells_count -= 1
                    print(f"number {sudoku[-1]} deleted")
                    sudoku[filled_cells_count] = 0
            elif char == "l":
                pass  # apagar linha atual
            elif char == "L":
                pass  # apagar uma linha
            elif char == "c":
                pass  # apagar coluna atual
            elif char == "C":
                pass  # apagar uma coluna
            elif char == "q":
                pass  # apagar quadrante atual
            elif char == "Q":
                pass  # apagar um quadrante
            elif char == "o":
                print("entrada completamente apagada")
                sudoku = [0 for _ in range(81)]
                filled_cells_count = 0
            elif char == "s":
                row = ""
                for a in range(81):
                    row += str(sudoku[a])
                    if a % 9 == 8:
                        print(row)
                        row = ""
            elif char == "e":
                filled_cells_count = 81
            elif char in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                sudoku[filled_cells_count] = cast(CellData, int(char))
                print(f"element {char} added")
                filled_cells_count += 1
            else:
                print("type a number between 0 and 9 or additional options")
                sudoku[filled_cells_count] = 0
                filled_cells_count += 1
        print()
    sudoku_board = create_sudoku_board("".join([str(char) for char in sudoku]))
    print_board(sudoku_board)
    return sudoku_board


def print_board(board: BoardData) -> None:
    for y in range(9):
        if (y != 0) and (y % 3 == 0):
            print("---+---+---")
        row = ""
        for x in range(0, 3):
            row += str(board[y][x])
        row += "|"
        for x in range(3, 6):
            row += str(board[y][x])
        row += "|"
        for x in range(6, 9):
            row += str(board[y][x])
        print(row)


def convert_raw_sudoku(raw_sudoku: str) -> list[CellData]:
    for espaco in [" ", "\n", "\t"]:
        if espaco in raw_sudoku:
            raw_sudoku = raw_sudoku.replace(espaco, "")
    parsed_sudoku: list[int] = []
    for char in raw_sudoku:
        if char in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            parsed_sudoku.append(int(char))
    return cast(list[CellData], parsed_sudoku)


def create_sudoku_board(sudoku_board_raw: str) -> BoardData:
    grid: SudokuGridData = []
    empty_cells: list[CoordData] = []
    board: BoardData = (grid, empty_cells)
    for _ in range(9):
        board[0].append([0, 0, 0, 0, 0, 0, 0, 0, 0])
    parsed_sudoku_input = convert_raw_sudoku(sudoku_board_raw)
    for xy, value in enumerate(parsed_sudoku_input):
        if xy > 80:
            break
        y = xy // 9
        x = xy % 9
        board[0][y][x] = value
        if value == 0:
            board[1].append((y, x))
    return board


def find_valid_candidates(board: BoardData, y: int, x: int) -> list[CellData]:
    block_y = y // 3
    block_x = x // 3
    possible_values: list[CellData] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    board[0][y][x] = 0
    for y_offset in range(3):
        for x_offset in range(3):
            if (
                board[0][3 * block_y + y_offset][3 * block_x + x_offset]
                in possible_values
            ):
                possible_values.remove(
                    board[0][3 * block_y + y_offset][3 * block_x + x_offset]
                )
    if block_y == 0:
        for y_offset in range(3, 9):
            if board[0][y_offset][x] in possible_values:
                possible_values.remove(board[0][y_offset][x])
    elif block_y == 2:
        for y_offset in range(0, 6):
            if board[0][y_offset][x] in possible_values:
                possible_values.remove(board[0][y_offset][x])
    else:
        for y_offset in range(3):
            if board[0][y_offset][x] in possible_values:
                possible_values.remove(board[0][y_offset][x])
        for y_offset in range(6, 9):
            if board[0][y_offset][x] in possible_values:
                possible_values.remove(board[0][y_offset][x])
    if not (possible_values):
        return possible_values
    if block_x == 0:
        for x_offset in range(3, 9):
            if board[0][y][x_offset] in possible_values:
                possible_values.remove(board[0][y][x_offset])
    elif block_x == 2:
        for x_offset in range(0, 6):
            if board[0][y][x_offset] in possible_values:
                possible_values.remove(board[0][y][x_offset])
    else:
        for x_offset in range(3):
            if board[0][y][x_offset] in possible_values:
                possible_values.remove(board[0][y][x_offset])
        for x_offset in range(6, 9):
            if board[0][y][x_offset] in possible_values:
                possible_values.remove(board[0][y][x_offset])
    return possible_values


def solve_sudoku_board(board: BoardData) -> BoardData | None:
    if len(board[1]) == 0:
        return board
    empty_cell = board[1].pop()
    global tries
    for value in find_valid_candidates(board, empty_cell[0], empty_cell[1]):
        board[0][empty_cell[0]][empty_cell[1]] = value
        tries += 1
        solution_board = solve_sudoku_board(board)
        if solution_board:
            return solution_board
    board[0][empty_cell[0]][empty_cell[1]] = 0
    board[1].append(empty_cell)
    return None


def solve_single_board(board: BoardData) -> BoardData | None:
    print()
    global tries
    tries = 0
    start_time = time()
    solution_board = solve_sudoku_board(board)
    if solution_board is not None:
        print_board(solution_board)
    end_time = time()
    print(f"\nattempts: {tries}")
    elapsed_duration = end_time - start_time
    global elapsed_time
    elapsed_time += elapsed_duration
    print_elapsed_time(elapsed_duration)
    return solution_board


tries = 0
elapsed_time = 0.0
while True:
    elapsed_time = 0
    mode = main_menu()
    if mode == 0:
        break
    if mode == 3:
        file_names = os.listdir("sudokus")
        for file_name in file_names:
            print(f"{file_name}\n")
            with open(
                f"sudokus//{file_name}", "r", encoding="utf-8"
            ) as sudoku_board_raw:
                board = create_sudoku_board(sudoku_board_raw.read())
            solution_board = solve_single_board(board)
            print_elapsed_time(elapsed_time)
    elif mode == 2:
        file_name = input("what is the anme of the file? (without .txt)")
        with open(f"{file_name}.txt", "r", encoding="utf-8") as sudoku_board_raw:
            board = create_sudoku_board(sudoku_board_raw.read())
        solve_single_board(board)
    else:
        board = create_sudoku_board_from_input()
        solve_single_board(board)
        print_board(board)
