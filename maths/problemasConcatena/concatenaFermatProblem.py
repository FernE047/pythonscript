# this script is to find numbers that can be expressed as the concatenation of two other numbers, where the first number is a perfect square and the second number is also a perfect square AND the number itself is also a perfect square. For example, 49 is 7 squared and can be expressed as 4 concatenated with 9, where 4 is a perfect square and 9 is also a perfect square.

def find_power_concatenation_pairs(base_value: int, power: int) -> list[tuple[int, int]]:
    results: list[tuple[int, int]] = []
    target_value = base_value**power
    for prefix_base in range(1, target_value):
        prefix_value = prefix_base**power
        prefix_text = str(prefix_value)
        for suffix_base in range(target_value):
            suffix_value = suffix_base**power
            suffix_text = str(suffix_value)
            candidate_text = prefix_text + suffix_text
            candidate_value = int(candidate_text)
            if candidate_value > target_value:
                break
            if candidate_value == target_value:
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