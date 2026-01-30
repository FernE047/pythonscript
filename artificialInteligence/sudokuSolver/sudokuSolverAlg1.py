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
QuadranteRowData = tuple["SudokuBlock", "SudokuBlock", "SudokuBlock"]
BoardData = tuple[QuadranteRowData, QuadranteRowData, QuadranteRowData]
CellData = Literal["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
SudokuGridData = list[list[CellData]]


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


def convert_raw_sudoku(raw_sudoku: str) -> list[CellData]:
    for espaco in [" ", "\n", "\t"]:
        if espaco in raw_sudoku:
            raw_sudoku = raw_sudoku.replace(espaco, "")
    return cast(list[CellData], list(raw_sudoku))


class SudokuBlock:
    def __init__(self, config_str: str | None = None) -> None:
        self.sudoku_grid: SudokuGridData = []
        for _ in range(3):
            self.sudoku_grid.append(["0", "0", "0"])
        if config_str is not None:
            for char_index, cell_value in enumerate(list(config_str)):
                cell_value = cast(CellData, cell_value)
                self.sudoku_grid[char_index // 3][char_index % 3] = cell_value

    def delete_cell(self, y: int, x: int) -> None:
        self.sudoku_grid[y][x] = "0"

    def get_cell(self, y: int, x: int) -> CellData:
        return self.sudoku_grid[y][x]

    def is_value_valid(self, v: CellData) -> bool:
        for a in range(3):
            for b in range(3):
                if self.sudoku_grid[a][b] == v:
                    return False
        return True

    def set_element(self, y: int, x: int, cell_value: CellData) -> bool:
        if cell_value not in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            raise ValueError("cell_value must be between '0' and '9'")
        if cell_value == "0":
            self.sudoku_grid[y][x] = "0"
            return True
        if self.is_value_valid(cell_value):
            self.sudoku_grid[y][x] = cell_value
            return True
        return False

    def generate_config_str(self):
        chave = ""
        for a in range(3):
            for b in range(3):
                chave += self.get_cell(a, b)
        return chave

    def copy(self) -> "SudokuBlock":
        return SudokuBlock(self.generate_config_str())

    def is_block_valid(self) -> bool:
        quadrante = self.copy()
        for y in range(3):
            for x in range(3):
                cell_value = quadrante.get_cell(y, x)
                quadrante.set_element(y, x, "0")
                if not (quadrante.set_element(y, x, cell_value)):
                    return False
        return True


class SudokuBoard:
    def __init__(self, sudoku_board_raw: str | None = None) -> None:
        self.sudoku_grid: BoardData = (
            (SudokuBlock(), SudokuBlock(), SudokuBlock()),
            (SudokuBlock(), SudokuBlock(), SudokuBlock()),
            (SudokuBlock(), SudokuBlock(), SudokuBlock()),
        )
        if sudoku_board_raw is not None:
            parsed_sudoku_input = convert_raw_sudoku(sudoku_board_raw)
            for xy, cell_value in enumerate(parsed_sudoku_input):
                if xy > 80:
                    break
                y = xy // 9
                x = xy % 9
                self.set_cell(y, x, cell_value)

    def calculate_grid_position(
        self, y: int = 0, x: int = 0
    ) -> tuple[int, int, int, int]:
        row_block_index = y // 3
        col_block_index = x // 3
        row_in_block = y % 3
        col_in_block = x % 3
        return (row_block_index, col_block_index, row_in_block, col_in_block)

    def get_sudoku_block(self, block_y: int, block_x: int) -> SudokuBlock:
        return self.sudoku_grid[block_y][block_x]

    def delete_cell(self, y: int, x: int) -> None:
        row_block_index, col_block_index, row_in_block, col_in_block = (
            self.calculate_grid_position(y, x)
        )
        self.get_sudoku_block(row_block_index, col_block_index).delete_cell(
            row_in_block, col_in_block
        )

    def get_cell(self, y: int, x: int) -> CellData:
        row_block_index, col_block_index, row_in_block, col_in_block = (
            self.calculate_grid_position(y, x)
        )
        return self.get_sudoku_block(row_block_index, col_block_index).get_cell(
            row_in_block, col_in_block
        )

    def is_value_valid_in_block(self, y: int, x: int, cell_value: CellData) -> bool:
        row_block_index, col_block_index, _, _ = self.calculate_grid_position(y, x)
        return self.get_sudoku_block(row_block_index, col_block_index).is_value_valid(
            cell_value
        )

    def is_value_valid_in_row(self, y: int, cell_value: CellData) -> bool:
        row_block_index, _, row_in_block, _ = self.calculate_grid_position(y=y)
        for block_x in range(3):
            quadrante = self.get_sudoku_block(row_block_index, block_x)
            for x in range(3):
                if quadrante.sudoku_grid[row_in_block][x] == cell_value:
                    return False
        return True

    def is_value_valid_in_column(self, x: int, cell_value: CellData) -> bool:
        _, col_block_index, _, col_in_block = self.calculate_grid_position(x=x)
        for block_y in range(3):
            quadrante = self.get_sudoku_block(block_y, col_block_index)
            for y in range(3):
                if quadrante.sudoku_grid[y][col_in_block] == cell_value:
                    return False
        return True

    def is_block_valid(self, y: int, x: int) -> bool:
        row_block_index, col_block_index, _, _ = self.calculate_grid_position(y, x)
        return self.get_sudoku_block(row_block_index, col_block_index).is_block_valid()

    def generate_config_str(self) -> str:
        config_str = ""
        for y in range(9):
            for x in range(9):
                config_str += self.get_cell(y, x)
        return config_str

    def copy(self) -> "SudokuBoard":
        return SudokuBoard(self.generate_config_str())

    def is_column_valid(self, x: int) -> bool:
        board = self.copy()
        for y in range(9):
            cell_value = board.get_cell(y, x)
            board.set_cell(y, x, "0")
            if not (board.set_cell(y, x, cell_value)):
                return False
        return True

    def is_row_valid(self, y: int) -> bool:
        board = self.copy()
        for x in range(9):
            cell_value = board.get_cell(y, x)
            board.set_cell(y, x, "0")
            if not (board.set_cell(y, x, cell_value)):
                return False
        return True

    def is_board_valid(self) -> bool:
        board = self.copy()
        for y in range(9):
            for x in range(9):
                cell_value = board.get_cell(y, x)
                if cell_value == "0":
                    return False
                board.set_cell(y, x, "0")
                if not (board.set_cell(y, x, cell_value)):
                    return False
        return True

    def is_value_valid(self, y: int, x: int, v: CellData) -> bool:
        if not (self.is_value_valid_in_block(y, x, v)):
            return False
        if not (self.is_value_valid_in_column(x, v)):
            return False
        if not (self.is_value_valid_in_row(y, v)):
            return False
        return True

    def set_cell(self, y: int, x: int, cell_value: CellData) -> bool:
        row_block_index, col_block_index, row_in_block, col_in_block = (
            self.calculate_grid_position(y, x)
        )
        sudoku_block = self.get_sudoku_block(row_block_index, col_block_index)
        if cell_value not in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            raise ValueError("cell_value must be between '0' and '9'")
        if cell_value == "0":
            sudoku_block.set_element(row_in_block, col_in_block, "0")
            return True
        if self.is_value_valid(y, x, cell_value):
            sudoku_block.set_element(row_in_block, col_in_block, cell_value)
            return True
        return False

    def find_next_empty_cell(self) -> tuple[int, int] | None:
        for y in range(9):
            for x in range(9):
                if self.get_cell(y, x) == "0":
                    return (y, x)
        return None

    def get_possible_values(self, pos: tuple[int, int]) -> list[CellData]:
        possibilidades: list[CellData] = []
        for value in range(1, 10):
            cell_value = cast(CellData, str(value))
            if self.is_value_valid(pos[0], pos[1], cell_value):
                possibilidades.append(cell_value)
        return possibilidades

    def print_grid(self) -> None:
        for y in range(9):
            row = ""
            for x in range(9):
                row += self.get_cell(y, x)
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
            position_y = filled_cells_count // 9
            position_x = filled_cells_count % 9
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
            if char == "o":
                print("entry completely deleted")
                sudoku_board = SudokuBoard()
                filled_cells_count = 0
                continue
            if char == "s":
                sudoku_board.print_grid()
                continue
            if char == "e":
                return sudoku_board
            if char in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                sudoku_board.set_cell(position_y, position_x, char)
                print(f"element {char} added")
                filled_cells_count += 1
                continue
            print("enter a number between 0 and 9 or additional options")
            user_input += "0"
        print()
        sudoku_board.print_grid()
    return sudoku_board


def solve_sudoku_board(board: SudokuBoard) -> SudokuBoard | None:
    global tries
    if board.is_board_valid():
        return board
    empty_cell = board.find_next_empty_cell()
    if not empty_cell:
        return None
    possible_values = board.get_possible_values(empty_cell)
    for possible_value in possible_values:
        board_state = board.copy()
        board_state.set_cell(empty_cell[0], empty_cell[1], possible_value)
        tries += 1
        solucao = solve_sudoku_board(board_state)
        if solucao:
            return solucao
    return None


def solve_single_board(sudoku_board: SudokuBoard) -> None:
    sudoku_board.print_grid()
    print()
    global tries
    tries = 0
    start_time = time()
    solution_board = solve_sudoku_board(sudoku_board)
    if solution_board is None:
        print("no solution found")
        return
    solution_board.print_grid()
    end_time = time()
    print("\ntentativas: " + str(tries))
    print_elapsed_time(end_time - start_time)
    print("\n\n")


tries = 0
while True:
    mode = main_menu()
    if mode == 0:
        break
    if mode != 3:
        board = create_sudoku_board(mode)
        solve_single_board(board)
        continue
    files = os.listdir("sudokus")
    for file_name in files:
        print(f"{file_name}\n\n")
        with open(f"sudokus//{file_name}", "r", encoding="utf-8") as sudoku_board_raw:
            board = SudokuBoard(sudoku_board_raw.read())
        solve_single_board(board)
