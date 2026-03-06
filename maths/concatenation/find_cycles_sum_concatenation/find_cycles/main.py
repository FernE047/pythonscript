from pathlib import Path


ALLOW_USER_INPUT = False
SPACE_LIMIT = 10
INPUT_PATH = Path("no_cycles.txt")


def generate_cycle(current_term: str) -> list[str]:
    term_sequence = [current_term]
    while True:
        current_term = generate_next_term(current_term)
        if len(current_term) >= SPACE_LIMIT:
            current_term = current_term[:SPACE_LIMIT]
        term_sequence.append(current_term)
        if current_term in term_sequence[:-1]:
            break
    return term_sequence


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


def solve_for_term(term: str) -> None:
    result_terms = generate_cycle(term)
    sequence_size = len(result_terms) - 1
    print(f"\nThe term {term} reaches the end in {sequence_size} steps:")
    print(", ".join(result_terms))
    last_term_first_occurrence_index = result_terms.index(result_terms[-1])
    cycle_size = sequence_size - last_term_first_occurrence_index
    cycle_terms = result_terms[last_term_first_occurrence_index:]
    print(f"Degree {cycle_size} cycle found:")
    print(", ".join(cycle_terms))


def solve_with_file() -> None:
    with open(INPUT_PATH, "r", encoding="utf-8") as file:
        non_periodic_terms = [line.strip() for line in file]
    for term in non_periodic_terms:
        if not term.isdigit():
            print(f"Skipping invalid term: {term}")
            continue
        solve_for_term(term)


def solve_with_input() -> None:
    while True:
        print("What is the term to analyze?")
        term = input()
        if not term.isdigit():
            print("Please enter a valid term (only digits).")
            continue
        solve_for_term(term)


def main() -> None:
    if ALLOW_USER_INPUT:
        solve_with_input()
        return
    solve_with_file()


if __name__ == "__main__":
    main()
