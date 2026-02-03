#! python3
import random


def main() -> None:
    uno = []
    cores = ["VERMELHO", "AZUL", "VERDE", "AMARELO"]
    cartas = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "SKIP", "REVERSE", "+2"]
    for a in cores:
        uno += [[a, "0"]]
        for b in range(2):
            for i in cartas:
                uno += [[a, i]]
    uno += 4 * [["WILD", ""], ["WILD +4", ""]]
    random.shuffle(uno)
    print(uno)


if __name__ == "__main__":
    main()