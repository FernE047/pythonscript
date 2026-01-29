from random import randint


def generate_char(file_name: str, index: int, previous_char: str = "") -> str:
    with open(f"{file_name}/{index:03d}.txt", encoding="utf-8") as file:
        line = file.readline()
        character_weights: dict[str, int] = {}
        while line:
            if index == 0:
                char = line[0]
                weight = int(line[2:-1])
            else:
                if previous_char == line[0]:
                    char = line[2]
                    weight = int(line[4:-1])
                else:
                    line = file.readline()
                    continue
            character_weights[char] = weight
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
    generated_word = ""
    char = generate_char(file_name, 0)
    while char != "¨":
        generated_word += char
        char = generate_char(file_name, len(generated_word), char)
    return generated_word


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
for index in range(1000):
    print(f"{index} : {generate_word(file_name)}")
