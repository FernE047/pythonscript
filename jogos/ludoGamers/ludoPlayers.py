from string import ascii_uppercase
from typing import Any
import numpy.random as npr
import math

# this code is incomplete, so I am only changing what I can to stop linter errors.

# Constants initialization

FINAL_WALK_LENGTH = 5  # size of the final walk after the main board, it is not necessary to be 5 but it is a common size for ludo boards
LUDO_PIECE_COUNT = 4  # how many pieces each player has, it is not necessary to be 4 but it is a common size for ludo boards
NUMBER_OF_DICE = 6  # how many dice will be rolled in a turn, 1 die only reduces the strategies that can be used
NUM_DICE_SIDES = 6  # how many faces the dice have
TOTAL_PLAYERS = 4  # total number of players the board can have
ACTIVE_PLAYER_COUNT = 4  # number of players that will be playing, if it is less than the total number of players, the order on the board is chosen randomly
EXIT_NUMBER: tuple[int, ...] = (
    1,
)  # the number you need to roll to get a piece out of the starting area, it is common to be 1.
JOGADORES_CORES = [
    "red",
    "yellow",
    "blue",
    "green",
    "purple",
    "pink",
    "orange",
    "brown",
    "gray",
    "cyan",
    "lime",
    "aqua",
    "light-green",
    "black",
]
ALPHABET = list(ascii_uppercase)

BoardData = list[list[str]]

# DEBUG functions


def print_list_debug(items: list[Any], title: str) -> None:
    print(f"{title}\n")
    for index, item in enumerate(items):
        print(f"{index} : {item}")
    print()


def print_dict_debug(dictionary: dict[Any, Any], title: str) -> None:
    print(f"{title}\n")
    for index, (key, value) in enumerate(dictionary.items()):
        print(f"{index} : {key} : {value}")
    print()


# initialization functions


def generate_player_name(player_index: int) -> str:
    digits_count = 1
    if player_index > 0:
        digits_count = int(math.log(player_index, 10) + 1)
    modulus = player_index % 26
    division = player_index // 26
    letter = ALPHABET[modulus]
    player_name = f"{letter}{division:0{digits_count}d}"
    return player_name


def generate_player_pieces(player_index: int) -> list[str]:
    player_name = generate_player_name(player_index)
    digits_count = 1
    if player_index > 0:
        digits_count = int(math.log(LUDO_PIECE_COUNT, 10) + 1)
    player_piece_names = [
        f"{player_name}-{int(piece_index):0{digits_count}d}"
        for piece_index in range(LUDO_PIECE_COUNT)
    ]
    return player_piece_names


# booleans functions


def is_game_over(player_positions: dict[str, str | int]) -> bool:
    for position in player_positions.values():
        if position != "win":
            return False
    return True


# getters functions


def get_player_by_index(player_index: int, player_order: dict[int, str]) -> str:
    current_player = player_order[player_index]
    return current_player


def get_player_color_by_index(
    player_index: int, player_colors: dict[str, str], player_order: dict[int, str]
) -> str:
    color = player_colors[get_player_by_index(player_index, player_order)]
    return color


def get_player_piece_positions(
    player_index: int,
    player_order: dict[int, str],
    player_pieces: dict[str, list[str]],
    piece_locations: dict[str, str | int],
) -> dict[str, str | int]:
    player_piece_positions: dict[str, str | int] = {}
    for piece in player_pieces[get_player_by_index(player_index, player_order)]:
        player_piece_positions[piece] = piece_locations[piece]
    return player_piece_positions


def get_strategy_by_player_index(
    player_index: int, player_order: dict[int, str], player_strategies: dict[str, str]
) -> str:
    current_strategy = player_strategies[
        get_player_by_index(player_index, player_order)
    ]
    return current_strategy


# basic game functions


def roll_dice() -> list[int]:
    results: list[int] = []
    for _ in range(NUMBER_OF_DICE):
        results.append(npr.randint(NUM_DICE_SIDES))
    return results


def execute_player_move(
    board: BoardData,
    player_index: int,
    player_colors: dict[str, str],
    player_turn_order: dict[int, str],
    player_strategies: dict[str, str],
    player_pieces: dict[str, list[str]],
    piece_locations: dict[str, str | int],
) -> BoardData:
    dice_rolls = roll_dice()
    color = get_player_color_by_index(player_index, player_colors, player_turn_order)
    strategy = get_strategy_by_player_index(
        player_index, player_turn_order, player_strategies
    )
    piece_positions = get_player_piece_positions(
        player_index, player_turn_order, player_pieces, piece_locations
    )
    player_info: dict[str, Any] = {
        "dice": dice_rolls,
        "piece_positions": piece_positions,
        "color": color,
        "order": player_index,
    }
    print(f"player {color} rolled: {','.join([str(dado) for dado in dice_rolls])}")
    if strategy == "random":
        board = play_random_move(board, player_info)
    return board


def update_piece_locations(
    board: BoardData, piece_locations: dict[str, str | int]
) -> dict[str, str | int]:
    for cell_index, cell in enumerate(board):
        if board[cell_index]:
            for piece in cell:
                if cell_index == len(board) - 1:
                    piece_locations[piece] = "win"
                else:
                    piece_locations[piece] = cell_index
    return piece_locations


def movePecaXtoY(
    piece: str,
    x: int,
    y: int,
    board: BoardData,
    piece_locations: dict[str, str | int],
    tamanhoTabuleiro: int,
) -> None:
    board[x].pop(int(piece))  # something is wrong here
    jogadorId = piece[: piece.find("-")]
    if y < tamanhoTabuleiro:
        casa = board[y]
        if casa:
            for pecaRival in casa:
                idRival = pecaRival[: piece.find("-")]
                if idRival != jogadorId:
                    piece_locations[pecaRival] = "sleep"
        board[y] = [piece]
        piece_locations[piece] = y
    else:
        board[y] += [piece]
        piece_locations[piece] = "fila"


def get_available_moves(
    board,  # type: ignore
    pieces,  # type: ignore
    dice,  # type: ignore
):
    for piece in pieces:  # type: ignore
        pass  # TODO: stopped coding here


# strategy functions


def play_random_move(board: BoardData, player: dict[str, Any]) -> BoardData:
    moves = get_available_moves(  # type: ignore
        board, player["piece_positions"], player["dice"]
    )
    del moves
    return board


def main() -> None:
    board_size = 2 * TOTAL_PLAYERS * (FINAL_WALK_LENGTH + 2)
    game_board: BoardData = []

    for _ in range(board_size + FINAL_WALK_LENGTH + 1):
        game_board.append([])

    # Inicialização das variaveis dos jogadores

    player_names: list[str] = []
    player_colors: dict[str, str] = {}
    player_turn_order: dict[int, str] = {}
    player_pieces: dict[str, list[str]] = {}
    piece_locations: dict[str, str | int] = {}
    player_strategies: dict[str, str] = {}
    player_draw_order_helper = npr.choice(
        [player_index for player_index in range(TOTAL_PLAYERS)], ACTIVE_PLAYER_COUNT, replace=False
    )
    player_draw_order = sorted(player_draw_order_helper)
    for player_index in range(ACTIVE_PLAYER_COUNT):
        player_name = generate_player_name(player_index)
        player_names.append(player_name)
        player_turn_order[player_draw_order[player_index]] = player_name
        if ACTIVE_PLAYER_COUNT <= 14:
            player_colors[player_name] = JOGADORES_CORES[player_index]
        player_pieces[player_name] = generate_player_pieces(player_index)
        for piece in player_pieces[player_name]:
            piece_locations[piece] = "sleep"
        player_strategies[player_name] = "random"

    # deletar variaveis não reutilizaveis

    del player_draw_order, player_draw_order_helper

    # DEBUG

    print(f"size : {board_size}")
    print_list_debug(game_board, "board : ")
    print_list_debug(player_names, "players : ")
    print_dict_debug(player_strategies, "strategies : ")
    print_dict_debug(player_pieces, "pieces : ")
    print_dict_debug(piece_locations, "piece locations : ")
    print_dict_debug(player_colors, "colors : ")
    print_dict_debug(player_turn_order, "order : ")

    # Jogo

    while not (is_game_over(piece_locations)):
        for player_index in range(TOTAL_PLAYERS):
            if player_index in player_turn_order.keys():
                game_board = execute_player_move(
                    game_board,
                    player_index,
                    player_colors,
                    player_turn_order,
                    player_strategies,
                    player_pieces,
                    piece_locations,
                )
                piece_locations = update_piece_locations(game_board, piece_locations)


if __name__ == "__main__":
    main()
