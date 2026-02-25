from typing import Any, Literal, overload

IS_DEBUG = False
ITERATION_LIMIT = 1000


def print_debug(*args: Any, **kwargs: Any) -> None:
    if IS_DEBUG:
        print(*args, **kwargs)


@overload
def get_user_integer(message: str, can_exit: Literal[False] = False) -> int: ...


@overload
def get_user_integer(message: str, can_exit: Literal[True]) -> int | Literal[""]: ...


def get_user_integer(message: str, can_exit: bool = False) -> int | Literal[""]:
    while True:
        user_input = input(f"{message} : ")
        if can_exit and user_input == "":
            return ""
        try:
            value = int(user_input)
            return value
        except Exception as _:
            print("invalid value, please try again")


def get_user_integers() -> list[int]:
    user_input_integers: list[int] = []
    print("enter the integers of the continued fraction one by one")
    print("when finished, enter an empty line")
    while True:
        value = get_user_integer("integer", can_exit=True)
        if value == "":
            break
        user_input_integers.append(value)
    return user_input_integers


def choose_from_options(prompt: str, options: list[str]) -> int:
    while True:
        for i, option in enumerate(options):
            print(f"{i} - {option}")
        user_choice = input(prompt)
        try:
            return int(user_choice)
        except (ValueError, IndexError):
            user_choice = input("not valid, try again: ")


def get_user_float(mensagem: str) -> float:
    while True:
        entrada = input(mensagem)
        try:
            return float(entrada)
        except Exception as _:
            print("valor inválido, tente novamente")


def fraction_to_number(fraction: list[int]) -> float:
    fraction_length = len(fraction)
    current_value = fraction[-1] * 1.0
    print_debug(f"current value : {current_value}")
    for n in range(fraction_length - 1):
        current_index = fraction_length - n - 2
        current_value = fraction[current_index] + 1 / current_value
        print_debug(f"current index : {current_index}")
        print_debug(f"current fraction value : {fraction[current_index]}")
        print_debug(f"current value : {current_value}\n")
    return current_value


def decimal_to_fraction(float_value: float) -> list[int]:
    iteration_count = 0
    fraction: list[int] = []
    while True:
        iteration_count += 1
        print_debug()
        integer_part = int(float_value)
        print_debug(f"integer_part : {integer_part}")
        fractional_part = float_value - integer_part
        print_debug(f"fractional_part : {fractional_part}")
        fraction.append(integer_part)
        if fractional_part == 0:
            return fraction
        else:
            float_value = 1 / fractional_part
            print_debug(f"inverted : {float_value}")
        if iteration_count == ITERATION_LIMIT:
            fraction.append(int(fractional_part))
            print_debug("iteration limit reached, stopping")
            return fraction


def fraction_to_continued(numerator: int, denominator: int) -> list[int]:
    iteration_count = 0
    fraction: list[int] = []
    while True:
        iteration_count += 1
        print_debug()
        integer_part = int(numerator / denominator)
        print_debug(f"integer_part : {integer_part}")
        previous_numerator = numerator
        numerator = denominator
        print_debug(f"numerator : {numerator}")
        denominator = previous_numerator - integer_part * denominator
        print_debug(f"denominator : {denominator}")
        fraction.append(integer_part)
        if denominator == 0:
            return fraction
        if numerator == 1:
            fraction.append(denominator)
            return fraction
        if iteration_count == ITERATION_LIMIT:
            fraction.append(numerator // denominator)
            print_debug("iteration limit reached, stopping")
            return fraction


def main() -> None:
    while True:
        user_input = choose_from_options(
            "conversion type",
            ["continued fraction to number", "number to continued fraction"],
        )
        if user_input == 0:
            fraction = get_user_integers()
            float_value = fraction_to_number(fraction)
            print(float_value)
            continue
        user_input = choose_from_options(
            "number type", ["decimal", "fraction", "square roots"]
        )
        if user_input == 0:
            valor = get_user_float("enter a decimal value")
            resultado = decimal_to_fraction(valor)
            print(resultado)
            continue
        if user_input == 1:
            numerator = get_user_integer("enter the numerator")
            denominator = get_user_integer("enter the denominator")
            resultado = fraction_to_continued(numerator, denominator)
            print(resultado)
            continue
        user_input = choose_from_options("root mode:", ["simple", "complex"]) + 2
        root_value = get_user_float("enter the number inside the root")
        root_value = root_value * 1.0  # just to make sure it's a float
        if user_input == 3:
            numerator = get_user_integer(
                "enter the number that will be added to the root"
            )
            denominator = get_user_integer("enter the denominator")
        raise NotImplementedError("root modes are not implemented yet")
        # TODO: implementar a função de raiz complexa


if __name__ == "__main__":
    main()
