from random import randint
from numpy.random import choice


def generate_char(filename: str, previous_char: str = "¨") -> str:
    with open(filename, "r", encoding="UTF-8") as file:
        line = file.readline()
        character_weights: dict[str, int] = {}
        while line:
            chars = [line[a] for a in range(0, 5, 2)]
            if previous_char == chars[0]:
                char = chars[1]
                frequency = int(chars[-1])
                character_weights[char] = frequency
            line = file.readline()
        total = sum(list(character_weights.values()))
        chosen = randint(1, total)
        cumulative_frequency = 0
        for index, value in enumerate(character_weights.values()):
            cumulative_frequency += value
            if cumulative_frequency >= chosen:
                file.close()
                return list(character_weights.keys())[index]
        return ""


def generate_word(filename: str) -> str:
    generated_chars: list[str] = []
    char = generate_char(filename)
    while char != "¨":
        generated_chars.append(char)
        char = generate_char(filename, char)
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
    for _ in range(1000):
        generated_words: list[str] = []
        word_quantities = choice(
            [b for b in range(1, len(word_frequencies_map) + 1)],
            1,
            p=word_frequencies_map,
        )[0]
        for b in range(word_quantities):
            generated_words.append(generate_word(f"{filename}/{b:03d}.txt"))
        print(" ".join(generated_words))


if __name__ == "__main__":
    main()
