from typing import Callable, Literal
from numpy.random import randint

USE_USER_INTERFACE = True
DEFAULT_STRATEGIES = [
    "random play",
    "mirror_x",
    "mirror_y",
    "mirror_diagonal",
    "mirror_diagonal_x",
    "spin_180_clockwise",
]
MINIMUM_ROUNDS = 1
MAXIMUM_BOARD_SIZE = 10
PLAYER_SYMBOLS = ["X", "O"]
DEFAULT_SYMBOL = " "
NEW_SEED_DIGIT_COUNT = 7
MAX_SEED = 10**NEW_SEED_DIGIT_COUNT - 1
MIN_SEED = 10 ** (NEW_SEED_DIGIT_COUNT - 1) + 1
SEED_SIZE = 4

CoordData = tuple[int, int]
PossibilitiesData = list[CoordData]
BoardData = list[list[str]]
ResultsOptions = Literal["Win", "Draw", "Continue"]


class Player:
    def __init__(self, symbol: str, strategy: str) -> None:
        self.symbol = symbol
        self.strategy = strategy
        self.victories = 0


def get_user_integer(
    prompt: str, minimum_value: int | None = None, maximum_value: int | None = None
) -> int:
    while True:
        user_input = input(f"{prompt} : ")
        try:
            valor = int(user_input)
            if (minimum_value is not None) and (valor < minimum_value):
                print(f"Value must be greater than or equal to {minimum_value}")
                continue
            if (maximum_value is not None) and (valor > maximum_value):
                print(f"Value must be less than or equal to {maximum_value}")
                continue
            return valor
        except Exception as _:
            print("Invalid value, please try again")


def choose_from_options(prompt: str, options: list[str]) -> str:
    while True:
        for index, option in enumerate(options):
            print(f"{index} - {option}")
        user_choice = input(prompt)
        try:
            return options[int(user_choice)]
        except (ValueError, IndexError):
            user_choice = input("Invalid Value, please try again: ")


def display_board(board: BoardData) -> None:
    if not USE_USER_INTERFACE:
        return
    size = len(board)
    row_headers = [str(index) for index in range(size)]
    headers = " ".join(row_headers)
    print(f" {headers}")
    separator_line = f" {'+'.join(['-' for _ in range(size)])}"
    for row_index, row in enumerate(board):
        row_display = str(row_index)
        for cell_index, cell_value in enumerate(row):
            row_display += str(cell_value)
            if cell_index != size - 1:
                row_display += "|"
        print(row_display)
        if row_index != size - 1:
            print(separator_line)
    print()


def check_main_diagonal_win(board: BoardData) -> bool:
    size = len(board)
    player_symbol = board[0][0]
    if player_symbol == DEFAULT_SYMBOL:
        return False
    for x in range(size):
        cell = board[x][x]
        if cell != player_symbol:
            return False
    return True


def check_anti_diagonal_win(board: BoardData) -> bool:
    size = len(board)
    player_symbol = board[0][-1]
    if player_symbol == DEFAULT_SYMBOL:
        return False
    for x in range(size):
        anti_x = size - 1 - x
        cell = board[x][anti_x]
        if cell != player_symbol:
            return False
    return True


def check_win_row(board: BoardData, row_index: int) -> bool:
    size = len(board)
    player_symbol = board[row_index][0]
    if player_symbol == DEFAULT_SYMBOL:
        return False
    for x in range(size):
        cell = board[row_index][x]
        if cell != player_symbol:
            return False
    return True


def check_win_rows(board: BoardData) -> bool:
    size = len(board)
    for y in range(size):
        if check_win_row(board, y):
            return True
    return False


def check_win_column(board: BoardData, column_index: int) -> bool:
    size = len(board)
    player_symbol = board[0][column_index]
    if player_symbol == DEFAULT_SYMBOL:
        return False
    for y in range(size):
        cell = board[y][column_index]
        if cell != player_symbol:
            return False
    return True


def check_win_columns(board: BoardData) -> bool:
    size = len(board)
    for x in range(size):
        if check_win_column(board, x):
            return True
    return False


def check_win(board: BoardData) -> bool:
    if check_main_diagonal_win(board):
        return True
    if check_anti_diagonal_win(board):
        return True
    if check_win_rows(board):
        return True
    if check_win_columns(board):
        return True
    return False


def check_draw(board: BoardData) -> bool:
    available_moves = play_random(board)
    if len(available_moves) == 0:
        return True
    return False


def evaluate_game_status(board: BoardData, player_symbol: str) -> ResultsOptions:
    if check_win(board):
        if USE_USER_INTERFACE:
            print(f"{player_symbol} Ganhou\n\n")
        return "Win"
    if check_draw(board):
        if USE_USER_INTERFACE:
            print("Deu velha\n\n")
        return "Draw"
    return "Continue"


def generate_new_seed(seed: int) -> int:
    while seed == 0:
        seed = randint(MIN_SEED, MAX_SEED)
    seed_squared = seed**2
    seed_str = list(str(seed_squared))
    while len(seed_str) > NEW_SEED_DIGIT_COUNT:
        seed_str.pop(0)
        if len(seed_str) == NEW_SEED_DIGIT_COUNT:
            break
        seed_str.pop()
    new_seed = int("".join(seed_str))
    return new_seed


def play_random(board: BoardData) -> PossibilitiesData:
    size = len(board)
    available_moves: PossibilitiesData = []
    for y in range(size):
        for x in range(size):
            if board[y][x] != DEFAULT_SYMBOL:
                continue
            available_moves.append((y, x))
    return available_moves


def play_human(board: BoardData) -> PossibilitiesData:
    size = len(board)
    while True:
        y = get_user_integer("enter position Y", 0, size - 1)
        x = get_user_integer("enter position X", 0, size - 1)
        if board[y][x] == DEFAULT_SYMBOL:
            return [(y, x)]
        print("position already used")


def play_mirror_x(board: BoardData) -> PossibilitiesData:
    # if the cell is empty, and the mirror cell is not empty, play in this cell
    size = len(board)
    available_moves: PossibilitiesData = []
    for y in range(size):
        for x in range(size):
            if board[y][x] != DEFAULT_SYMBOL:
                continue
            mirror_x = size - 1 - x
            mirror_cell = board[y][mirror_x]
            if mirror_cell == DEFAULT_SYMBOL:
                continue
            available_moves.append((y, mirror_x))
    return available_moves


def play_mirror_y(board: BoardData) -> PossibilitiesData:
    size = len(board)
    available_moves: PossibilitiesData = []
    for y in range(size):
        for x in range(size):
            if board[y][x] != DEFAULT_SYMBOL:
                continue
            mirror_y = size - 1 - y
            mirror_cell = board[mirror_y][x]
            if mirror_cell == DEFAULT_SYMBOL:
                continue
            available_moves.append((mirror_y, x))
    return available_moves


def play_spin_180_clockwise(board: BoardData) -> PossibilitiesData:
    size = len(board)
    available_moves: PossibilitiesData = []
    for y in range(size):
        for x in range(size):
            if board[y][x] != DEFAULT_SYMBOL:
                continue
            spin_180_x = size - 1 - x
            spin_180_y = size - 1 - y
            spin_180_cell = board[spin_180_y][spin_180_x]
            if spin_180_cell == DEFAULT_SYMBOL:
                continue
            available_moves.append((spin_180_y, spin_180_x))
    return available_moves


def play_mirror_diagonal(board: BoardData) -> PossibilitiesData:
    size = len(board)
    available_moves: PossibilitiesData = []
    for y in range(size):
        for x in range(size):
            if board[y][x] != DEFAULT_SYMBOL:
                continue
            if board[x][y] == DEFAULT_SYMBOL:
                continue
            available_moves.append((x, y))
    return available_moves


def play_mirror_diagonal_x(board: BoardData) -> PossibilitiesData:
    size = len(board)
    available_moves: PossibilitiesData = []
    for y in range(size):
        for x in range(size):
            if board[y][x] != DEFAULT_SYMBOL:
                continue
            mirror_x = size - 1 - x
            mirror_y = size - 1 - y
            mirror_cell = board[mirror_y][mirror_x]
            if mirror_cell == DEFAULT_SYMBOL:
                continue
            available_moves.append((mirror_y, mirror_x))
    return available_moves


def play_move(board: BoardData, player: Player, seed: int) -> ResultsOptions:
    if USE_USER_INTERFACE:
        print(f"symbol {player.symbol} : \n")
    available_moves = execute_turn(board, player.strategy)
    total = len(available_moves)
    if total == 0:
        available_moves = execute_turn(board, "random play")
        total = len(available_moves)
    chosen_move = seed % total
    move_coordinates = available_moves[chosen_move]
    y, x = move_coordinates
    board[y][x] = player.symbol
    display_board(board)
    return evaluate_game_status(board, f"symbol {player.symbol}")


STRATEGY_MAP: dict[str, Callable[[BoardData], PossibilitiesData]] = {
    "random play": play_random,
    "mirror_x": play_mirror_x,
    "mirror_y": play_mirror_y,
    "mirror_diagonal": play_mirror_diagonal,
    "mirror_diagonal_x": play_mirror_diagonal_x,
    "spin_180_clockwise": play_spin_180_clockwise,
    "human": play_human,
}


def execute_turn(board: BoardData, strategy_name: str) -> PossibilitiesData:
    strategy = STRATEGY_MAP.get(strategy_name)
    if strategy is None:
        raise ValueError(f"Unknown strategy: {strategy_name}")
    return strategy(board)


def main() -> None:
    strategies = DEFAULT_STRATEGIES
    if USE_USER_INTERFACE:
        strategies += ["human"]
    while True:
        strategies = ["CHOOSE RANDOM"] + list(strategies)
        total_rounds = get_user_integer(
            f"how many rounds? MIN:{MINIMUM_ROUNDS}", minimum_value=MINIMUM_ROUNDS
        )
        board_size = get_user_integer(
            f"board size? MAX:{MAXIMUM_BOARD_SIZE}", maximum_value=MAXIMUM_BOARD_SIZE
        )
        board_area = board_size**2
        seed = 0
        player_one_strategy = choose_from_options(
            "Choose strategy for player 1", strategies
        )
        strategies.pop(0)
        if player_one_strategy == "CHOOSE RANDOM":
            strategies.remove("human")
            random_one = randint(len(strategies)) - 1
            random_two = randint(len(strategies)) - 1
            player_one_strategy = strategies[random_one]
            player_two_strategy = strategies[random_two]
            strategies.append("human")
        else:
            player_two_strategy = choose_from_options(
                "Choose strategy for player 2", strategies
            )
        players = [
            Player(PLAYER_SYMBOLS[0], player_one_strategy),
            Player(PLAYER_SYMBOLS[1], player_two_strategy),
        ]
        for _ in range(total_rounds):
            seed = generate_new_seed(seed)
            board = [
                [DEFAULT_SYMBOL for _ in range(board_size)] for _ in range(board_size)
            ]

            def faz_jogada(player: Player) -> ResultsOptions:
                return play_move(board, player, seed)

            display_board(board)
            for turn in range(board_area):
                player_turn = turn % 2
                current_player = players[player_turn]
                game_outcome = faz_jogada(current_player)
                if game_outcome == "Draw":
                    break
                if game_outcome == "Win":
                    current_player.victories += 1
                    break
        print(f"board size : {board_size}")
        print(f"board area : {board_area}")
        print(f"total rounds : {total_rounds}")
        victories_1 = players[0].victories
        ratio_1 = victories_1 * 100 / total_rounds
        victories_2 = players[1].victories
        ratio_2 = victories_2 * 100 / total_rounds
        draws = total_rounds - victories_1 - victories_2
        draw_ratio = draws * 100 / total_rounds
        print(
            f"player {players[0].symbol} won {victories_1} times, {ratio_1}%, with strategy {player_one_strategy}"
        )
        print(
            f"player {players[1].symbol} won {victories_2} times, {ratio_2}%, with strategy {player_two_strategy}"
        )
        print(f"Draws {draws} times, {draw_ratio}%")
        if "no" == choose_from_options("continue?", ["yes", "no"]):
            break


if __name__ == "__main__":
    main()
