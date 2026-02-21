from typing import Callable

from estruturas import load_collatz


def branching(x: int, y: int) -> None:
    collatz = load_collatz(y).get_opposite()
    for _ in range(10):
        proximosTermos = collatz.apply(x)
        print(proximosTermos)
        if len(proximosTermos) > 1:
            texto = f"{x} - {proximosTermos[-1]}"
            x = proximosTermos[-2]
        else:
            texto = str(x)
            x = proximosTermos[0]
        print(texto)


def makeBranch(z: int) -> Callable[[int], None]:
    def branch(x: int) -> None:
        return branching(x, z)
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
