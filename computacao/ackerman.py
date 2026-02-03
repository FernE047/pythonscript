def ackerman(m: int, n: int) -> int:
    global level
    level += 1
    print(f"ackerman({m},{n})\tlevel={level}")
    if m <= 0:
        return n + 1
    if (m > 0) and (n <= 0):
        result_value = ackerman(m - 1, 1)
        level -= 1
        return result_value
    if (m > 0) and (n > 0):
        result_value = ackerman(m - 1, ackerman(m, n - 1))
        level -= 2
        return result_value
    print("error")
    return n - 1


def main() -> None:
    level = 0
    print(ackerman(3, 10))


if __name__ == "__main__":
    main()
