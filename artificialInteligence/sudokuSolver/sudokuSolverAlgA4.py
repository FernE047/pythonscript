from typing import Literal, cast
from time import time
import os

CellData = Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
SudokuGridData = list[list[CellData]]
CoordData = tuple[int, int]
BoardData = tuple[SudokuGridData, list[CoordData]]


class TimeManager:
    def __init__(self) -> None:
        self.start_time = 0.0
        self.end_time = 0.0
        self.elapsed_time = 0.0

    def start(self) -> None:
        self.start_time = time()

    def stop(self) -> None:
        self.end_time = time()
        self.elapsed_time += self.end_time - self.start_time
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
    block_y = (y // 3) * 3
    block_x = (x // 3) * 3
    possible_values: list[CellData] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    board[0][y][x] = 0
    for y_offset in range(3):
        for x_offset in range(3):
            cell_value = board[0][block_y + y_offset][block_x + x_offset]
            if cell_value in possible_values:
                possible_values.remove(cell_value)
    if block_y == 0:
        for y_offset in range(3, 9):
            cell_value = board[0][y_offset][x]
            if cell_value in possible_values:
                possible_values.remove(cell_value)
    elif block_y == 6:
        for y_offset in range(0, 6):
            cell_value = board[0][y_offset][x]
            if cell_value in possible_values:
                possible_values.remove(cell_value)
    else:
        for y_offset in range(3):
            cell_value = board[0][y_offset][x]
            if cell_value in possible_values:
                possible_values.remove(cell_value)
        for y_offset in range(6, 9):
            cell_value = board[0][y_offset][x]
            if cell_value in possible_values:
                possible_values.remove(cell_value)
    if not (possible_values):
        return possible_values
    if block_x == 0:
        for x_offset in range(3, 9):
            cell_value = board[0][y][x_offset]
            if cell_value in possible_values:
                possible_values.remove(cell_value)
    elif block_x == 6:
        for x_offset in range(0, 6):
            cell_value = board[0][y][x_offset]
            if cell_value in possible_values:
                possible_values.remove(cell_value)
    else:
        for x_offset in range(3):
            cell_value = board[0][y][x_offset]
            if cell_value in possible_values:
                possible_values.remove(cell_value)
        for x_offset in range(6, 9):
            cell_value = board[0][y][x_offset]
            if cell_value in possible_values:
                possible_values.remove(cell_value)
    return possible_values


def solve_sudoku_board(board: BoardData, counter_manager: CounterManager) -> BoardData | None:
    if len(board[1]) == 0:
        return board
    empty_cell = board[1].pop()
    for value in find_valid_candidates(board, empty_cell[0], empty_cell[1]):
        board[0][empty_cell[0]][empty_cell[1]] = value
        counter_manager.increment()
        solution_board = solve_sudoku_board(board, counter_manager)
        if solution_board:
            return solution_board
    board[0][empty_cell[0]][empty_cell[1]] = 0
    board[1].append(empty_cell)
    return None


def solve_single_board(board: BoardData, time_manager: TimeManager) -> None:
    print()
    counter_manager = CounterManager()
    time_manager.start()
    solve_sudoku_board(board, counter_manager)
    time_manager.stop()
    counter_manager.display()



def main() -> None:
    time_manager = TimeManager()
    file_names = os.listdir("sudokus")
    for file_name in file_names:
        print(f"{file_name}\n")
        with open(f"sudokus//{file_name}", "r", encoding="utf-8") as sudoku_board_raw:
            board = create_sudoku_board(sudoku_board_raw.read())
        solve_single_board(board, time_manager)
    time_manager.print_elapsed_time()


if __name__ == "__main__":
    main()