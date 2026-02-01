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


def convert_raw_sudoku(raw_sudoku: str) -> list[CellData]:
    for espaco in [" ", "\n", "\t"]:
        if espaco in raw_sudoku:
            raw_sudoku = raw_sudoku.replace(espaco, "")
    parsed_sudoku: list[int] = []
    for char in raw_sudoku:
        if char in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            parsed_sudoku.append(int(char))
    return cast(list[CellData], parsed_sudoku)


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


class SudokuBoard:
    def __init__(self, sudoku_board_raw: str | None = None) -> None:
        self.grid: SudokuGridData = []
        self.empty_cells: list[CoordData] = []
        for y in range(9):
            self.grid.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
        if sudoku_board_raw is None:
            self.empty_cells = [(0, x) for x in range(9, 0, -1)] + self.empty_cells
            return
        parsed_sudoku_input = convert_raw_sudoku(sudoku_board_raw)
        for xy, value in enumerate(parsed_sudoku_input):
            if xy > 80:
                break
            y = xy // 9
            x = xy % 9
            self.set_cell(y, x, value)
            if value == 0:
                self.empty_cells = [(y, x)] + self.empty_cells

    def is_value_valid(self, y: int, x: int, cell_value: CellData) -> bool:
        block_y = y // 3
        block_x = x // 3
        for a in range(3):
            for b in range(3):
                if self.grid[3 * block_y + a][3 * block_x + b] == cell_value:
                    return False
        if block_y == 0:
            for a in range(3, 9):
                if self.grid[a][x] == cell_value:
                    return False
        elif block_y == 2:
            for a in range(0, 6):
                if self.grid[a][x] == cell_value:
                    return False
        else:
            for a in range(3):
                if self.grid[a][x] == cell_value:
                    return False
            for a in range(6, 9):
                if self.grid[a][x] == cell_value:
                    return False
        if block_x == 0:
            for b in range(3, 9):
                if self.grid[y][b] == cell_value:
                    return False
        elif block_x == 2:
            for b in range(0, 6):
                if self.grid[y][b] == cell_value:
                    return False
        else:
            for b in range(3):
                if self.grid[y][b] == cell_value:
                    return False
            for b in range(6, 9):
                if self.grid[y][b] == cell_value:
                    return False
        return True

    def set_cell(self, y: int, x: int, cell_value: CellData) -> bool:
        self.grid[y][x] = 0
        if cell_value not in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
            return False
        if cell_value == 0:
            return True
        if self.is_value_valid(y, x, cell_value):
            self.grid[y][x] = cell_value
            return True
        return False

    def show(self) -> None:
        for y in range(9):
            row = ""
            for x in range(9):
                row += str(self.grid[y][x])
            print(row)


def create_sudoku_board(mode: Literal[1, 2]) -> SudokuBoard:
    if mode == 2:
        file_name = input("what is the sudoku file name (without .txt)? ")
        with open(
            f"sudokus//{file_name}.txt", "r", encoding="utf-8"
        ) as sudoku_raw_file:
            sudoku_board = SudokuBoard(sudoku_raw_file.read())
        return sudoku_board
    sudoku_board = SudokuBoard()
    filled_cells_count = 0
    while filled_cells_count < 81:
        user_input = input("")
        row_input: list[userInputOptions] = cast(
            list[userInputOptions], user_input.strip().split("")
        )
        for char in row_input:
            y = filled_cells_count // 9
            x = filled_cells_count % 9
            if char == "p":
                if filled_cells_count > 0:
                    filled_cells_count -= 1
                    y = filled_cells_count // 9
                    x = filled_cells_count % 9
                    board_cell = sudoku_board.grid[y][x]
                    print(f"number {board_cell} deleted")
                    sudoku_board.grid[y][x] = 0
                continue
            if char == "l":
                continue  # TODO delete current line
            if char == "L":
                continue  # TODO delete a line
            if char == "c":
                continue  # TODO delete current column
            if char == "C":
                continue  # TODO delete a column
            if char == "q":
                continue  # TODO delete current block
            if char == "Q":
                continue  # TODO delete a block
            elif char == "o":
                print("input completely cleared")
                sudoku_board = SudokuBoard()
                filled_cells_count = 0
                continue
            elif char == "s":
                sudoku_board.show()
                continue
            elif char == "e":
                return sudoku_board
            elif char in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                sudoku_board.set_cell(y, x, cast(CellData, int(char)))
                print(f"element {char} added")
                filled_cells_count += 1
                continue
            print("type a number between 0 and 9 or additional options")
        print()
        sudoku_board.show()
    return sudoku_board


def solve_sudoku_board(sudoku_board: SudokuBoard) -> SudokuBoard | None:
    if len(sudoku_board.empty_cells) == 0:
        return sudoku_board
    empty_cell = sudoku_board.empty_cells.pop(-1)
    if not empty_cell:
        return None
    global tries
    for value in range(1, 10):
        cell_value = cast(CellData, value)
        if not sudoku_board.set_cell(empty_cell[0], empty_cell[1], cell_value):
            continue
        tries += 1
        solution_board = solve_sudoku_board(sudoku_board)
        if solution_board is not None:
            return solution_board
    sudoku_board.grid[empty_cell[0]][empty_cell[1]] = 0
    sudoku_board.empty_cells.append(empty_cell)
    return None


def solve_single_board(sudoku_board: SudokuBoard) -> None:
    sudoku_board.show()
    print()
    global tries
    tries = 0
    start_time = time()
    solution_board = solve_sudoku_board(sudoku_board)
    end_time = time()
    if solution_board is not None:
        solution_board.show()
    print(f"\nAttempts: {tries}")
    elapsed_duration = end_time - start_time
    global elapsed_time
    elapsed_time += elapsed_duration
    print_elapsed_time(elapsed_duration)


tries = 0
elapsed_time = 0.0
while True:
    mode = main_menu()
    if mode == 0:
        break
    if mode != 3:
        board = create_sudoku_board(mode)
        solve_single_board(board)
    file_names = os.listdir("sudokus")
    for file_name in file_names:
        print(f"{file_name}\n")
        with open(f"sudokus//{file_name}", "r", encoding="utf-8") as sudoku_board_raw:
            board = SudokuBoard(sudoku_board_raw.read())
        solve_single_board(board)
    print_elapsed_time(elapsed_time)
