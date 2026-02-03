from numpy.random import shuffle


class Counters:
    def __init__(self) -> None:
        self.comparison_count = 0
        self.swap_count = 0

    def increment_comparison(self, count: int = 1) -> None:
        self.comparison_count += count

    def increment_swap(self) -> None:
        self.swap_count += 1

    def display(self) -> None:
        print(f"Comparisons: {self.comparison_count}, Swaps: {self.swap_count}")


def swap_elements(
    sort_list: list[int],
    index_a: int,
    index_b: int,
    counters: Counters,
    enable_logging: bool = True,
) -> None:
    counters.increment_swap()
    if enable_logging:
        print(
            f"swap {sort_list[index_a]} and {sort_list[index_b]} - positions {index_a} and {index_b}"
        )
    sort_list[index_a], sort_list[index_b] = sort_list[index_b], sort_list[index_a]


def insertion_sort(
    sort_list: list[int], counters: Counters, enable_logging: bool = True
) -> list[int]:
    def swap_this(element_a: int, element_b: int) -> None:
        swap_elements(
            sort_list, element_a, element_b, counters, enable_logging=enable_logging
        )

    current_position = 1
    while current_position < len(sort_list):
        counters.increment_comparison()
        current_index = current_position
        while (
            current_index > 0
            and sort_list[current_index - 1] > sort_list[current_index]
        ):
            counters.increment_comparison(3)
            swap_this(current_index, current_index - 1)
            current_index = current_index - 1
        counters.increment_comparison(3)
        current_position = current_position + 1
    counters.increment_comparison()
    return sort_list


def pythonic_selection_sort(
    sort_list: list[int], counters: Counters, enable_logging: bool = True
) -> None:
    def swap_this(element_a: int, element_b: int) -> None:
        swap_elements(
            sort_list, element_a, element_b, counters, enable_logging=enable_logging
        )

    for index in range(len(sort_list) - 1):
        smallest_index = sort_list.index(min(sort_list[index + 1 :]))
        if smallest_index != index:
            swap_this(index, smallest_index)


def selectionSort(
    sort_list: list[int], counters: Counters, enable_logging: bool = True
) -> None:
    def swap_this(element_a: int, element_b: int) -> None:
        swap_elements(
            sort_list, element_a, element_b, counters, enable_logging=enable_logging
        )

    total = len(sort_list)
    outer_index = 0
    while outer_index < (total - 1):
        counters.increment_comparison()
        min_index = outer_index
        inner_index = outer_index + 1
        while inner_index < total:
            counters.increment_comparison()
            if sort_list[inner_index] < sort_list[min_index]:
                counters.increment_comparison()
                min_index = inner_index
            inner_index += 1
        counters.increment_comparison()
        if min_index != outer_index:
            swap_this(outer_index, min_index)
        counters.increment_comparison()
        outer_index += 1
    counters.increment_comparison()



def main() -> None:
    counters = Counters()
    tamanhoLista = 1000
    imprimeListas = True
    lista = [a for a in range(tamanhoLista)]
    shuffle(lista)
    if imprimeListas:
        print(lista, end="\n\n")
    insertion_sort(lista, counters, enable_logging=False)
    if imprimeListas:
        print(f"\n{lista}")
    counters.display()


if __name__ == "__main__":
    main()