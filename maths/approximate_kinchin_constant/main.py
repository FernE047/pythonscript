KINCHIN_CONSTANT = 2.68545200106530644530971483548179569382038

def fraction_to_number(fraction: list[int]) -> float:
    fraction_length = len(fraction)
    current_fraction_value = float(fraction[-1])
    print(current_fraction_value)
    print()
    for depth in range(fraction_length - 1):
        term_index = fraction_length - depth - 2
        print(term_index)
        print(fraction[term_index])
        current_fraction_value = fraction[term_index] + 1 / current_fraction_value
        print(current_fraction_value)
        print()
    return current_fraction_value


def check_kinchin_proximity(fraction: list[int], is_less_than_kinchin: bool) -> bool:
    result = 1
    for fraction_term in fraction:
        result *= fraction_term
    if is_less_than_kinchin:
        if result < KINCHIN_CONSTANT:
            return True
    else:
        if result > KINCHIN_CONSTANT:
            return True
    return False


def main() -> None:
    continued_fraction: list[int] = []
    for depth in range(10):
        current_term = 0
        while True:
            current_term += 1
            continued_fraction.append(current_term)
            if check_kinchin_proximity(continued_fraction, depth % 2 == 0):
                continued_fraction.pop()
                break
            continued_fraction.pop()
        print(continued_fraction)


if __name__ == "__main__":
    main()
