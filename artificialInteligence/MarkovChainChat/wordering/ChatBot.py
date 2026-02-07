from random import randint

EMPTY_CHAR = "¨"
WORDS_GENERATED = 1000

def fetch_word_from_chain(index: int, previous_word: str = "") -> str:
    with open(f"chain/{index:03d}.txt", "r", encoding="utf-8") as file:
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
    message = ""
    letter = fetch_word_from_chain(0)
    while letter != EMPTY_CHAR:
        message += letter
        letter = fetch_word_from_chain(len(message), letter)
    return message


def main() -> None:
    for index in range(WORDS_GENERATED):
        print(f"{index} : {generate_message()}")


if __name__ == "__main__":
    main()
