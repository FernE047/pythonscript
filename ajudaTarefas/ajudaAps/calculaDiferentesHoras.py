import random
from typing import Literal


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
            pass


def prompt_for_yes_no(message: str) -> Literal["y", "n", "0"]:
    choice = ""
    while choice not in ("y", "n", "0"):
        print(f"{message} [y/n]")
        choice = input()
    if not isinstance(Literal["y", "n", "0"], type(choice)):
        raise TypeError("choice is not of the expected Literal type")
    return choice


def print_list(factors_list: list[tuple[int, int, int, int]]) -> None:
    for factors in factors_list:
        print(f"4*{factors[0]}+3*{factors[1]}+2*{factors[2]}+1*{factors[3]}")


def main() -> None:
    hours_a = 4
    hours_b = 3
    hours_c = 2
    hours_d = 1
    while True:
        print("how many hours to calculate?")
        hours = int(input())
        while True:
            choice = prompt_for_yes_no("sheet mode?")
            if choice == "0":
                break
            sheet_mode = choice == "y"
            sheets = 1
            lines_arranged = 1
            while True:
                factors_list: list[tuple[int, int, int, int]] = []
                if sheet_mode:
                    sheets = get_integer_input("how many sheets")
                else:
                    lines_arranged = get_integer_input("how many lines")
                if (sheets == 0) or (lines_arranged == 0):
                    break
                aLimit = define_limit(hours_a, hours)
                for a in range(aLimit):
                    bLimit = define_limit(hours_b, hours, add=hours_a * a)
                    for b in range(bLimit):
                        cLimit = define_limit(
                            hours_c, hours, add=hours_a * a + hours_b * b
                        )
                        for c in range(cLimit):
                            dLimit = define_limit(
                                hours_d,
                                hours,
                                add=hours_a * a + hours_b * b + hours_c * c,
                            )
                            for d in range(dLimit):
                                if (
                                    hours_a * a
                                    + hours_b * b
                                    + hours_c * c
                                    + hours_d * d
                                    == hours
                                ):
                                    if sheet_mode:
                                        if (a + b + c + d <= sheets * 25) and (
                                            a + b + c + d >= sheets * 25 - 25
                                        ):
                                            factors_list.append((a, b, c, d))
                                    else:
                                        if a + b + c + d == lines_arranged:
                                            factors_list.append((a, b, c, d))
                while True:
                    choice = prompt_for_yes_no("randomize results")
                    if choice != "y":
                        break
                    group_length = get_integer_input(
                        "how many people are in your group"
                    )
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
                        resulting_list = (
                            [hours_a for _ in range(personal_list[0])]
                            + [hours_b for _ in range(personal_list[1])]
                            + [hours_c for _ in range(personal_list[2])]
                            + [hours_d for _ in range(personal_list[3])]
                        )
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


if __name__ == "__main__":
    main()
