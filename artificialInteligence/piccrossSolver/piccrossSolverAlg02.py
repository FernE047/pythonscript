from time import time
from PIL import Image

BoardData = list[list[bool]]
HintData = list[int]
HintHorizontalData = list[HintData]
VerticalHintData = tuple[int, int]
HintVerticalData = list[VerticalHintData]
HintsData = tuple[HintHorizontalData, HintVerticalData]
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


class CounterManager:
    def __init__(self) -> None:
        self.attempts = 0
        self.heuristic_cuts = 0

    def increment_attempts(self) -> None:
        self.attempts += 1

    def increment_cuts(self) -> None:
        self.heuristic_cuts += 1

    def reset_all(self) -> None:
        self.attempts = 0
        self.heuristic_cuts = 0

    def display(self) -> None:
        print(f"\nAttempts : {self.attempts}")
        print(f"\nCuts : {self.heuristic_cuts}")

    def __str__(self) -> str:
        return f"\nAttempts : {self.attempts}\nCuts : {self.heuristic_cuts}"


def save_board_image(board: BoardData, filename: str) -> None:
    image = Image.new("RGBA", (len(board[0]), len(board)), (255, 255, 255, 255))
    for y, column in enumerate(board):
        for x, cell in enumerate(column):
            if cell:
                image.putpixel((x, y), (0, 0, 0, 255))
    image.save(f"{filename}.png")
    image.close()


def compare_states(
    states: list[int], hint: list[int], previous_cell: bool, limit: int, size: int
) -> bool:
    if hint[0] == 0:
        if states:
            return False
        else:
            return True
    if len(states) > len(hint):
        return False
    if not states:
        if size - (limit + 1) < len(hint) + sum(hint) - 1:
            return False
        return True
    index = -1
    if len(states) > 1:
        for index, state in enumerate(states[:-1]):
            if state != hint[index]:
                return False
    if not previous_cell:
        if states[index + 1] != hint[index + 1]:
            return False
        if len(states) < len(hint):
            if (
                size - (limit + 1)
                < len(hint[len(states) :]) + sum(hint[len(states) :]) - 1
            ):
                return False
    else:
        if states[index + 1] > hint[index + 1]:
            return False
        if states[index + 1] == hint[index + 1]:
            if (
                size - (limit + 1)
                < len(hint[len(states) :]) + sum(hint[len(states) :]) - 2
            ):
                return False
        else:
            if (
                size - (limit + 1)
                < len(hint[len(states) :])
                + sum(hint[len(states) :])
                + hint[index + 1]
                - states[index + 1]
                - 1
            ):
                return False
    return True


def verificaColunasParcial(
    game: GameData, limit_y: int, minimum_x: int, limit_x: int
) -> bool:
    if minimum_x != 0:
        minimum_x -= 1
    for x in range(minimum_x, limit_x):
        hint = game[1][0][x]
        state: list[int] = []
        previous_cell = False
        count = 0
        for y in range(limit_y + 1):
            cell = game[0][y][x]
            if previous_cell:
                if cell:
                    count += 1
                else:
                    state.append(count)
            else:
                if cell:
                    count = 1
            previous_cell = cell
        if previous_cell:
            state.append(count)
        if not compare_states(state, hint, previous_cell, limit_y, len(game[0])):
            return False
    return True


def solve_board(game: GameData, counter_manager: CounterManager) -> BoardData | None:
    # TODO fix game, it should be mutable
    board = game[0]
    hints = game[1]
    vertical_hints = hints[1]
    horizontal_hints = hints[0]
    if not vertical_hints:
        return board
    current_hint = vertical_hints.pop(0)
    if current_hint[1] == 0:
        solved_board = solve_board(game, counter_manager)
        if solved_board:
            return solved_board
        game = (board, (horizontal_hints, [current_hint] + vertical_hints))
        return None
    y = current_hint[0]
    first_free_space = -1
    board_width = len(horizontal_hints)
    for x in range(board_width):
        if board[y][x]:
            first_free_space = x
    if first_free_space != -1:
        first_free_space += 2
    else:
        first_free_space = 0
    current_y_hints: list[VerticalHintData] = []
    if vertical_hints:
        for hint in vertical_hints:
            if hint[0] != y:
                break
            current_y_hints.append(hint)
        additional_hints_size = len(current_y_hints) + sum(
            [hint[1] for hint in current_y_hints]
        )
    else:
        additional_hints_size = 0
    total_free_space = len(horizontal_hints) - first_free_space - additional_hints_size
    if current_hint[1] > total_free_space:
        game = (board, (horizontal_hints, [current_hint] + vertical_hints))
        return None
    if (current_hint[1] == total_free_space) and (current_y_hints):
        for x in range(first_free_space, first_free_space + current_hint[1]):
            board[y][x] = True
        x_limit = first_free_space + current_hint[1] - 1
        for hint in current_y_hints:
            vertical_hints.pop(0)
            for x in range(x_limit + 2, x_limit + hint[1] + 2):
                board[y][x] = True
            if verificaColunasParcial(game, y, first_free_space, len(board[0])):
                counter_manager.increment_cuts()
                solved_board = solve_board(game, counter_manager)
                if solved_board:
                    return solved_board
        for x in range(first_free_space, len(board[0])):
            board[y][x] = False
        game = (board, (horizontal_hints, current_y_hints + vertical_hints))
    else:
        for inicial in range(
            first_free_space,
            board_width - current_hint[1] + 1 - additional_hints_size,
        ):
            for x in range(inicial, inicial + current_hint[1]):
                board[y][x] = True
            if verificaColunasParcial(
                game, y, first_free_space, inicial + current_hint[1]
            ):
                counter_manager.increment_attempts()
                solved_board = solve_board(game, counter_manager)
                if solved_board:
                    return solved_board
            for x in range(inicial, inicial + current_hint[1]):
                board[y][x] = False
    game = (board, (horizontal_hints, [current_hint] + vertical_hints))
    return None


def solve_piccross_board(
    game: GameData, timer_manager: TimeManager, counter_manager: CounterManager
) -> BoardData | None:
    print()
    counter_manager.reset_all()
    timer_manager.start()
    solution_board = solve_board(game, counter_manager)
    timer_manager.stop()
    counter_manager.display()
    for linha in game[0]:
        row = ""
        for element in linha:
            if element:
                row += "#"
                continue
            row += "0"
        print(row)
    timer_manager.print_elapsed_time()
    return solution_board


def main() -> None:
    timer_manager = TimeManager()
    counter_manager = CounterManager()
    for index in range(8):
        with open(f"piccross/A{index:03d}.txt") as piccross_file:
            config = piccross_file.read()
        horizontal_hints_lines, vertical_hints_text = config.split("#")
        horizontal_hints: HintHorizontalData = [
            [int(n) for n in hint.split()]
            for hint in horizontal_hints_lines[:-1].split("\n")
        ]
        vertical_hints_lines = vertical_hints_text[1:].split("\n")
        vertical_hints: HintVerticalData = []
        for y, dica in enumerate(vertical_hints_lines):
            for numero in dica.split():
                vertical_hints.append((y, int(numero)))
        tabuleiro: BoardData = []
        for _ in vertical_hints_lines:
            tabuleiro.append([False for _ in horizontal_hints])
        dicas: HintsData = (horizontal_hints, vertical_hints)
        game: GameData = (tabuleiro, dicas)
        solve_piccross_board(game, timer_manager, counter_manager)
        timer_manager.print_elapsed_time(print_total=True)
        save_board_image(tabuleiro, f"piccross/A{index:03d}")


if __name__ == "__main__":
    main()
