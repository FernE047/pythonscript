from typing import Callable

from estruturas import load_collatz


def branching(current_value: int, collatz_level: int) -> None:
    collatz = load_collatz(collatz_level).get_opposite()
    for _ in range(10):
        next_terms = collatz.apply(current_value)
        print(next_terms)
        if len(next_terms) > 1:
            formatted_output = f"{current_value} - {next_terms[-1]}"
            current_value = next_terms[-2]
        else:
            formatted_output = str(current_value)
            current_value = next_terms[0]
        print(formatted_output)


def makeBranch(collatz_level: int) -> Callable[[int], None]:
    def branch(value: int) -> None:
        return branching(value, collatz_level)
    return branch


def main() -> None:
    #TODO we only calculated collatz functions up to 6, it's a very slow process. I will calculate more in the future, but for now we can only branch up to collatz 5.
    for collatz_level in range(5):
        collatz = makeBranch(collatz_level)
        print(f"collatz {collatz_level}:\n")
        collatz(1)
        print()


if __name__ == "__main__":
    main()
