from random import randint


def generate_word(is_title: bool, previous_word: str = "¨") -> str:
    if is_title:
        directory = "monoChainTitle"
    else:
        directory = "monoChainStory"
    filename = f"{directory}/chain.txt"
    with open(filename, "r", encoding="utf-8") as file:
        line = file.readline()
        word_frequency_map: dict[str, int] = {}
        while line:
            words = line.split()
            if previous_word == words[0]:
                word = words[1]
                number = int(words[-1])
            else:
                line = file.readline()
                continue
            word_frequency_map[word] = number
            line = file.readline()
        total = sum(list(word_frequency_map.values()))
        chosen = randint(1, total)
        cumulative_sum = 0
        for index, value in enumerate(word_frequency_map.values()):
            cumulative_sum += value
            if cumulative_sum >= chosen:
                return list(word_frequency_map.keys())[index]
    return "¨"


def generate_text(is_title: bool) -> str:
    word_list: list[str] = []
    word = generate_word(is_title)
    while word != "¨":
        word_list.append(word)
        word = generate_word(is_title, word)
    return " ".join(word_list)


def main() -> None:
    for _ in range(10):
        print(generate_text(True) + " : " + generate_text(False), end="\n\n")


if __name__ == "__main__":
    main()
