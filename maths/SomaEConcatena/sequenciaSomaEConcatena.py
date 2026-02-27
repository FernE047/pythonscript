ITERATION_LIMIT = 100


def validate_sequence_termination(current_term: str) -> tuple[bool, list[str]]:
    terms_list: list[str] = [current_term]
    while True:
        current_term = generate_next_term(current_term)
        terms_list.append(current_term)
        if current_term in terms_list[:-1]:
            return (True, terms_list)
        if len(current_term) > ITERATION_LIMIT:
            return (False, terms_list)


def generate_next_term(term: str) -> str:
    result: list[str] = []
    if len(term) <= 1:
        return term
    digits = list(term)
    for digit_1, digit_2 in zip(digits[:-1], digits[1:]):
        sum_digits = int(digit_1) + int(digit_2)
        double_digit = str(sum_digits)
        result.append(double_digit)
    if not (result):
        result = [term]
    term = "".join(result)
    return term


def display_message(test_number: int, terms_list: list[str]) -> None:
    print(f"\n{test_number} reaches an end in {len(terms_list) - 1} steps")
    print(",".join(terms_list))


def print_results(terms_list: list[str], test_number: int, mode: str, is_successful: bool, steps: int|str) -> int:
    result_count = 0
    if is_successful:
        if mode == "1":
            return result_count
        if mode == "3":
            if len(terms_list) - 1 != steps:
                return result_count
        if mode == "4":
            if str(test_number) != terms_list[-1]:
                return result_count
        display_message(test_number, terms_list)
        result_count += 1
        return result_count
    if mode == "0":
        print(f"{test_number} exceeded the limit:")
        print(",".join(terms_list))
        result_count += 1
    if mode == "1":
        print(f"{test_number}")
        if steps == "1":
            print(",".join(terms_list))
        result_count += 1
    return result_count


def main() -> None:
    steps: int|str
    result_count = 0
    while True:
        print(
            "Choose an option:\n0 - all\n1 - only overflows\n2 - no overflows\n3 - only steps\n4 - expected final\n5 - exit"
        )
        user_input = input()
        if user_input == "5":
            break
        steps = 0
        if user_input == "3":
            print("How many steps?")
            steps = int(input())
        if user_input == "1":
            print("With terms or without? [1/0]")
            steps = input()
        print("Search up to what number?")
        search_limit = int(input())
        for current_number in range(search_limit + 1):
            try:
                current_term = str(current_number)
                is_successful, terms_list = validate_sequence_termination(current_term)
                result_count += print_results(
                    terms_list, current_number, user_input, is_successful, steps
                )
                current_number += 1
            except Exception:
                print(f"{current_number}")
        print(f"Total quantity : {result_count}")


if __name__ == "__main__":
    main()
