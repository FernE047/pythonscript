from typing import Literal, TypedDict, cast
from time import time
import os

CellData = Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
SudokuGridData = list[list[CellData]]
CoordData = tuple[int, int]


class BoardData(TypedDict):
    grid: SudokuGridData
    empty_cells: list[CoordData]


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


def create_sudoku_board(sudoku_board_raw: str) -> BoardData:
    grid: SudokuGridData = []
    empty_cells: list[CoordData] = []
    board: BoardData = {"grid": grid, "empty_cells": empty_cells}
    for _ in range(9):
        board["grid"].append([0, 0, 0, 0, 0, 0, 0, 0, 0])
    parsed_sudoku_input = convert_raw_sudoku(sudoku_board_raw)
    for xy, value in enumerate(parsed_sudoku_input):
        if xy > 80:
            break
        y = xy // 9
        x = xy % 9
        board["grid"][y][x] = value
        if value == 0:
            board["empty_cells"] = [(y, x)] + board["empty_cells"]
    return board


def is_value_valid(board: BoardData, y: int, x: int, cell_value: CellData) -> bool:
    block_y = y // 3
    block_x = x // 3
    for y_offset in range(3):
        for x_offset in range(3):
            if (
                board["grid"][3 * block_y + y_offset][3 * block_x + x_offset]
                == cell_value
            ):
                return False
    if block_y == 0:
        for y_offset in range(3, 9):
            if board["grid"][y_offset][x] == cell_value:
                return False
    elif block_y == 2:
        for y_offset in range(0, 6):
            if board["grid"][y_offset][x] == cell_value:
                return False
    else:
        for y_offset in range(3):
            if board["grid"][y_offset][x] == cell_value:
                return False
        for y_offset in range(6, 9):
            if board["grid"][y_offset][x] == cell_value:
                return False
    if block_x == 0:
        for x_offset in range(3, 9):
            if board["grid"][y][x_offset] == cell_value:
                return False
    elif block_x == 2:
        for x_offset in range(0, 6):
            if board["grid"][y][x_offset] == cell_value:
                return False
    else:
        for x_offset in range(3):
            if board["grid"][y][x_offset] == cell_value:
                return False
        for x_offset in range(6, 9):
            if board["grid"][y][x_offset] == cell_value:
                return False
    return True


def set_cell(board: BoardData, y: int, x: int, cell_value: CellData) -> bool:
    board["grid"][y][x] = 0
    if cell_value not in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
        return False
    if cell_value == 0:
        return True
    if is_value_valid(board, y, x, cell_value):
        board["grid"][y][x] = cell_value
        return True
    return False


def show(board: BoardData) -> None:
    for y in range(9):
        row = ""
        for x in range(9):
            row += str(board["grid"][y][x])
        print()


def solve_sudoku_board(board: BoardData) -> BoardData | None:
    if len(board["empty_cells"]) == 0:
        return board
    empty_cell = board["empty_cells"].pop(-1)
    if not empty_cell:
        return None
    global tries
    for value in range(1, 10):
        cell_value = cast(CellData, value)
        if not set_cell(board, empty_cell[0], empty_cell[1], cell_value):
            continue
        tries += 1
        solution_board = solve_sudoku_board(board)
        if solution_board is not None:
            return solution_board
    board["grid"][empty_cell[0]][empty_cell[1]] = 0
    board["empty_cells"].append(empty_cell)
    return board


def solve_single_board(board: BoardData) -> None:
    show(board)
    print()
    global tries
    tries = 0
    start_time = time()
    solution_board = solve_sudoku_board(board)
    end_time = time()
    if solution_board is not None:
        show(solution_board)
    print(f"\nAttempts: {tries}")
    elapsed_duration = end_time - start_time
    global elapsed_time
    elapsed_time += elapsed_duration
    print_elapsed_time(elapsed_duration)


tries = 0
elapsed_time = 0.0
while True:
    file_names = os.listdir("sudokus")
    for file_name in file_names:
        print(f"{file_name}\n")
        with open(f"sudokus//{file_name}", "r", encoding="utf-8") as sudoku_board_raw:
            board = create_sudoku_board(sudoku_board_raw.read())
        solve_single_board(board)
    print_elapsed_time(elapsed_time)
