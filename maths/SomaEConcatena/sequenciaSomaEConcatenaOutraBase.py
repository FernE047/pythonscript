ITERATION_LIMIT = 100
DEFAULT_BASE = 10


def get_user_int(prompt: str) -> int:
    while True:
        user_input = input(f"{prompt} : ")
        try:
            return int(user_input)
        except Exception as _:
            print("Invalid value, please try again")


def choose_from_options(prompt: str, options: list[str]) -> str:
    while True:
        for i, option in enumerate(options):
            print(f"{i} - {option}")
        user_choice = input(prompt)
        try:
            return options[int(user_choice)]
        except (ValueError, IndexError):
            user_choice = input("not valid, try again: ")


def validate_sequence_termination(
    current_term: list[int], termination_threshold: int, numerical_base: int
) -> tuple[bool, list[list[int]]]:
    sequence_terms = [current_term]
    while True:
        current_term = get_next_term(current_term, numerical_base)
        sequence_terms.append(current_term)
        if current_term in sequence_terms[:-1]:
            return (True, sequence_terms)
        if len(current_term) > termination_threshold:
            return (False, sequence_terms)


def get_next_term(current_term: list[int], numerical_base: int) -> list[int]:
    result: list[int] = []
    if len(current_term) <= 1:
        return current_term
    for digit_1, digit_2 in zip(current_term[:-1], current_term[1:]):
        sum_of_digits = digit_1 + digit_2
        base_representation = [sum_of_digits]
        if sum_of_digits >= numerical_base:
            base_representation = convert_to_base(sum_of_digits, numerical_base)
        result += base_representation
    if not (result):
        return current_term.copy()
    return result


def str_representation_of_term(term: list[int]) -> str:
    return "|".join([str(digit) for digit in term])


def str_representation_of_result(result: list[list[int]]) -> str:
    return ", ".join([str_representation_of_term(term) for term in result])


def display_message(test_number: int, termos: list[list[int]], base: int) -> None:
    print(f"\n{test_number} reaches an end in {len(termos) - 1} steps")
    print(str_representation_of_result(termos))
    print(" , ".join([str(convert_from_base(i, base)) for i in termos]))


def print_results(
    sequence_items: list[list[int]],
    test_number: int,
    output_mode: str,
    is_successful: bool,
    total_steps: int | str,
    numerical_base: int,
) -> int:
    quantia = 0
    if is_successful:
        if output_mode == "1":
            return quantia
        if output_mode == "3":
            if len(sequence_items) - 1 != total_steps:
                return quantia
        if output_mode == "4":
            if sequence_items[0] != sequence_items[-1]:
                return quantia
        display_message(test_number, sequence_items, numerical_base)
        quantia += 1
        return quantia
    if output_mode == "0":
        print(f"{test_number} exceeded the limit:")
        print(str_representation_of_result(sequence_items))
        quantia += 1
        return quantia
    if output_mode != "1":
        return quantia
    print(f"{test_number}")
    if total_steps == "1":
        print(str_representation_of_result(sequence_items))
    quantia += 1
    return quantia


def convert_to_base(decimal_value: int, base: int) -> list[int]:
    if base < 2:
        raise ValueError("Base must be >= 2")
    if decimal_value == 0:
        return [0]
    if decimal_value < 0:
        raise ValueError("Only non-negative integers supported")
    if decimal_value < base:
        return [decimal_value]
    conversion: list[int] = []
    current_value = decimal_value
    while current_value >= base:
        remainder = current_value % base
        conversion.append(remainder)
        current_value //= base
    conversion.append(current_value)
    conversion.reverse()
    return conversion


def convert_from_base(digits_list: list[int], base: int) -> int:
    total_value = 0
    for power_index, digit in enumerate(reversed(digits_list)):
        total_value += digit * base**power_index
    return total_value


def main() -> None:
    steps: int | str
    iteration_limit = ITERATION_LIMIT
    numerical_base = DEFAULT_BASE
    while True:
        result_count = 0
        user_choice = choose_from_options(
            "Choose an option: ",
            [
                "All",
                "Only Overflows",
                "No Overflows",
                "Only Steps",
                "Expected End",
                "Change Base",
                "Change Limits",
                "Exit",
            ],
        )
        if user_choice == "7":
            break
        if user_choice == "5":
            numerical_base = get_user_int("Enter the new base: ")
            continue
        if user_choice == "6":
            iteration_limit = get_user_int("Enter the new limit: ")
            continue
        steps = 0
        if user_choice == "3":
            steps = get_user_int("How many steps?")
        if user_choice == "1":
            steps = choose_from_options("Terms?", ["Without", "With"])
        search_limit = get_user_int("Search up to what?")
        for test_number in range(search_limit + 1):
            try:
                converted_term = convert_to_base(test_number, numerical_base)
                is_successful, result_terms = validate_sequence_termination(
                    converted_term, iteration_limit, numerical_base
                )
                result_count += print_results(
                    result_terms,
                    test_number,
                    user_choice,
                    is_successful,
                    steps,
                    numerical_base,
                )
                test_number += 1
            except Exception as _:
                print(f"Something went wrong with number:\n{test_number}")
        print(f"Total quantity {result_count}")


if __name__ == "__main__":
    main()
