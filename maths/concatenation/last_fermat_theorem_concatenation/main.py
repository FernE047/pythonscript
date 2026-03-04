# this script is to find numbers that can be expressed as the concatenation of two other numbers, where the first number is a perfect square and the second number is also a perfect square AND the number itself is also a perfect square. For example, 49 is 7 squared and can be expressed as 4 concatenated with 9, where 4 is a perfect square and 9 is also a perfect square.


def find_power_concatenation_pairs(
    base_value: int, power: int
) -> list[tuple[int, int]]:
    results: list[tuple[int, int]] = []
    target_value = base_value**power
    target_text = str(target_value)
    if len(target_text) == 1:
        return results
    for cursor in range(1, len(target_text)):
        prefix_text = target_text[:cursor]
        if prefix_text[0] == "0":
            continue
        prefix_value = int(prefix_text)
        inverse_power = 1 / power
        prefix_base = int(prefix_value**inverse_power)
        if prefix_base**power != prefix_value:
            continue
        suffix_text = target_text[cursor:]
        if suffix_text[0] == "0":
            continue
        suffix_value = int(suffix_text)
        suffix_base = int(suffix_value**inverse_power)
        if suffix_base**power != suffix_value:
            continue
        results.append((prefix_base, suffix_base))
    return results


def calculate_and_print_results(iteration_limit: int, power: int) -> None:
    for iteration in range(iteration_limit):
        results = find_power_concatenation_pairs(iteration, power)
        if not results:
            continue
        print(f"{iteration} : {iteration**power}")
        for element_0, element_1 in results:
            print(f"{element_0},{element_1}")
        print("")


def main() -> None:
    calculate_and_print_results(10000, 2)


if __name__ == "__main__":
    main()