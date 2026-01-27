import random
from typing import Literal


def define_limit(factor: int, total: int, add: int = 0) -> int:
    num = 0
    while factor * num + add <= total:
        num += 1
    limit = num
    return limit


def get_integer_input(message: str) -> int:
    print(message)
    number_text = input()
    is_converted = False
    number = 0
    while not (is_converted):
        try:
            number = int(number_text)
            is_converted = True
        except Exception as _:
            print(message)
            number_text = input()
    return number


def prompt_for_yes_no(message: str) -> Literal["y", "n", "0"]:
    choice = ""
    while choice not in ("y", "n", "0"):
        print(message + " [y/n]")
        choice = input()
    return choice


def print_list(factors_list: list[tuple[int, int, int, int]]) -> None:
    for factors in factors_list:
        print(f"4*{factors[0]}+3*{factors[1]}+2*{factors[2]}+1*{factors[3]}")

HOURS_A = 4
HOURS_B = 3
HOURS_C = 2
HOURS_D = 1
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
            aLimit = define_limit(HOURS_A, hours)
            for a in range(aLimit):
                bLimit = define_limit(HOURS_B, hours, add=HOURS_A * a)
                for b in range(bLimit):
                    cLimit = define_limit(
                        HOURS_C, hours, add=HOURS_A * a + HOURS_B * b
                    )
                    for c in range(cLimit):
                        dLimit = define_limit(
                            HOURS_D, hours, add=HOURS_A * a + HOURS_B * b + HOURS_C * c
                        )
                        for d in range(dLimit):
                            if (
                                HOURS_A * a + HOURS_B * b + HOURS_C * c + HOURS_D * d
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
                group_length = get_integer_input("how many people are in your group")
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
                        [HOURS_A for _ in range(personal_list[0])]
                        + [HOURS_B for _ in range(personal_list[1])]
                        + [HOURS_C for _ in range(personal_list[2])]
                        + [HOURS_D for _ in range(personal_list[3])]
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