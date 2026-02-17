from estruturas import Collatz


def branching(x, y):
    collatz = Collatz(y).inversa()
    for a in range(10):
        proximosTermos = collatz.aplicaFuncao(x)
        print(proximosTermos)
        if len(proximosTermos) > 1:
            texto = f"{x} - {proximosTermos[-1]}"
            x = proximosTermos[-2]
        else:
            texto = str(x)
            x = proximosTermos[0]
        print(texto)


def makeBranch(z):
    return lambda x: branching(x, z)



def main() -> None:
    for a in range(5):
        c = makeBranch(a)
        print(f"collatz {a}:\n")
        print(f"{c(1)}\n")


if __name__ == "__main__":
    main()