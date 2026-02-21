import numpy as np
from typing import Callable, Literal, TypedDict

EquationData = Callable[[float], float]
IntervalData = tuple[float, float]

DEFAULT_INITIAL = -100
DEFAULT_END = 100
DEFAULT_POINT_COUNT = 201
DEFAULT_TERMINATION_THRESHOLD = 0.0001


class RangeConfig(TypedDict):
    start: float
    end: float
    total: int


def get_integer_input(
    message: str,
    default: int | Literal["."] | None = None,
    minimum: int | None = None,
    maximum: int | None = None,
) -> int | Literal["."]:
    while True:
        user_input = input(f"{message} : ")
        if user_input == "":
            if default is not None:
                return default
        try:
            value = int(user_input)
            if (minimum is not None) and (value < minimum):
                print(f"value must be greater than or equal to {minimum}")
                continue
            if (maximum is not None) and (value > maximum):
                print(f"value must be less than or equal to {maximum}")
                continue
            return value
        except Exception as _:
            print("invalid value, please try again")


def get_float_input(
    message: str, default_value: float | Literal["."]
) -> float | Literal["."]:
    while True:
        user_input = input(f"{message} (default: {default_value}) : ")
        if user_input == "":
            return default_value
        try:
            return float(user_input)
        except Exception as _:
            print("invalid value, please try again")


def get_coefficients() -> list[float]:
    n = 0
    coefficients: list[float] = []
    while True:
        value = get_float_input(f"enter the coefficient for x^{n}", ".")
        if value == ".":
            return coefficients
        else:
            coefficients.append(value)
            n += 1


def evaluate_polynomial(x: float, coefficient_list: list[float]) -> float:
    result = 0.0
    for index, coefficient in enumerate(reversed(coefficient_list)):
        power = len(coefficient_list) - 1 - index
        result += coefficient * x**power
    return result


def create_equation(coefficient_list: list[float]) -> EquationData:
    def equation(x: float) -> float:
        return evaluate_polynomial(x, coefficient_list)

    return equation


def check_sign(n: float) -> bool:
    return n > 0


def refine_intervals(
    equation: EquationData, search_range: RangeConfig
) -> list[IntervalData]:
    interval_list: list[IntervalData] = []
    search_space = (
        np.linspace(search_range["start"], search_range["end"], search_range["total"])
    ).tolist()
    for index in range(len(search_space) - 1):
        current_value = search_space[index]
        current_equation_value = equation(current_value)
        print(f"F({current_value}) : {current_equation_value}")
        if current_equation_value == 0:
            interval_list.append((current_equation_value, current_equation_value))
            continue
        next_value = search_space[index + 1]
        next_equation_value = equation(next_value)
        if check_sign(current_equation_value) != check_sign(next_equation_value):
            interval_list.append((current_value, next_value))
    return interval_list


def find_root(equation: EquationData, parada: float, intervalo: IntervalData) -> float:
    value_cache: dict[str, float] = {}
    iteration_count = 0
    lower_bound, upper_bound = intervalo
    while True:
        iteration_count += 1
        difference = upper_bound - lower_bound
        mid_value = lower_bound + difference / 2
        for x in (lower_bound, upper_bound, mid_value):
            if x not in value_cache.keys():
                value_cache[str(x)] = equation(x)
        if abs(difference) < parada:
            print(f"\niteration count : {iteration_count}")
            return mid_value
        if check_sign(lower_bound) == check_sign(mid_value):
            value_cache.pop(str(lower_bound))
            lower_bound = mid_value
        elif check_sign(upper_bound) == check_sign(mid_value):
            value_cache.pop(str(upper_bound))
            upper_bound = mid_value


def main() -> None:
    coefficients = get_coefficients()
    equation = create_equation(coefficients)
    initial_refinement_point = get_float_input(
        "enter the initial refinement point", "."
    )
    if initial_refinement_point == ".":
        initial_refinement_point = DEFAULT_INITIAL
    end_refinement_point = get_float_input("enter the end refinement point", ".")
    if end_refinement_point == ".":
        end_refinement_point = DEFAULT_END
    point_count = get_integer_input(
        f"enter how many points to take between {initial_refinement_point} and {end_refinement_point} for refinement",
        ".",
    )
    if point_count == ".":
        point_count = DEFAULT_POINT_COUNT
    refinement_range: RangeConfig = {
        "start": initial_refinement_point,
        "end": end_refinement_point,
        "total": point_count,
    }
    refined_intervals = refine_intervals(equation, refinement_range)
    print(refined_intervals)
    termination_threshold = get_float_input("enter the stopping criterion", ".")
    if termination_threshold == ".":
        termination_threshold = DEFAULT_TERMINATION_THRESHOLD
    for intervalo in refined_intervals:
        resultado = find_root(equation, termination_threshold, intervalo)
        print(f"result : {resultado}\n")


if __name__ == "__main__":
    main()
