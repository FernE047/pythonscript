from random import randint
from numpy.random import choice


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
word_occurrence_map: list[int] = []
with open(file_name + "/c.txt", "r", encoding="UTF-8") as markov_chain_file:
    linha = markov_chain_file.readline()[:-1].split()
    while linha:
        word_occurrence_map.append(int(linha[-1]))
        linha = markov_chain_file.readline()[:-1].split()
word_frequencies_map = normalize_statistics(word_occurrence_map)
for _ in range(1000):
    generated_words: list[str] = []
    word_quantity = choice(
        [word_index for word_index in range(1, len(word_frequencies_map) + 1)],
        1,
        p=word_frequencies_map,
    )[0]
    for index in range(word_quantity):
        generated_words.append(generate_word(f"{file_name}/{index:03d}.txt"))
    print(" ".join(generated_words))
