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
GameData = tuple[BoardData, HintsData]


class TimeManager:
    def __init__(self) -> None:
        self.total_time = 0.0
        self.start_time = 0.0
        self.end_time = 0.0
        self.elapsed_time = 0.0

    def start(self) -> None:
        self.start_time = time()

    def stop(self) -> None:
        self.end_time = time()
        self.elapsed_time = self.end_time - self.start_time
        self.total_time += self.elapsed_time

    def print_elapsed_time(self, print_total: bool = False) -> None:
        elapsed_time = self.elapsed_time
        if print_total:
            elapsed_time = self.total_time
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


def calculate_space(dica: HintData) -> int:
    return len(dica) + sum(dica) - 1


def solve_verticals(game: GameData) -> None:
    vertical_hints = game[1][0]
    board = game[0]
    for x, hint in enumerate(vertical_hints):
        board_height = len(board)
        current_space = calculate_space(hint)
        free_spaces = board_height - current_space
        if free_spaces == board_height:
            for y in range(0, board_height):
                board[y][x] = -1
            continue
        if free_spaces == 0:
            y = -2
            for number_hint in hint:
                y += 2
                if y != 0:
                    board[y - 1][x] = -1
                for y in range(y, y + number_hint):
                    board[y][x] = 1
            continue
        if free_spaces >= max(hint):
            continue
        for hint_index, number_hint in enumerate(hint):
            if free_spaces >= number_hint:
                continue
            if hint_index == 0:
                last_y = number_hint - 1
            else:
                last_y = calculate_space(hint[hint_index:])
            if hint_index == len(hint) - 1:
                first_y = board_height - number_hint
            else:
                first_y = calculate_space(hint[: hint_index + 1])
            for y in range(first_y, last_y):
                board[y][x] = 1


def solve_horizontals(game: GameData) -> None:
    horizontal_hints = game[1][1]
    board = game[0]
    for y, hint in enumerate(horizontal_hints):
        board_width = len(board[0])
        current_space = calculate_space(hint)
        free_spaces = board_width - current_space
        if free_spaces == board_width:
            for x in range(0, board_width):
                board[y][x] = -1
            continue
        if free_spaces == 0:
            x = -2
            for number_hint in hint:
                if x != -2:
                    board[y][x + 1] = -1
                for x in range(x + 2, x + 2 + number_hint):
                    board[y][x] = 1
            continue
        if free_spaces >= max(hint):
            continue
        for hint_index, number_hint in enumerate(hint):
            if free_spaces >= number_hint:
                continue
            if hint_index == 0:
                last_x = number_hint - 1
            else:
                last_x = calculate_space(hint[hint_index:])
            if hint_index == len(hint) - 1:
                first_x = board_width - number_hint
            else:
                first_x = calculate_space(hint[: hint_index + 1])
            for x in range(first_x, last_x):
                board[y][x] = 1


def solve_board(game: GameData) -> BoardData:
    solve_horizontals(game)
    solve_verticals(game)
    return game[0]


def save_board_image(board: BoardData, file_name: str) -> None:
    image = Image.new("RGBA", (len(board[0]), len(board)), (255, 255, 255, 255))
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            if cell == 1:
                image.putpixel((x, y), (0, 0, 0, 255))
    image.save(f"{file_name}.png")
    image.close()


def solve_piccross_board(game: GameData, time_manager: TimeManager) -> BoardData:
    print()
    time_manager.start()
    solution_board = solve_board(game)
    time_manager.stop()
    time_manager.print_elapsed_time()
    completed_count = 0
    element_count = 0
    for row in solution_board:
        row_str = ""
        for element in row:
            element_count += 1
            completed_count += 1
            if element == 1:
                row_str += "#"
                continue
            if element == 0:
                row_str += "?"
                completed_count -= 1
                continue
            row_str += "0"
        print(row_str)
    print("\n\nPorcentagem : " + str(100 * completed_count / element_count) + "%")
    return solution_board


def main() -> None:
    time_manager = TimeManager()
    for index in range(8):
        with open(f"piccross/A{index:03d}.txt") as piccross_file:
            config = piccross_file.read()
        horizontal_hints_lines, vertical_hints_lines = config.split("#")
        horizontal_hints: HintAxysData = [
            [int(n) for n in hint.split()]
            for hint in horizontal_hints_lines[:-1].split("\n")
        ]
        vertical_hints: HintAxysData = [
            [int(n) for n in hint.split()]
            for hint in vertical_hints_lines[1:].split("\n")
        ]
        board: BoardData = []
        for _ in vertical_hints:
            board.append([0 for _ in horizontal_hints])
        all_hints: HintsData = (horizontal_hints, vertical_hints)
        game: GameData = (board, all_hints)
        solution_board = solve_piccross_board(game, time_manager)
        time_manager.print_elapsed_time(print_total=True)
        save_board_image(solution_board, f"piccross/A{index:03d}")


if __name__ == "__main__":
    main()
