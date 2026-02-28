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
    level_board = 0  # limite:270 2 cores
    while True:
        start_time = time.time()
        shared_board = 8 * level_board + 8
        total_board = 9 * level_board + 9
        total = [1, 0, 0, 0, 0]
        filas = [0, 0, 0, 0, 0]
        for pecasFora in range(4):
            for pecasDentro in range(1, 5 - pecasFora):
                filas[pecasFora] = compute_repetitions(level_board + 1, pecasDentro)
        shared_minus: list[int] = []
        for espacosOcupados in range(shared_board + 1):
            shared_minus.append(0)
            for pecas in range(1, 5):
                shared_minus[espacosOcupados] += compute_repetitions(
                    total_board - espacosOcupados, pecas
                )

        # 1 color calculus

        for pecas in range(1, 5):
            total[1] += compute_repetitions(total_board, pecas)

        # 2 color calculus

        for ocuppied in range(5):
            for pecas in range(ocuppied, 5):
                mult = 1
                mult *= space_piece(ocuppied, pecas)
                mult *= compute_combinations(shared_board, pecas)
                mult *= shared_minus[ocuppied]
                mult *= filas[4 - ocuppied] + 1
                total[2] += mult

        # 3 color calculus

        # Apresentação
        print(f"\nlevel: {level_board}")
        for elemento in total:
            print(f"{elemento}")
        end_time = time.time()
        real_time = end_time - start_time
        print(f"{real_time} seconds")


if __name__ == "__main__":
    main()
