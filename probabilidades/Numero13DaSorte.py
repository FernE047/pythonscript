import random

MINIMUM = 10
MAXIMUM = 200
TOTAL_SIMULATIONS = 1000000


def main() -> None:
    valores: dict[int, int] = {}
    for index in range(1, MAXIMUM + 1):
        valores[index] = 0
    for _ in range(TOTAL_SIMULATIONS):
        numeros = random.randint(MINIMUM, MAXIMUM)
        sorteado = random.randint(1, numeros)
        valores[sorteado] += 1
    for numero in valores:
        if valores[numero] != 0:
            print(f"{numero:03d} : {valores[numero] * 100 / TOTAL_SIMULATIONS}%")


if __name__ == "__main__":
    main()
