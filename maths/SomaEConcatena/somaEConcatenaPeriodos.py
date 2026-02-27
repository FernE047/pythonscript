IS_DEBUG = False

def print_debug(message: str) -> None:
    if IS_DEBUG:
        print(message)

def validate_sequence_termination(
    current_term: str, limit: int
) -> tuple[bool, list[str]]:
    terms_list: list[str] = [current_term]
    while True:
        current_term = generate_next_term(current_term)
        terms_list.append(current_term)
        if current_term in terms_list[:-1]:
            return (True, terms_list)
        if len(current_term) > limit:
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


def extract_cycles(term_a: str, term_b: str) -> str | None:
    cycle = ""
    for char_a, char_b in zip(term_a, term_b[:len(term_a)]):
        if char_a != char_b:
            return cycle
        cycle += char_a
    return None


def main() -> None:
    while True:
        print("Choose a mode:\n\n1 - all\n2 - no\n3 - yes")
        selection_mode = input()
        print("threshold")
        threshold = int(input())
        print("end value")
        end_value = int(input())
        for test_number in range(end_value + 1):
            current_number = str(test_number)
            is_successful, result_terms = validate_sequence_termination(current_number, threshold)
            if is_successful:
                continue
            cycle_1 = extract_cycles(result_terms[-1], result_terms[-3])
            cycle_2 = extract_cycles(result_terms[-2], result_terms[-4])
            if cycle_1 is None or cycle_2 is None:
                if selection_mode != "3":
                    print_debug(f"{current_number} doesn't have cycles:")
                    print(f"{current_number}")
                print_debug("\n".join(result_terms))
                continue
            if selection_mode == "2":
                continue
            print(f"\n{current_number} has cycles:")
            print(f"cycle 1: {cycle_1}")
            print(f"cycle 2: {cycle_2}")


if __name__ == "__main__":
    main()
