from random import randint

POWER = 5
SEED_SIZE = 4
PERCENTAGE_THRESHOLD = 1


def calculate_next_seed(current_seed: int) -> int:
    next_seed = current_seed**POWER
    next_list = list(str(next_seed))
    while len(next_list) > SEED_SIZE:
        next_list.pop()
    return int("".join(next_list))


def print_details(num: int, indice: int) -> None:
    print(f"{indice:0{SEED_SIZE}d} : {num}")


def evaluate_probability(seed_index: int, seed_history: list[int]) -> bool:
    frequency_count = [0 for _ in range(seed_index)]
    for seed_number in seed_history:
        frequency_count[seed_number % seed_index] += 1
    print("")
    print(f"{seed_index} probability : ")
    for index, quantity in enumerate(frequency_count):
        if quantity != 0:
            percentage = quantity * 100 / len(seed_history)
            print(f"{index} : {percentage}%")
            if percentage <= PERCENTAGE_THRESHOLD:
                return True
    return False


def main() -> None:
    initial_seed = randint(10 ** (SEED_SIZE - 1), 10**SEED_SIZE - 1)
    index = 0
    print_details(initial_seed, index)
    current_seed = calculate_next_seed(initial_seed)
    index += 1
    print_details(current_seed, index)
    seed_history = [initial_seed, current_seed]
    while True:
        index += 1
        current_seed = calculate_next_seed(current_seed)
        print_details(current_seed, index)
        if current_seed in seed_history:
            break
        else:
            seed_history.append(current_seed)
    for seed_index in range(1, len(seed_history)):
        if evaluate_probability(seed_index, seed_history):
            break


if __name__ == "__main__":
    main()
