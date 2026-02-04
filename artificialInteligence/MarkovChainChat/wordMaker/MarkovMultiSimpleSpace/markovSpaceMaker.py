from random import randint
from typing import Any
from numpy.random import choice

IS_DEBUG = False
WORDS_GENERATED = 1000
EMPTY_CHAR = "¨"



def print_debug(*args: Any) -> None:
    if IS_DEBUG:
        for arg in args:
            print(repr(arg))


def generate_char(
    filename: str, index: int, space_index: int, previous_char: str = ""
) -> str:
    with open(f"{filename}/{index:03d}.txt", encoding="utf-8") as file:
        line = file.readline()
        character_weights: dict[str, int] = {}
        while line:
            if int(line[0]) == space_index:
                if index == 0:
                    char = line[2]
                    frequency = int(line[4:-1])
                elif previous_char == line[2]:
                    char = line[4]
                    frequency = int(line[6:-1])
                else:
                    line = file.readline()
                    continue
                character_weights[char] = frequency
            line = file.readline()
        print_debug(previous_char, character_weights, index, space_index)
        total = sum(list(character_weights.values()))
        chosen = randint(1, total)
        cumulative_frequency = 0
        for index, value in enumerate(character_weights.values()):
            cumulative_frequency += value
            if cumulative_frequency >= chosen:
                return list(character_weights.keys())[index]
        return ""


def generate_word(filename: str, space_index: int) -> str:
    generated_word = ""
    char = generate_char(filename, 0, space_index)
    while char != EMPTY_CHAR:
        generated_word += char
        char = generate_char(filename, len(generated_word), space_index, char)
    return generated_word


def normalize_statistics(frequency_map: list[int]) -> list[float]:
    total_frequency = sum(frequency_map)
    frequency_normalized = [frequency / total_frequency for frequency in frequency_map]
    while sum(frequency_normalized) != 1:
        if sum(frequency_normalized) > 1:
            add = sum(frequency_normalized) - 1
            frequency_normalized[
                frequency_normalized.index(max(frequency_normalized))
            ] -= add
        elif sum(frequency_normalized) < 1:
            add = 1 - sum(frequency_normalized)
            frequency_normalized[
                frequency_normalized.index(min(frequency_normalized))
            ] += add
    return frequency_normalized


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
    word_occurrence_map: list[int] = []
    with open(filename + "/c.txt", "r", encoding="UTF-8") as markov_chain_file:
        linha = markov_chain_file.readline()[:-1].split()
        while linha:
            word_occurrence_map.append(int(linha[-1]))
            linha = markov_chain_file.readline()[:-1].split()
    word_frequencies_map = normalize_statistics(word_occurrence_map)
    for _ in range(WORDS_GENERATED):
        generated_words: list[str] = []
        word_quantity = choice(
            [word_index for word_index in range(1, len(word_frequencies_map) + 1)],
            1,
            p=word_frequencies_map,
        )[0]
        for index in range(word_quantity):
            print_debug(index)
            generated_words.append(generate_word(filename, index))
        print(" ".join(generated_words), end="\n")


if __name__ == "__main__":
    main()
