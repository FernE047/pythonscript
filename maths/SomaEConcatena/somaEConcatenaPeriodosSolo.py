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
    if not result:
        result = [term]
    term = "".join(result)
    return term


def extract_cycles(term_a: str, term_b: str) -> str | None:
    cycle = ""
    for char_a, char_b in zip(term_a, term_b[: len(term_a)]):
        if char_a != char_b:
            return cycle
        cycle += char_a
    return None


def main() -> None:
    while True:
        print("limit")
        max_iterations = int(input())
        print("first term")
        initial_term = input()
        is_successful, sequence_terms = validate_sequence_termination(
            initial_term, max_iterations
        )
        if is_successful:
            print(f"term {initial_term} reaches an end in {len(sequence_terms) - 1}")
            print(",".join(sequence_terms))
        else:
            print(f"{initial_term} exceeded the limit:")
            print("\n".join(sequence_terms))
            print(
                f"cycle 1: {extract_cycles(sequence_terms[-1], sequence_terms[-3])}"
            )
            print(
                f"cycle 2: {extract_cycles(sequence_terms[-2], sequence_terms[-4])}"
            )


if __name__ == "__main__":
    main()
