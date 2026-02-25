def testaBase(base: int, check_equal_values: bool = False) -> None:
    for digit_1 in range(1, base):
        for digit_2 in range(base):
            for digit_3 in range(base):
                primeiro = (digit_1 * base + digit_2) * digit_3
                segundo = digit_1 * int(digit_2 * base + digit_3)
                if primeiro != segundo:
                    continue
                if primeiro == 0:
                    continue
                if check_equal_values:
                    if (digit_1 == digit_2) and (digit_2 == digit_3):
                        continue
                print(f"{digit_1}|{digit_2}|{digit_3}")
                print(primeiro)
                print("")


def main() -> None:
    for base in range(2, 21):
        print(f"base {base} :\n")
        testaBase(base, check_equal_values=False)


if __name__ == "__main__":
    main()
