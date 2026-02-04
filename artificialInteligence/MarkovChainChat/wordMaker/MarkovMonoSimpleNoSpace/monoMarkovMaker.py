from random import randint

WORDS_GENERATED = 1000
EMPTY_CHAR = "¨"

def generate_char(filename: str, previous_chars: list[str] | None = None) -> str:
    if previous_chars is None:
        previous_chars = []
    while len(previous_chars) != 2:
        previous_chars = [EMPTY_CHAR] + previous_chars
    with open(filename, "r", encoding="UTF-8") as file:
        line = file.readline()
        character_weights: dict[str, int] = {}
        while line:
            chars = [line[a] for a in range(0, 5, 2)]
            if previous_chars == chars[:2]:
                char = chars[2]
                frequency = int(line[6:-1])
                character_weights[char] = frequency
            line = file.readline()
        total = sum(list(character_weights.values()))
        chosen = randint(1, total)
        cumulative_frequency = 0
        for index, value in enumerate(character_weights.values()):
            cumulative_frequency += value
            if cumulative_frequency >= chosen:
                return list(character_weights.keys())[index]
        return ""


def generate_word(filename: str) -> str:
    generated_chars: list[str] = []
    char = generate_char(filename)
    while char != EMPTY_CHAR:
        generated_chars.append(char)
        char = generate_char(filename, generated_chars[-2:])
    return "".join(generated_chars)


def get_filename() -> str:
    is_filename_valid = True
    filename = "default"
    while is_filename_valid:
        print("type the file name (without .txt): ")
        filename = input()
        try:
            with open(f"{filename}.txt", "r", encoding="UTF-8") as _:
                pass
        except Exception as _:
            print("invalid name")
        is_filename_valid = False
    return filename


def main() -> None:
    filename = get_filename()
    for _ in range(WORDS_GENERATED):
        print(generate_word(f"{filename}/chain.txt"))


if __name__ == "__main__":
    main()
