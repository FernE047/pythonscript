from time import time


class TimeCounter:
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
        self.print_elapsed_time(print_total=False)

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


def resolve_board(
    board: tuple[list[list[bool]], tuple[int, int]],
) -> list[tuple[int, int]] | None:  # TODO: implement solver
    return None


def solve_one_board(
    board: tuple[list[list[bool]], tuple[int, int]], timer: TimeCounter
) -> None:
    print()
    tries = 0
    timer.start()
    resolve_board(board)
    timer.stop()
    print("\ntries: " + str(tries))
    timer.print_elapsed_time()


def main() -> None:
    timer = TimeCounter()
    for pos in (
        (0, 0),
        (0, 1),
        (0, 2),
        (0, 3),
        (1, 1),
        (1, 2),
        (1, 3),
        (2, 2),
        (2, 3),
        (3, 3),
    ):
        matriz = [[False for _ in range(8)] for _ in range(8)]
        matriz[pos[0]][pos[1]] = True
        board = (matriz, pos)
        solve_one_board(board, timer)
    timer.print_elapsed_time(print_total=True)


if __name__ == "__main__":
    main()
