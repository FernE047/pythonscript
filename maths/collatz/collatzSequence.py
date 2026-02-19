def collatz_0(number: int) -> int:
    if (number % 2) == 0:
        return number // 2
    else:
        return 3 * number + 1


def collatz_1(number: int) -> int:
    if (number % 2) == 0:
        return number // 2
    elif (number % 4) == 3:
        return (3 * number + 1) // 2
    elif (number % 8) == 1:
        return (3 * number + 1) // 4
    else:
        return (number - 1) // 4


def collatz_2(number: int) -> int:
    if number % 2 == 0:
        return number // 2
    elif number % 8 == 5:
        return (number - 1) // 4
    elif number % 8 == 7:
        return (3 * number + 1) // 2
    elif number % 16 == 3:
        return (number - 1) // 2
    elif number % 16 == 9:
        return (3 * number + 1) // 4
    elif number % 16 == 11:
        return (3 * number + 1) // 2
    elif number % 32 == 1:
        return (3 * number + 1) // 4
    elif number % 64 == 17:
        return (3 * number - 3) // 16
    elif number % 128 == 49:
        return (3 * number - 3) // 16
    elif number % 128 == 113:
        return (number - 17) // 32
    raise ValueError("Invalid number for collatz_2")


def collatz(number: int, level: int) -> int:
    functions = [collatz_0, collatz_1, collatz_2]
    steps = 0
    print(f"\ncollatz level {level}:\n")
    while number != 1:
        print(str(int(number)))
        number = functions[level](number)
        steps += 1
    print(str(int(number)))
    return int(steps)


def main() -> None:
    current_value = 1
    steps = [0 for _ in range(3)]
    while current_value != 0:
        steps = [collatz(current_value, i) for i in range(3)]
        print(f"steps : {steps[0]:4d}, {steps[1]:4d}, {steps[2]:4d}\n")
        current_value = int(input())


if __name__ == "__main__":
    main()
