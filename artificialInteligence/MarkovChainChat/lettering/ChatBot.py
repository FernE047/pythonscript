from random import randint

EMPTY_CHAR = "¨"
GENERATED_MESSAGES = 1000

def fetch_character_from_chain(index: int, previous_character: str = "") -> str:
    with open(f"chain/{index:03d}.txt", "r", encoding="utf-8") as file:
        lines = file.read().splitlines()
    character_frequency_map: dict[str, int] = {}
    for line in lines:
        if not line:
            continue
        if index != 0:
            if previous_character != line[0]:
                continue
            character = line[2]
            frequency_count = int(line[4:-1])
        else:
            character = line[0]
            frequency_count = int(line[2:-1])
        character_frequency_map[character] = frequency_count
    frequencies = list(character_frequency_map.values())
    total = sum(frequencies)
    chosen = randint(1, total)
    cumulative = 0
    for index, value in enumerate(frequencies):
        cumulative += value
        if cumulative >= chosen:
            return list(character_frequency_map.keys())[index]
    return ""


def generate_message() -> str:
    message = ""
    letter = fetch_character_from_chain(0)
    while letter != EMPTY_CHAR:
        message += letter
        letter = fetch_character_from_chain(len(message), letter)
    return message


def main() -> None:
    for index in range(GENERATED_MESSAGES):
        print(str(index) + " : " + generate_message())


if __name__ == "__main__":
    main()
