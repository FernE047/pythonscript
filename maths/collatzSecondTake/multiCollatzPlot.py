from matplotlib import pyplot as plt


COLLATZ_RULES = (
    ((2, 0), (1, 0, 2)),
    ((8, 5), (1, -1, 4)),
    ((8, 7), (3, 1, 2)),
    ((16, 3), (1, -1, 2)),
    ((16, 9), (3, 1, 4)),
    ((16, 11), (3, 1, 2)),
    ((32, 1), (3, 1, 4)),
    ((64, 17), (3, -3, 16)),
    ((128, 49), (3, -3, 16)),
    ((128, 113), (1, -17, 32)),
)

def mod(data: tuple[int, int], x: int) -> bool:  # base,resto,x):
    base, remainder = data
    return x % base == remainder


def formula(data: tuple[int, int, int], x: int) -> int:  # a,b,c,x:
    a, b, c = data
    return (a * x + b) // c


def collatz(x: int) -> int:
    if x % 2:
        return 3 * x + 1
    else:
        return x // 2


def collatz_2(x: int) -> int:
    for modulus_arguments, formula_arguments in COLLATZ_RULES:
        if mod(modulus_arguments, x):
            return formula(formula_arguments, x)
    return x


def plot_points(lista: list[int]) -> None:
    plt.plot(lista, "o")  # type: ignore
    plt.show()  # type: ignore


def count_collatz_steps(x: int) -> int:
    collatz_sequence: list[int] = []
    while x not in collatz_sequence:
        collatz_sequence.append(x)
        x = collatz(x)
    return len(collatz_sequence)


def count_collatz_2_steps(x: int) -> int:
    collatz_2_sequence: list[int] = []
    while x not in collatz_2_sequence:
        collatz_2_sequence.append(x)
        x = collatz_2(x)
    return len(collatz_2_sequence)


def iterate_collatz(n: int, x: int) -> int:
    for _ in range(n):
        x = collatz(x)
    return x


def iterate_collatz_2(n: int, x: int) -> int:
    for _ in range(n):
        x = collatz_2(x)
    return x


def main() -> None:
    plot_points([count_collatz_2_steps(a) for a in range(100)])
    plot_points([count_collatz_steps(a) for a in range(100)])
    for n in range(1, 100):
        plot_points([iterate_collatz_2(n, a) for a in range(100)])
        plot_points([iterate_collatz(n, a) for a in range(100)])


if __name__ == "__main__":
    main()
