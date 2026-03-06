from time import time
from datetime import timedelta


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
        self.print_elapsed_time()

    def print_elapsed_time(self, print_total: bool = False) -> None:
        if print_total:
            print(f"\nTotal time: {str(timedelta(seconds=self.total_time))}\n\n\n")
        else:
            print(f"\nElapsed time: {str(timedelta(seconds=self.elapsed_time))}\n\n\n")


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
    print(f"\ntries: {tries}")


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
