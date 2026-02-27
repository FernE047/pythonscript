ITERATION_LIMIT = 100


def validate_sequence_termination(
    number_test: int, term: str, limit: int
) -> tuple[bool, list[str]]:
    terms_list = [term]
    while True:
        term = generate_next_term(number_test, term)
        terms_list.append(term)
        if term in terms_list[:-1]:
            return (True, terms_list)
        if len(term) >= limit:
            return (False, terms_list)


def generate_next_term(number_test: int, term: str) -> str:
    result: list[str] = []
    if len(term) <= 1:
        return term
    digits = list(term)
    for digit_1, digit_2 in zip(digits[:-1], digits[1:]):
        sum_of_digits = int(digit_1) + int(digit_2)
        digit_sum = str(sum_of_digits)
        result.append(digit_sum)
    if not (result):
        return str(number_test)
    return "".join(result)


def print_result(test_number: int, results_list: list[str]) -> None:
    print(f"\n{test_number} succeeded in {len(results_list) - 1} steps")
    print(", ".join(results_list))


def main() -> None:
    iteration_limit = ITERATION_LIMIT
    while True:
        test_number = 0
        while True:
            try:
                current_term = str(test_number)
                _, result_terms = validate_sequence_termination(
                    test_number, current_term, iteration_limit
                )
                if str(test_number) == result_terms[-1]:
                    print_result(test_number, result_terms)
                test_number += 1
            except KeyboardInterrupt:
                print(f"execution stopped at {test_number}")
                return


if __name__ == "__main__":
    main()
