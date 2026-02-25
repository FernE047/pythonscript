import math

LIMITE = -100
DEFAULT_BASE = 11


def convert_to_base(number: int) -> str:
    base_digits: list[str] = []
    highest_exponent = int(math.log(number, DEFAULT_BASE))
    for exponent in range(highest_exponent, LIMITE - 1, -1):
        base_term = DEFAULT_BASE**exponent
        base_factor = number // base_term
        number -= base_factor * base_term
        base_digits.append(str(base_factor))
        if exponent == 0:
            base_digits.append(",")
    base_number_string = "".join(base_digits)
    return base_number_string


def print_number_in_base(index: int, base_length: int = 0, formatted_width: int = 3):
    if base_length == 0:
        base_length = 10 - LIMITE
    converted_number = convert_to_base(index)
    print(
        f"{DEFAULT_BASE} : {index:0{formatted_width}} :  {converted_number:0>{base_length}}"
    )


def main() -> None:
    for index in range(1, 101):
        print_number_in_base(index)


if __name__ == "__main__":
    main()
