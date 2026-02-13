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

BLOCK_SIZE = 3
BOARD_LENGTH = 3 * BLOCK_SIZE
BOARD_SIZE = BOARD_LENGTH * BOARD_LENGTH
BLANK_SPACES = (" ", "\n", "\t")


class TimeManager:
    def __init__(self) -> None:
        self.start_time = 0.0
        self.end_time = 0.0
        self.elapsed_time = 0.0

    def start(self) -> None:
        self.start_time = time()

    def stop(self) -> None:
        self.end_time = time()
        self.elapsed_time = self.end_time - self.start_time
        self.print_elapsed_time()

    def print_elapsed_time(self) -> None:
        elapsed_time = self.elapsed_time
        if elapsed_time < 0:
            elapsed_time = -elapsed_time
            sign = "-"
        else:
            sign = ""
        total_ms = int(round(elapsed_time * 1000))
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
        text = ", ".join(parts)
        print(f"\n{sign}{text}\n\n\n")


class CounterManager:
    def __init__(self) -> None:
        self.attempts = 0

    def increment(self) -> None:
        self.attempts += 1

    def display(self) -> None:
        print(str(self))

    def __str__(self) -> str:
        return f"\nAttempts : {self.attempts}"


def convert_raw_sudoku(raw_sudoku: str) -> list[CellData]:
    for space in BLANK_SPACES:
        if space in raw_sudoku:
            raw_sudoku = raw_sudoku.replace(space, "")
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
        for xy in range(BOARD_LENGTH):
            self.grid.append([0 for _ in range(BOARD_LENGTH)])
        if sudoku_board_raw:
            parsed_sudoku_input = convert_raw_sudoku(sudoku_board_raw)
            for xy, valor in enumerate(parsed_sudoku_input):
                if xy > BOARD_SIZE - 1:
                    break
                y = xy // BOARD_LENGTH
                x = xy % BOARD_LENGTH
                self.set_cell(y, x, valor)

    def delete_cell(self, y: int, x: int) -> None:
        self.grid[y][x] = 0

    def get_cell(self, y: int, x: int) -> CellData:
        return self.grid[y][x]

    def is_value_valid_in_block(self, y: int, x: int, cell_value: CellData) -> bool:
        block_y = y // BLOCK_SIZE
        block_x = x // BLOCK_SIZE
        for y in range(BLOCK_SIZE):
            for x in range(BLOCK_SIZE):
                if self.get_cell(BLOCK_SIZE * block_y + y, BLOCK_SIZE * block_x + x) == cell_value:
                    return False
        return True

    def is_value_valid_in_row(self, y: int, cell_value: CellData) -> bool:
        for x in range(BOARD_LENGTH):
            if self.get_cell(y, x) == cell_value:
                return False
        return True

    def is_value_valid_in_column(self, x: int, cell_value: CellData) -> bool:
        for y in range(BOARD_LENGTH):
            if self.get_cell(y, x) == cell_value:
                return False
        return True

    def is_block_valid(self, y: int, x: int) -> bool:
        block_y = y // BLOCK_SIZE
        block_x = x // BLOCK_SIZE
        board = self.copy()
        for block_inside_y in range(BLOCK_SIZE):
            for block_inside_x in range(BLOCK_SIZE):
                y = BLOCK_SIZE * block_y + block_inside_y
                x = BLOCK_SIZE * block_x + block_inside_x
                cell_value = board.get_cell(y, x)
                board.set_cell(y, x, 0)
                if not (board.set_cell(y, x, cell_value)):
                    return False
        return True

    def to_raw(self) -> str:
        raw = ""
        for y in range(BOARD_LENGTH):
            for x in range(BOARD_LENGTH):
                raw += str(self.get_cell(y, x))
        return raw

    def copy(self) -> "SudokuBoard":
        return SudokuBoard(self.to_raw())

    def is_column_valid(self, x: int) -> bool:
        board = self.copy()
        for y in range(BOARD_LENGTH):
            cell_value = board.get_cell(y, x)
            board.set_cell(y, x, 0)
            if not (board.set_cell(y, x, cell_value)):
                return False
        return True

    def is_row_valid(self, y: int) -> bool:
        board = self.copy()
        for x in range(BOARD_LENGTH):
            cell_value = board.get_cell(y, x)
            board.set_cell(y, x, 0)
            if not (board.set_cell(y, x, cell_value)):
                return False
        return True

    def is_board_valid(self) -> bool:
        board = self.copy()
        for y in range(BOARD_LENGTH):
            for x in range(BOARD_LENGTH):
                cell_value = board.get_cell(y, x)
                if cell_value == 0:
                    return False
                board.set_cell(y, x, 0)
                if not (board.set_cell(y, x, cell_value)):
                    return False
        return True

    def is_value_valid(self, y: int, x: int, cell_value: CellData) -> bool:
        if not (self.is_value_valid_in_block(y, x, cell_value)):
            return False
        if not (self.is_value_valid_in_column(x, cell_value)):
            return False
        if not (self.is_value_valid_in_row(y, cell_value)):
            return False
        return True

    def set_cell(self, y: int, x: int, cell_value: CellData) -> bool:
        self.delete_cell(y, x)
        if cell_value not in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
            return False
        if cell_value == 0:
            return True
        if self.is_value_valid(y, x, cell_value):
            self.grid[y][x] = cell_value
            return True
        return False

    def find_empty_cell(self) -> tuple[int, int] | None:
        for y in range(BOARD_LENGTH):
            for x in range(BOARD_LENGTH):
                if self.get_cell(y, x) == 0:
                    return (y, x)
        return None

    def show(self) -> None:
        for y in range(BOARD_LENGTH):
            row = ""
            for x in range(BOARD_LENGTH):
                row += str(self.get_cell(y, x))
            print(row)


def create_sudoku_board(mode: Literal[1, 2]) -> SudokuBoard:
    if mode == 2:
        filename = input("what is the sudoku file name (without .txt)? ")
        with open(f"sudokus/{filename}.txt", "r", encoding="utf-8") as sudoku_raw_file:
            sudoku_board = SudokuBoard(sudoku_raw_file.read())
        return sudoku_board
    sudoku_board = SudokuBoard()
    filled_cells_count = 0
    while filled_cells_count < BOARD_SIZE:
        user_input = input("")
        row_input: list[userInputOptions] = cast(
            list[userInputOptions], user_input.strip().split("")
        )
        for char in row_input:
            position_y = filled_cells_count // BOARD_LENGTH
            position_x = filled_cells_count % BOARD_LENGTH
            if char == "p":
                if filled_cells_count > 0:
                    filled_cells_count -= 1
                    position_y = filled_cells_count // 9
                    position_x = filled_cells_count % 9
                    board_cell = sudoku_board.get_cell(position_y, position_x)
                    print(f"number {board_cell} deleted")
                    sudoku_board.delete_cell(position_y, position_x)
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
                sudoku_board.set_cell(position_y, position_x, cast(CellData, int(char)))
                print(f"element {char} added")
                filled_cells_count += 1
                continue
            print("type a number between 0 and 9 or additional options")
        print()
        sudoku_board.show()
    return sudoku_board


def solve_sudoku_board(
    sudoku_board: SudokuBoard, counter_manager: CounterManager
) -> SudokuBoard | None:
    if sudoku_board.is_board_valid():
        return sudoku_board
    empty_cell = sudoku_board.find_empty_cell()
    if not empty_cell:
        return None
    for value in range(1, BOARD_LENGTH + 1):
        cell_value = cast(CellData, value)
        if not sudoku_board.set_cell(empty_cell[0], empty_cell[1], cell_value):
            continue
        counter_manager.increment()
        solution_board = solve_sudoku_board(sudoku_board, counter_manager)
        if solution_board is not None:
            return solution_board
        sudoku_board.delete_cell(empty_cell[0], empty_cell[1])
    return None


def solve_single_board(sudoku_board: SudokuBoard) -> None:
    sudoku_board.show()
    print()
    counter_manager = CounterManager()
    time_manager = TimeManager()
    time_manager.start()
    solution_board = solve_sudoku_board(sudoku_board, counter_manager)
    if solution_board is not None:
        solution_board.show()
    time_manager.stop()
    counter_manager.display()


def main() -> None:
    time_manager = TimeManager()
    while True:
        mode = main_menu()
        if mode == 0:
            break
        if mode != 3:
            board = create_sudoku_board(mode)
            solve_single_board(board)
            continue
        time_manager.start()
        filenames = os.listdir("sudokus")
        for filename in filenames:
            print(f"{filename}\n")
            with open(f"sudokus/{filename}") as sudoku_board_raw:
                board = SudokuBoard(sudoku_board_raw.read())
                solve_single_board(board)
        time_manager.stop()


if __name__ == "__main__":
    main()
