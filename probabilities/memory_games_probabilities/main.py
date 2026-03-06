import random
import time
from typing import Any
from datetime import timedelta

IS_DEBUG = False
IS_INPUT_ALLOWED = False
GAME_COUNT_DEFAULT = 1000
PAIR_COUNT_DEFAULT = 4


def print_debug(*args: Any, **kwargs: Any) -> None:
    if IS_DEBUG:
        print(*args, **kwargs)


def get_input(prompt: str, default: int) -> int:
    if IS_INPUT_ALLOWED:
        try:
            return int(input(prompt))
        except ValueError:
            print(f"Invalid input, using default value. (default: {default})")
    print_debug(f"{prompt} (default: {default})")
    return default


def is_board_clean(board: list[int]) -> bool:
    for cell_value in board:
        if cell_value != -1:
            return False
    return True


def is_valid_move(board: list[int], move: int | list[int]) -> bool:
    if isinstance(move, list):
        for index in move:
            if board[index] == -1:
                return False
    else:
        if board[move] == -1:
            return False
    return True

def random_move(board: list[int]) -> int:
    return random.randint(0, len(board) - 1)


def make_move(board: list[int], quant: int) -> int:
    move = 0
    while True:
        move = random_move(board)
        while not (is_valid_move(board, move)):
            move = random_move(board)
        return move


def main() -> None:
    while True:
        total_game_count = get_input("Game Amount", GAME_COUNT_DEFAULT)
        total_pairs = get_input("Pair Amount", PAIR_COUNT_DEFAULT)
        game_results: list[int] = []
        start_time = time.time()
        for game_index in range(total_game_count):
            print_debug(f"Game : {game_index + 1}")
            board: list[int] = []
            seen_pieces: list[int] = []
            for index in range(2 * total_pairs):
                pair_index = index // 2
                board.append(pair_index)
                seen_pieces.append(-1)
            random.shuffle(board)
            print_debug(board)
            selected_moves = [0, 0]
            total_moves = 0
            while not (is_board_clean(board)):
                selected_moves[0] = make_move(board, len(board) - 1)
                while True:
                    selected_moves[0] = random_move(board)
                    selected_moves[1] = random_move(board)
                    while not (is_valid_move(board, selected_moves)):
                        selected_moves[0] = random_move(board)
                        selected_moves[1] = random_move(board)
                    if selected_moves[0] != selected_moves[1]:
                        break
                if board[selected_moves[0]] == board[selected_moves[1]]:
                    board[selected_moves[0]] = -1
                    board[selected_moves[1]] = -1
                total_moves += 1
                print_debug(f"move : {selected_moves}\n{board}")
            game_results.append(total_moves)
            print_debug(total_moves)
        end_time = time.time()
        print(f"games count : {total_game_count}")
        print(f"\n\naverage: {sum(game_results) / total_game_count}")
        print(f"maximum: {max(game_results)}")
        print(f"minimum: {min(game_results)}")
        elapsed_time = end_time - start_time
        elapsed_time_str = str(timedelta(seconds=elapsed_time))
        print(f"Elapsed time: {elapsed_time_str}")
        if input("\nPress Enter to play again or type anything else to exit."):
            break


if __name__ == "__main__":
    main()
