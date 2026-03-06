from pathlib import Path
import random
from generate_chain import CHAIN_FOLDER

EMPTY_CHAR = "¨"
GENERATED_MESSAGES = 1000
OUTPUT_FOLDER = Path("out")
OUTPUT_FOLDER.mkdir(exist_ok=True)
OUTPUT_FILE = OUTPUT_FOLDER / "generated_messages.txt"


def build_character_frequency_map(
    index: int, previous_character: str, lines: list[str]
) -> dict[str, int]:
    character_frequency_map: dict[str, int] = {}
    for line in lines:
        if not line:
            continue
        if index == 0:
            character = line[0]
            frequency_count = int(line[2:])
            character_frequency_map[character] = frequency_count
            continue
        if previous_character != line[0]:
            continue
        character = line[2]
        frequency_count = int(line[4:])
        character_frequency_map[character] = frequency_count
    return character_frequency_map


def fetch_character_from_chain(index: int, previous_character: str = "") -> str:
    with open(CHAIN_FOLDER / f"{index:03d}.txt", "r", encoding="utf-8") as file:
        lines = file.read().splitlines()
    character_frequency_map = build_character_frequency_map(
        index, previous_character, lines
    )
    frequencies = list(character_frequency_map.values())
    if len(frequencies) == 0:
        return EMPTY_CHAR
    return random.choices(
        list(character_frequency_map.keys()), weights=frequencies, k=1
    )[0]


def generate_message() -> str:
    message = ""
    letter = fetch_character_from_chain(0)
    while letter != EMPTY_CHAR:
        message += letter
        letter = fetch_character_from_chain(len(message), letter)
    return message


def generate_messages() -> None:
    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        for index in range(GENERATED_MESSAGES):
            message = generate_message()
            output = f"{index} : {message}"
            print(output)
            file.write(f"{output}\n")