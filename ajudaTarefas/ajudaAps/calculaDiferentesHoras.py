import random
from typing import Literal

YES_OR_NO_OPTIONS = ("y", "n", "0")
POSSIBLE_HOURS = (4, 3, 2, 1)

YesOrNoOptions = Literal["y", "n", "0"]


def define_limit(factor: int, total: int, add: int = 0) -> int:
    remaining = total - add
    if remaining < 0:
        return 0
    return remaining // factor + 1


def get_integer_input(message: str) -> int:
    while True:
        try:
            return int(input(f"{message}\n").strip())
        except ValueError:
            print("invalid input, try again")


def prompt_for_yes_no(message: str) -> YesOrNoOptions:
    choice = ""
    while choice not in YES_OR_NO_OPTIONS:
        print(f"{message} [y/n/0]")
        choice = input()
    return choice  # type: ignore


def print_list(factors_list: list[tuple[int, ...]]) -> None:
    for factors in factors_list:
        terms = [
            f"{hour}*{factor}"
            for hour, factor in zip(POSSIBLE_HOURS, factors)
            if factor > 0
        ]
        print("+".join(terms))


def distribute_hours_recursive(
    index: int,
    limits: list[int],
    factors: list[int],
    hours: int,
    is_sheets_mode: bool,
    sheets: int,
    lines_arranged: int,
) -> None | list[tuple[int, ...]]:
    if index == len(POSSIBLE_HOURS):
        if is_sheets_mode:
            factors_sum = sum(factors)
            if factors_sum <= sheets * 25 and factors_sum >= (sheets - 1) * 25:
                return [tuple(factors)]
        else:
            if sum(factors) == lines_arranged:
                return [tuple(factors)]
        return None
    limits[index] = define_limit(
        POSSIBLE_HOURS[index],
        hours,
        add=sum(
            hour * factor
            for hour, factor in zip(POSSIBLE_HOURS[:index], factors[:index])
        ),
    )
    combinations: list[tuple[int, ...]] = []
    for factor in range(limits[index]):
        factors[index] = factor
        result = distribute_hours_recursive(
            index + 1, limits, factors, hours, is_sheets_mode, sheets, lines_arranged
        )
        if result is not None:
            combinations.extend(result)
    return combinations


def distribute_hours_based_on_mode(hours: int, is_sheets_mode: bool) -> None:
    lines_arranged = 1
    sheets = 1
    if is_sheets_mode:
        sheets = get_integer_input("how many sheets")
    else:
        lines_arranged = get_integer_input("how many lines")
    if (sheets == 0) or (lines_arranged == 0):
        return
    limits = [0] * 4
    factors = [0] * 4
    factors_list = distribute_hours_recursive(
        0, limits, factors, hours, is_sheets_mode, sheets, lines_arranged
    )
    if factors_list is None:
        print("no combinations found")
        return
    while True:
        choice = prompt_for_yes_no("randomize results")
        if choice != "y":
            return
        group_length = get_integer_input(f"how many people are in your group [Max {len(factors_list)}]")
        if group_length > len(factors_list):
            print("the list is smaller than the group")
            print_list(factors_list)
            continue
        personal_lists = random.sample(factors_list, group_length)
        print_list(personal_lists)
        choice = prompt_for_yes_no("show personal results")
        if choice != "y":
            continue
        for personal_list in personal_lists:
            lines = 0
            resulting_list: list[int] = []
            for index, count in enumerate(personal_list):
                resulting_list.extend([POSSIBLE_HOURS[index] for _ in range(count)])
            random.shuffle(resulting_list)
            for element in resulting_list:
                print(element)
                lines += 1
                if lines == 25:
                    print("another sheet")
            print("continue")
            choice = prompt_for_yes_no("continue to the next")
            if choice == "0":
                break


def generate_hour_combinations(hours: int) -> None:
    while True:
        choice = prompt_for_yes_no("sheet mode?")
        if choice == "0":
            break
        sheet_mode = choice == "y"
        while True:
            distribute_hours_based_on_mode(hours, sheet_mode)


def main() -> None:
    while True:
        hours = get_integer_input("how many hours to calculate?")
        generate_hour_combinations(hours)


if __name__ == "__main__":
    main()
