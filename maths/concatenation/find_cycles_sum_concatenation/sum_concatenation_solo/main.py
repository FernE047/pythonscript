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


def main() -> None:
    while True:
        print("limit")
        limit = int(input())
        print("first term")
        term = input()
        success, terms = validate_sequence_termination(term, limit)
        if success:
            print(f"term {term} reaches an end in {len(terms) - 1}")
            print(",".join(terms))
        else:
            print(f"{term} exceeded the limit:")
            print("\n".join(terms))


if __name__ == "__main__":
    main()
