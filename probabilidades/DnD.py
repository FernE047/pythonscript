import random
from typing import Callable

# calculates chances of getting a certain result in a d20 dice roll, with or without advantage or disadvantage, and also the chances of getting a certain sequence of results in consecutive rolls.

SPECIAL_DICE_COUNT = 2
SIMULATION_COUNT_DEFAULT = 10**6


def roll_die(num_of_sides: int) -> int:
    return random.randint(1, num_of_sides)


def roll_dice(num_of_dice: int, num_of_sides: int) -> list[int]:
    results: list[int] = []
    for _ in range(num_of_dice):
        results.append(roll_die(num_of_sides))
    return results


def roll_normal(num_of_sides: int, num_of_dice: int = 1) -> int:
    results = roll_dice(num_of_dice, num_of_sides)
    return results[0]


def roll_with_advantage(
    num_of_sides: int, num_of_dice: int = SPECIAL_DICE_COUNT
) -> int:
    results = roll_dice(num_of_dice, num_of_sides)
    return max(results)


def roll_with_disadvantage(
    num_of_sides: int, num_of_dice: int = SPECIAL_DICE_COUNT
) -> int:
    results = roll_dice(num_of_dice, num_of_sides)
    return min(results)


def calculate_probabilities(
    roll_function: Callable[[int, int], int],
    num_of_sides: int,
    num_of_dice: int = SPECIAL_DICE_COUNT,
    simulation_count: int = SIMULATION_COUNT_DEFAULT,
):
    roll_results = [0 for _ in range(num_of_sides)]
    for _ in range(simulation_count):
        roll_results[roll_function(num_of_sides, num_of_dice) - 1] += 1
    for num, elemento in enumerate(roll_results):
        print(f"{num + 1} : {elemento * 100 / simulation_count}%")


def calculate_sequence_probability(
    num_of_sides: int,
    sequencia: list[int],
    simulation_count: int = SIMULATION_COUNT_DEFAULT,
) -> None:
    #this function actually calculates the chances of getting a certain sequence of results in consecutive rolls, not just the chances of getting a certain sequence in a single roll. The name is a bit misleading, but it is what it is.
    sequence_length = len(sequencia)
    dice_rolls = roll_dice(sequence_length - 1, num_of_sides)
    successful_matches_count = 0
    for _ in range(simulation_count):
        dice_rolls += roll_dice(1, num_of_sides)
        if dice_rolls == sequencia:
            successful_matches_count += 1
        dice_rolls.pop(0)
    print(f"{sequencia} : {successful_matches_count * 100 / simulation_count}%")


def main() -> None:
    print("desvantagem:\n")
    calculate_probabilities(roll_with_disadvantage, 20)
    print("\nvantagem:\n")
    calculate_probabilities(roll_with_advantage, 20)
    print("\nnormal:\n")
    calculate_probabilities(roll_normal, 20, 1)
    print("\nsequencia:\n")
    calculate_sequence_probability(20, [20, 20])
    calculate_sequence_probability(20, [20, 20, 20])
    calculate_sequence_probability(20, [20, 20, 20, 20])


if __name__ == "__main__":
    main()
