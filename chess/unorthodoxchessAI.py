from itertools import permutations as perm
from typing import Any, Literal, TypeAlias, TypedDict, cast

"""
PIECES:

walkers = 0 (rook)
jumpers = 1 (horses)
summers = 2 (queen)
custom = 3 (pawn)
multiDimensionalSteper = 4 (king)
square = 5 (king)
jumpWalker = 6 (none)

VICTORY:

check-mate = 0
check = 1
capture = 2
capture-All = 3

"""
"""
Camila Reis 02/02/2026 DD/MM/YYYY
This code is old and at the time of writing it I was still learning Python.
in this revision, I fixed some issues and added type hints.
and I have 100% translated variable and function names to English in underline case.
However, the code is still incomplete and may contain bugs.
I am only adding type hints that work for current code structure, to make it actually unorthodox the type hints would need to be more complex.
most times cast is used, it's where something in the code logic is probably wrong but I didn't want to change it.
"""


PieceOptions = Literal["P", "R", "N", "B", "Q", "K", " ", "█"]
PiecePositionData = tuple[PieceOptions, list[int]]
PieceTypeOptions = Literal[0, 1, 2, 3, 4, 5, 6]
MovementData = int | tuple[int] | tuple[int, int]
CaptureMovementData = MovementData | list[tuple[int, int]]
PieceBehaviorData: TypeAlias = (
    tuple[PieceTypeOptions, Literal[False], MovementData, CaptureMovementData, int]
    | tuple[PieceTypeOptions, Literal[True], MovementData, int]
)
VictoryConditionOptions = Literal[0, 1, 2, 3]
VictoryConditionData = tuple[VictoryConditionOptions, PieceOptions]
PositionData = list[int] | None
PlayerOptions = Literal[0, 1, 2]


class CellData(TypedDict):
    piece: PieceOptions
    player: PlayerOptions


BoardData = CellData | list["BoardData"]  # multi-dimensional board


def show_board(board: BoardData, position: list[int] | None = None) -> None:
    if position is None:
        position = []
    if len(position) == 0:
        if isinstance(board, list):
            for boardy in board:
                show_board(boardy)
            print()
        else:
            print(
                board["piece"]
                + (board["piece"] if board["player"] == 0 else str(board["player"])),
                end="",
            )
    else:
        boardy = cast(list[BoardData], board)
        show_board(boardy[position[0]], position[1:])


def create_board(
    dimensions: int = 2, board_size: int = 8, position: PositionData = None
) -> BoardData:
    if position is None:
        position = []
    if dimensions == 0:
        if sum(position) % 2:
            return {"piece": "█", "player": 0}
        else:
            return {"piece": " ", "player": 0}
    else:
        board: list[BoardData] = []
        for t in range(board_size):
            position.append(t)
            board.append(create_board(dimensions - 1, board_size, position))
            position.pop(-1)
    return board


def check_board(board: BoardData, position: list[int]) -> BoardData:
    if len(position) == 0:
        return board
    else:
        boardy = cast(list[BoardData], board)
        return check_board(boardy[position[0]], position[1:])


def apply_horizontal_symmetry(board: BoardData, current_dimension: int = -1) -> None:
    global board_size
    global board_dimensions
    if current_dimension == -1:
        current_dimension = board_dimensions
    if isinstance(board, int) or not isinstance(board, list):
        raise ValueError("Board structure does not match expected dimensions.")
    if current_dimension != 1:
        for index in range(board_size):
            apply_horizontal_symmetry(board[index], current_dimension - 1)
        return
    for n, piece in enumerate(board):
        piece = cast(CellData, piece)
        if piece["player"] != 0:
            board[board_size - n - 1]["piece"] = piece["piece"]  # type: ignore
            board[board_size - n - 1]["player"] = piece["player"]  # type: ignore


def apply_vertical_symmetry(
    board: BoardData,
    boardy: BoardData | None = None,
    current_dimension: int | None = None,
    position: list[int] | None = None,
) -> None:
    global board_size
    if position is None:
        position = []
    if boardy is None:
        boardy = board
    if current_dimension is None:
        global board_dimensions
        current_dimension = board_dimensions
    if current_dimension == 1:
        for n, peca in enumerate(boardy):
            peca = cast(CellData, peca)
            if peca["player"] != 0:
                reflected_position: list[int] = []
                reflected_position.append(board_size - position[0] - 1)
                position.append(n)
                places_piece(
                    board,
                    peca["piece"],
                    1 if peca["player"] == 2 else 2,
                    reflected_position + position[1:],
                )
                position.pop(-1)
        return
    boardy = cast(list[BoardData], boardy)
    for a in range(board_size):
        position.append(a)
        apply_vertical_symmetry(board, boardy[a], current_dimension - 1, position)
        position.pop(-1)


def rotate_board(
    board: BoardData,
    new_board: BoardData | None = None,
    boardy: BoardData | None = None,
    current_dimension: int | None = None,
    position: list[int] | None = None,
) -> BoardData | None:
    global board_size
    if position is None:
        position = []
    if boardy is None:
        boardy = board
    if current_dimension is None:
        global board_dimensions
        current_dimension = board_dimensions
    if new_board is None:
        new_board = create_board(board_dimensions, board_size)
    if current_dimension == 1:
        for n, peca in enumerate(boardy):
            peca = cast(CellData, peca)
            if peca["player"] != 0:
                alternative_position: list[int] = []
                position.append(n)
                for n, number in enumerate(position):
                    if n in (0, len(position) - 1):
                        alternative_position.append(board_size - number - 1)
                    else:
                        alternative_position.append(number)
                places_piece(
                    new_board, peca["piece"], peca["player"], alternative_position
                )
                position.pop(-1)
    else:
        for position_index in range(board_size):
            position.append(position_index)
            new_boardy = cast(list[BoardData], boardy)
            rotate_board(
                board,
                new_board,
                new_boardy[position_index],
                current_dimension - 1,
                position,
            )
            position.pop(-1)
    if current_dimension == board_dimensions:
        return new_board
    return None


def places_piece(
    board: BoardData,
    piece: PieceOptions,
    player: Literal[0, 1, 2],
    position: PositionData = None,
) -> None:
    if position is not None:
        if not isinstance(board, list):
            raise ValueError("Position provided does not match board structure.")
        if len(position) == 1:
            places_piece(board[position[0]], piece, player)
            return
        places_piece(board[position[0]], piece, player, position[1:])
        return
    if isinstance(board, dict):
        board["piece"] = piece
        board["player"] = player
        return
    for boardy in board:
        places_piece(boardy, piece, player)


def move_piece(board: BoardData, start_position: list[int], end_position: list[int]) -> None:
    piece = check_board(board, start_position)
    piece = cast(CellData, piece)
    places_piece(board, piece["piece"], piece["player"], end_position)
    clean = "█" if sum(start_position) % 2 else " "
    clean = cast(PieceOptions, clean)
    places_piece(board, clean, 0, start_position)

def find_the_pieces(
    board: BoardData,
    player_1_pieces: list[PiecePositionData],
    player_2_pieces: list[PiecePositionData],
    position: list[int] | None = None,
) -> tuple[list[PiecePositionData], list[PiecePositionData]]:
    if position is None:
        position = []
    if isinstance(board, list):
        for coordinate, boardy in enumerate(board):
            position.append(coordinate)
            find_the_pieces(boardy, player_1_pieces, player_2_pieces, position)
            position.pop(-1)
        return (player_1_pieces, player_2_pieces)
    if board["player"] == 1:
        player_1_pieces.append((board["piece"], position.copy()))
    if board["player"] == 2:
        player_2_pieces.append((board["piece"], position.copy()))
    return (player_1_pieces, player_2_pieces)


def jogadasPossiveisIndividuais(board:BoardData, piece: PiecePositionData, player: int) -> Any:
    global behaviors
    global board_dimensions
    global board_size
    behavior = behaviors[piece[0]]
    current_position = piece[1] #type: ignore
    if len(behavior) == 5:
        piece_type, is_static, movement, capture, piece_value = behavior  # type: ignore
    else:
        piece_type, is_static, movement, piece_value = behavior  # type: ignore
        capture = movement
    while len(movement) < board_dimensions:  # type: ignore
        movement.append(0)  # type: ignore
    while len(capture) < board_dimensions:  # type: ignore
        capture.append(0)  # type: ignore
    if piece_type == 0:
        for movimentoNovo in set(perm(movement)):  # type: ignore
            pass  # TODO: stopped coding here
    return current_position #added to avoid error


def find_possible_moves(board: BoardData, player_pieces: list[PiecePositionData], player: int) -> Any:
    moves: list[PositionData] = []
    for piece in player_pieces: #type: ignore
        moves.append() #type: ignore
    #TODO: stopped coding here
    return None

board_dimensions = 2
board_size = 8
game_board = create_board(board_dimensions, board_size)
behaviors: dict[PieceOptions, PieceBehaviorData] = {
    "P": (3, False, (1), [(1, 1), (1, -1)], 1),  # pawn
    "R": (0, True, (1), 5),  # rook
    "N": (1, True, (1, 2), 3),  # knight
    "B": (0, True, (1, 1), 3),  # bishop
    "Q": (2, True, (1, 3), 9),  # queen
    "K": (5, True, 1, 2),  # king
}
victory: VictoryConditionData = (0, "K")
places_piece(game_board, "R", 1, [0, 0])
places_piece(game_board, "N", 1, [0, 1])
places_piece(game_board, "B", 1, [0, 2])
places_piece(game_board, "P", 1, [1])
apply_horizontal_symmetry(game_board)
places_piece(game_board, "Q", 1, [0, 3])
places_piece(game_board, "K", 1, [0, 4])
apply_vertical_symmetry(game_board)
pieces_list: tuple[list[PiecePositionData], list[PiecePositionData]] = ([], [])
find_the_pieces(game_board, pieces_list[0], pieces_list[1])
game_board = cast(BoardData, rotate_board(game_board))
show_board(game_board)
current_player_turn = 0
round_number = 0
while True:
    jogadasPossiveis = find_possible_moves(
        game_board, pieces_list[current_player_turn], current_player_turn + 1
    )
