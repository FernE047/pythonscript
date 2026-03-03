# first lambda function I made in python, then I became addicted to them. now I prefer def statements tho


from typing import Callable


def get_integer_input(
    message: str,
    minimum: int | None = None,
    maximum: int | None = None,
) -> int | None:
    while True:
        user_input = input(f"{message} : ")
        if user_input == "exit":
            return None
        try:
            value = int(user_input)
            if (minimum is not None) and (value < minimum):
                print(f"value must be at least {minimum}")
                continue
            if (maximum is not None) and (value > maximum):
                print(f"value must be at most {maximum}")
                continue
            return value
        except Exception as _:
            print("invalid value, please try again")


def compute_polynomial_value(coefficients: list[int], x: int) -> int | float:
    degree_of_polynomial = len(coefficients)
    polynomial_value = 0
    for term_index, coefficient in enumerate(coefficients):
        polynomial_value += coefficient * x ** (degree_of_polynomial - term_index - 1)
    return polynomial_value


def generate_equation(coefficients: list[int]) -> Callable[[int], int | float]:
    return lambda x: compute_polynomial_value(coefficients, x)


def display_value_intervals(coefficients: list[int], interval_size: int) -> None:
    equation = generate_equation(coefficients)
    half_range = int(interval_size / 2)
    print(f"interval between -{half_range} and {half_range}")
    for value in range(-half_range, half_range):
        print(f"{value} : {equation(value)}")


def main() -> None:
    while True:
        max_power = get_integer_input("enter the maximum power of the polynomial")
        if max_power is None:
            break
        coefficients: list[int] = []
        for a in range(max_power + 1):
            new_coefficient = get_integer_input(
                f"enter the coefficient of x raised to {max_power - a}"
            )
            if new_coefficient is None:
                break
            coefficients = [new_coefficient] + coefficients
        print(coefficients)
        interval_size = get_integer_input("enter the size of the interval to evaluate")
        if interval_size is None:
            break
        display_value_intervals(coefficients, interval_size)


if __name__ == "__main__":
    main()
