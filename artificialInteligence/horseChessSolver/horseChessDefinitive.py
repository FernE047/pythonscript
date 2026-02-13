from time import time


MatrizData = bool | list["MatrizData"]


def format_elapsed_time(seconds: float) -> str:
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
    return f"{sign}{', '.join(parts)}"


class Board:
    def __init__(
        self, dimensions: int, board_size: int = 8, position: list[int] | None = None
    ) -> None:
        self.dimensions = dimensions
        self.board_size = board_size
        self.position = position
        if position is None:
            self.position = [0 for _ in range(dimensions)]
        self.matriz: MatrizData | "Board"
        if self.dimensions == 1:
            self.matriz = [False for _ in range(board_size)]
        else:
            self.matriz = Board(self.dimensions - 1, self.board_size)

    def set_position(self, position: list[int]) -> None:
        # TODO: implement set_position
        return

    def set_position_value(self, value: bool) -> None:
        # TODO: implement set_position_value
        return


def create_square_matriz(dimensions: int, size: int = 8) -> MatrizData:
    if dimensions == 0:
        return False
    else:
        return [create_square_matriz(dimensions - 1, size) for _ in range(size)]


def create_square_board(dimensions: int, size: int = 8) -> Board:
    # TODO: implement create_square_board
    return Board(dimensions, size)  # boilerplate


def resolve_board(board: Board) -> None:
    # TODO: implement solver
    return None


def resolve_one_board(board: Board) -> None:
    print()
    tries = 0
    begin = time()
    resolve_board(board)
    end = time()
    print(f"\ntries: {tries}")
    duration = end - begin
    print(f"\n{format_elapsed_time(duration)}\n\n\n")


def main() -> None:
    board = create_square_board(3, 5)
    print(board)
    resolve_one_board(board)


if __name__ == "__main__":
    main()
