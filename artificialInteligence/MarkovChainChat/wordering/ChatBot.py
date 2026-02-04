from random import randint

EMPTY_CHAR = "¨"

def fetch_word_from_chain(index: int, previous_word: str = "") -> str:
    with open(f"chain/{index:03d}.txt", "r", encoding="utf-8") as file:
        line = file.readline()
        word_frequency_map: dict[str, int] = {}
        while line:
            words = line.split()
            if index == 0:
                word = words[0]
                number = int(words[-1])
            else:
                if previous_word == words[0]:
                    word = words[1]
                    number = int(words[-1])
                else:
                    line = file.readline()
                    continue
            word_frequency_map[word] = number
            line = file.readline()
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
    for index in range(1000):
        print(f"{index} : {generate_message()}")


if __name__ == "__main__":
    main()
