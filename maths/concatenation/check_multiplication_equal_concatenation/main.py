LIMITE = 10000

def main() -> None:
    for factor_1 in range(1, LIMITE + 1):
        for factor_2 in range(factor_1, LIMITE + 1):
            product = factor_1 * factor_2
            concatenated_factors = int(str(factor_1) + str(factor_2))
            if product == concatenated_factors:
                print(product)
                print(concatenated_factors)
                print(f"{factor_1} | {factor_2}")
                print("")


if __name__ == "__main__":
    main()
