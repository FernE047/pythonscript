import math
from time import time
import gc
from datetime import timedelta

MAX_ITERATIONS = 1000


def create_permutation_list(initial_list: list[int], index: int) -> list[int]:
    list_length = len(initial_list)
    if list_length <= 1:
        return initial_list
    divisor = math.factorial(list_length - 1)
    selected_element = initial_list.pop(index // divisor)
    final_list = [selected_element]
    final_list.extend(create_permutation_list(initial_list, index % divisor))
    return final_list


def analyze_categories(num_permutations: int) -> dict[str, int]:
    categories: dict[str, int] = {}
    iteration_count = 0
    start_time = time()
    lista = [permutation_index for permutation_index in range(num_permutations)]
    for index in range(math.factorial(num_permutations)):
        category = determine_category(create_permutation_list(lista.copy(), index))
        if category in categories:
            categories[category] += 1
        else:
            categories[category] = 1
        if iteration_count < MAX_ITERATIONS:
            iteration_count += 1
            continue
        end_time = time()
        elapsed_time = end_time - start_time
        print(f"{MAX_ITERATIONS} executions took : ")
        elapsed_time_str = str(timedelta(seconds=elapsed_time))
        print(f"Elapsed time: {elapsed_time_str}")
        print("Estimated Total Execution Time : ")
        prediction = elapsed_time * (math.factorial(num_permutations) / MAX_ITERATIONS)
        prediction_str = str(timedelta(seconds=prediction))
        print(f"Elapsed time: {prediction_str}")
        iteration_count = MAX_ITERATIONS + 1
        break
    return categories


def determine_category(permutation_list: list[int]) -> str:
    visited_status = [False for _ in permutation_list]
    cycle_sizes = [0 for _ in permutation_list]
    while False in visited_status:
        current_index = visited_status.index(False)
        current_element = permutation_list[current_index]
        cycle_length = 0
        visited_status[current_index] = True
        while current_element != current_index:
            visited_status[current_element] = True
            current_element = permutation_list[current_element]
            cycle_length += 1
        cycle_sizes[cycle_length] += 1
    category_list: list[str] = []
    for index in range(1, len(permutation_list)):
        if cycle_sizes[index] != 0:
            category_list += [str(index + 1) for _ in range(cycle_sizes[index])]
    return " ".join(category_list)


def main() -> None:
    start_time = time()
    try:
        category_analysis = analyze_categories(12)
        for category in category_analysis:
            print(f"{category:8s} : {category_analysis[category]}")
        print("Total Execution Time : ")
        end_time = time()
        elapsed_time = end_time - start_time
        elapsed_time_str = str(timedelta(seconds=elapsed_time))
        print(f"Elapsed time: {elapsed_time_str}")
    except KeyboardInterrupt:
        print(gc.collect())


if __name__ == "__main__":
    main()
