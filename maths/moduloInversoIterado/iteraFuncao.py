from typing import Callable

MAX_ITERATIONS = 24


def get_user_int(message: str) -> int:
    while True:
        entrada = input(f"{message} : ")
        try:
            valor = int(entrada)
            return valor
        except Exception as _:
            print("valor inválido, tente novamente")


def math_expression(a: int, b: int, n: int) -> int:
    if (b == 0) and (n == 0):
        return 1
    return a * n + b


def get_prime_factors(number_to_factor: int) -> list[int]:
    current_divisor = 2
    factors: list[int] = []
    while current_divisor * current_divisor <= number_to_factor:
        if number_to_factor % current_divisor:
            current_divisor += 1
        else:
            number_to_factor //= current_divisor
            factors.append(current_divisor)
    if number_to_factor > 1:
        factors.append(number_to_factor)
    return factors


def get_prime_factors_text(factor_count: int) -> str:
    if factor_count <= 1:
        return str(factor_count)
    prime_factor_list = get_prime_factors(factor_count)
    previous_factor = prime_factor_list[0]
    factor_count = 0
    retorno = f"{previous_factor}^"
    for factor in prime_factor_list:
        if factor == previous_factor:
            factor_count += 1
        else:
            retorno += f"{factor_count}*{factor}^"
            factor_count = 1
        previous_factor = factor
    retorno += str(factor_count)
    return retorno


def iterate_function(
    transform_function: Callable[[int], int], start_value: int = 0
) -> None:
    current_value = transform_function(start_value)
    index = 0
    for index in range(start_value, MAX_ITERATIONS):
        print(f"{index} : {current_value} : {get_prime_factors_text(current_value)}")
        current_value = transform_function(current_value)
    print(f"{index + 1} : {current_value} : {get_prime_factors_text(current_value)}")


def main() -> None:
    while True:
        base = get_user_int("\nenter the base")
        if base == 0:
            raise Exception("base cannot be 0")
        remainder = get_user_int("enter the remainder")
        start = get_user_int("enter the start")

        def current_expression(x: int) -> int:
            return math_expression(base, remainder, x)

        if remainder == 0:
            iterate_function(current_expression, start_value=start)
        else:
            iterate_function(current_expression, start_value=start)


if __name__ == "__main__":
    main()
