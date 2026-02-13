def main() -> None:
    termo = 0
    for semente in range(1, 10**4 + 1):
        termoantigo = termo
        termo = 0
        for modular in range(1, semente + 1):
            termo += semente % modular
        print(f"{semente}:{termo}")


if __name__ == "__main__":
    main()