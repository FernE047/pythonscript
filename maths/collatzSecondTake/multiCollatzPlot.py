from matplotlib import pyplot as plt


def mod(lista, x):  # base,resto,x):
    base, resto = lista
    if x % base == resto:
        return True


def formula(lista, x):  # a,b,c,x):
    a, b, c = lista
    return (a * x + b) / c


def collatz(x):
    if x % 2:
        return 3 * x + 1
    else:
        return x / 2


def wazoo(x):
    regras = (
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
    for modArg, formArg in regras:
        if mod(modArg, x):
            return formula(formArg, x)


def mostra(lista):
    plt.plot(lista)
    plt.show()


def mostraP(lista):
    plt.plot(lista, "o")
    plt.show()


def collPassos(x):
    lista = []
    while x not in lista:
        lista.append(x)
        x = collatz(x)
    return len(lista)


def wazPassos(x):
    lista = []
    while x not in lista:
        lista.append(x)
        x = wazoo(x)
    return len(lista)


def collatzItera(n, x):
    for a in range(n):
        x = collatz(x)
    return x


def wazooItera(n, x):
    for a in range(n):
        x = wazoo(x)
    return x



def main() -> None:
    mostraP([wazPassos(a) for a in range(100)])
    mostraP([collPassos(a) for a in range(100)])
    # for n in range(1,100):
    #    mostraP([wazooItera(n,a) for a in range(100)])
    #    mostraP([collatzItera(n,a) for a in range(100)])


if __name__ == "__main__":
    main()