from pathlib import Path
from random import randint

EMPTY_CHAR = "¨"
WORDS_GENERATED = 1000
CHAIN_FOLDER = Path("chain")

def fetch_word_from_chain(index: int, previous_word: str = "") -> str:
    with open(CHAIN_FOLDER / f"{index:03d}.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()
    word_frequency_map: dict[str, int] = {}
    for line in lines:
        if not line.strip():
            continue
        words = line.split()
        if index == 0:
            word = words[0]
        elif previous_word == words[0]:
            word = words[1]
        else:
            continue
        number = int(words[-1])
        word_frequency_map[word] = number
    frequencies = list(word_frequency_map.values())
    total = sum(frequencies)
    chosen = randint(1, total)
    cumulative_sum = 0
    for index, valor in enumerate(frequencies):
        cumulative_sum += valor
        if cumulative_sum >= chosen:
            return list(word_frequency_map.keys())[index]
    return ""


def generate_message() -> str:
    message: list[str] = []
    word = fetch_word_from_chain(0)
    while word != EMPTY_CHAR:
        message.append(word)
        word = fetch_word_from_chain(len(message), word)
    return " ".join(message)


def generate_markov_messages() -> None:
    for index in range(WORDS_GENERATED):
        print(f"{index} : {generate_message()}")

if __name__ == "__main__":
    generate_markov_messages()