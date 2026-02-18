def collatz(number_input: int) -> int:
    print(str(number_input))
    if (number_input != 1) and (number_input % 2):
        return collatz(3 * number_input + 1)
    elif number_input % 2 == 0:
        return collatz(int(number_input / 2))
    else:
        return 1


def main() -> None:
    while True:
        print("enter a number:")
        try:
            valor = int(input())
        except ValueError:
            print("Only numbers are allowed")
            continue
        if valor <= 0:
            print("Only Positive numbers are allowed")
            continue
        collatz(valor)
        break


if __name__ == "__main__":
    main()
