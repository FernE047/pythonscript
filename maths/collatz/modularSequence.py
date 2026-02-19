def main() -> None:
    current_term = 0
    for seed in range(1, 10**4 + 1):
        current_term = 0
        for modulus in range(1, seed + 1):
            current_term += seed % modulus
        print(f"{seed}:{current_term}")


if __name__ == "__main__":
    main()