from time import time
from datetime import timedelta


MatrizData = bool | list["MatrizData"]


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
    print(f"\n{str(timedelta(seconds=duration))}\n\n\n")


def main() -> None:
    board = create_square_board(3, 5)
    print(board)
    resolve_one_board(board)


if __name__ == "__main__":
    main()
