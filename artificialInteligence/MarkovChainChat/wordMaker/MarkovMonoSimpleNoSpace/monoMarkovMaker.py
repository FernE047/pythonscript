from random import randint


def generate_char(file_name: str, previous_chars: list[str] | None = None) -> str:
    if previous_chars is None:
        previous_chars = []
    while len(previous_chars) != 2:
        previous_chars = ["¨"] + previous_chars
    with open(file_name, "r", encoding="UTF-8") as file:
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


def generate_word(file_name: str) -> str:
    generated_chars: list[str] = []
    char = generate_char(file_name)
    while char != "¨":
        generated_chars.append(char)
        char = generate_char(file_name, generated_chars[-2:])
    return "".join(generated_chars)


def get_file_name() -> str:
    is_file_name_valid = True
    file_name = "default"
    while is_file_name_valid:
        print("type the file name (without .txt): ")
        file_name = input()
        try:
            with open(f"{file_name}.txt", "r", encoding="UTF-8") as _:
                pass
        except Exception as _:
            print("invalid name")
        is_file_name_valid = False
    return file_name


file_name = get_file_name()
for a in range(1000):
    print(generate_word(f"{file_name}/chain.txt"))
