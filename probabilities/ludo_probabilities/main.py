import time

# incomplete code, only adding type hints and Englishirizing everything

# common function


def calculate_factorial(value: int) -> int:
    factorial_result = 1
    if value > 0:
        for current_number in range(value, 0, -1):
            factorial_result *= current_number
    return factorial_result


def compute_combinations(path_length: int, game_pieces: int) -> int:
    numerator_combinations = calculate_factorial(path_length)
    denominator_combinations = calculate_factorial(game_pieces) * calculate_factorial(
        path_length - game_pieces
    )
    return int(numerator_combinations / denominator_combinations)


def compute_repetitions(path_length: int, game_pieces: int) -> int:
    total_steps_in_game = path_length + game_pieces - 1
    total = compute_combinations(total_steps_in_game, game_pieces)
    return total


def space_piece(space: int, piece: int) -> int:
    total = compute_repetitions(space, piece - space)
    return total


def main() -> None:

    start_time = time.time()
    end_time = time.time()
    real_time = end_time - start_time
    level_board = 0  # limit:270 2 cores
    while True:
        start_time = time.time()
        shared_board = 8 * level_board + 8
        total_board = 9 * level_board + 9
        total = [1, 0, 0, 0, 0]
        pieces_in_rows = [0, 0, 0, 0, 0]
        for pieces_outside in range(4):
            for pieces_inside in range(1, 5 - pieces_outside):
                pieces_in_rows[pieces_outside] = compute_repetitions(
                    level_board + 1, pieces_inside
                )
        shared_minus: list[int] = []
        for occupied_spaces in range(shared_board + 1):
            shared_minus.append(0)
            for pieces in range(1, 5):
                shared_minus[occupied_spaces] += compute_repetitions(
                    total_board - occupied_spaces, pieces
                )

        # 1 color calculus

        for pieces in range(1, 5):
            total[1] += compute_repetitions(total_board, pieces)

        # 2 color calculus

        for occupied in range(5):
            for pieces in range(occupied, 5):
                color_combination_multiplier = 1
                color_combination_multiplier *= space_piece(occupied, pieces)
                color_combination_multiplier *= compute_combinations(
                    shared_board, pieces
                )
                color_combination_multiplier *= shared_minus[occupied]
                color_combination_multiplier *= pieces_in_rows[4 - occupied] + 1
                total[2] += color_combination_multiplier

        # 3 color calculus

        # Presentation
        print(f"\nlevel: {level_board}")
        for element in total:
            print(f"{element}")
        end_time = time.time()
        real_time = end_time - start_time
        print(f"{real_time} seconds")


if __name__ == "__main__":
    main()
