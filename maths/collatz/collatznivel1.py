def even_procedure(seed: int, iteration_count: int, current_term: int) -> int:
    if not current_term % 2:
        print(str(int(current_term)))
        while (current_term % 2) == 0:
            current_term //= 2
            print(f"V\n{int(current_term)}")
        return current_term
    for _ in range(1, iteration_count):
        current_term = 4 * current_term + 1
    for _ in range(1, iteration_count + 1):
        print(str(int(current_term)), end="")
        if (current_term % 6) == 1:
            print(f" < {int((4 * current_term - 1) // 3)}", end="")
        elif (current_term % 6) == 5:
            print(f" < {int((2 * current_term - 1) // 3)}", end="")
        print("\nV")
        if current_term != seed:
            current_term = (current_term - 1) // 4
    return current_term


def main() -> None:
    seed = 1
    while seed != 0:
        iteration_count = 1
        while (seed % 8) == 5:
            seed = (seed - 1) // 4
            iteration_count += 1
        current_term = seed
        if iteration_count < 10:
            iteration_count = 10
        current_term = even_procedure(seed, iteration_count, current_term)
        if (seed % 4) == 3:
            print(str(int((3 * seed + 1) // 2)))
        elif (seed % 8) == 1:
            print(str(int((3 * seed + 1) // 4)))
        seed = int(input())


if __name__ == "__main__":
    main()
