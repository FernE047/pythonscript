def collatz_2(x: int) -> int:
    if x % 2 == 0:
        return x // 2
    elif x % 8 == 5:
        return (x - 1) // 4
    elif x % 8 == 7:
        return (3 * x + 1) // 2
    elif x % 16 == 3:
        return (x - 1) // 2
    elif x % 16 == 9:
        return (3 * x + 1) // 4
    elif x % 16 == 11:
        return (3 * x + 1) // 2
    elif x % 32 == 1:
        return (3 * x + 1) // 4
    elif x % 64 == 17:
        return (3 * x - 3) // 16
    elif x % 128 == 49:
        return (3 * x - 3) // 16
    elif x % 128 == 113:
        return (x - 17) // 32
    return int(x)


def main() -> None:
    current_value = int(input())
    steps = 0
    while current_value != 1:
        current_value = collatz_2(current_value)
        print(f"{current_value}")
        steps += 1
    print(f"steps : {steps}")


if __name__ == "__main__":
    main()