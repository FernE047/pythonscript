from estruturas import Collatz


def branching(x, y):
    collatz = Collatz(y).inversa()
    for a in range(10):
        proximosTermos = collatz.aplicaFuncao(x)
        print(proximosTermos)
        if len(proximosTermos) > 1:
            texto = str(x) + " - " + str(proximosTermos[-1])
            x = proximosTermos[-2]
        else:
            texto = str(x)
            x = proximosTermos[0]
        print(texto)


def makeBranch(z):
    return lambda x: branching(x, z)


for a in range(5):
    c = makeBranch(a)
    print(f"collatz {a}:\n")
    print(c(1), end="\n\n")
