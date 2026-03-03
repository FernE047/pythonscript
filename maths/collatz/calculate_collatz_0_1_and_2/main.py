def collat_0(number: int) -> int:
    if number % 2 == 0:
        return number // 2
    return 3 * number + 1


def collatz_1(number: int) -> int:
    if number % 2 == 0:
        return number // 2
    if number % 4 == 3:
        return (3 * number + 1) // 2
    if number % 8 == 1:
        return (3 * number + 1) // 2
    return (number - 1) // 4


def collatz_2(number: int) -> int:
    if number % 2 == 0:
        return number // 2
    if number % 8 == 5:
        return (number - 1) // 4
    if number % 8 == 7:
        return (3 * number + 1) // 2
    if number % 16 == 3:
        return (number - 1) // 2
    if number % 16 == 9:
        return (3 * number + 1) // 4
    if number % 16 == 11:
        return (3 * number + 1) // 2
    if number % 32 == 1:
        return (3 * number + 1) // 4
    if number % 64 == 17:
        return (3 * number - 3) // 16
    if number % 128 == 49:
        return (3 * number - 3) // 16
    if number % 128 == 113:
        return (number - 17) // 32
    raise ValueError("Invalid number for collatz_2")


def collatz(number: int, level: int) -> int:
    functions = [collat_0, collatz_1, collatz_2]
    steps = 0
    while number != 1:
        number = functions[level](number)
        steps += 1
    return steps


def main() -> None:
    limite = 0
    starting_value = 1
    while limite == 0:
        print("enter a starting value and a limit (0 to exit):")
        starting_value = int(input())
        if starting_value <= 0:
            continue
        limite = int(input()) + 1
    if starting_value > limite - 1:  # inverte valores
        limite += starting_value
        print(str(limite))
        starting_value = limite - starting_value - 1
        print(str(starting_value))
        limite -= starting_value
        print(str(limite))
    for value in range(starting_value, limite):
        steps = [collatz(value, level) for level in range(3)]
        print(f"{value:5d}:{steps[0]:4d},{steps[1]:4d},{steps[2]:4d}")


if __name__ == "__main__":
    main()
