from random import randint
from pathlib import Path

WORDS_GENERATED = 1000
EMPTY_CHAR = "¨"


def generate_char(filename: Path, index: int, previous_char: str = "") -> str:
    with open(filename / f"{index:03d}.txt", encoding="utf-8") as file:
        lines = file.readlines()
    character_weights: dict[str, int] = {}
    for line in lines:
        if not line.strip():
            continue
        if index == 0:
            char = line[0]
            weight = int(line[2:-1])
        else:
            if previous_char == line[0]:
                char = line[2]
                weight = int(line[4:-1])
            else:
                continue
        character_weights[char] = weight
    total = sum(list(character_weights.values()))
    chosen = randint(1, total)
    cumulative_frequency = 0
    for index, value in enumerate(character_weights.values()):
        cumulative_frequency += value
        if cumulative_frequency >= chosen:
            return list(character_weights.keys())[index]
    return ""


def generate_word(filename: Path) -> str:
    generated_word = ""
    char = generate_char(filename, 0)
    while char != EMPTY_CHAR:
        generated_word += char
        char = generate_char(filename, len(generated_word), char)
    return generated_word


def get_filename() -> Path:
    is_filename_valid = True
    filename = Path("default")
    while is_filename_valid:
        print("type the file name (without .txt): ")
        filename = Path(input())
        try:
            with open(filename.with_suffix(".txt"), "r", encoding="UTF-8") as _:
                pass
        except Exception as _:
            print("invalid name")
        is_filename_valid = False
    return filename


def generate_text() -> None:
    filename = get_filename()
    for index in range(WORDS_GENERATED):
        print(f"{index} : {generate_word(filename)}")