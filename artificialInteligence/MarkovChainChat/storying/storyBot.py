from random import randint


DIRECTORY = "./FanficAnime/"
TAMANHO = 1
EMPTY_CHAR = "¨"

def generate_initial_words(is_title: bool) -> list[str]:
    initial_word = generate_word(is_title)
    if is_title:
        directory = f"{DIRECTORY}chainTitle/{TAMANHO}"
    else:
        directory = f"{DIRECTORY}chainStory/{TAMANHO}"
    filename = f"{directory}/chain.txt"
    with open(filename, "r", encoding="utf-8") as file:
        line = file.readline().lower()
        word_frequency_map: dict[str, int] = {}
        while line:
            words = line.split()
            if initial_word == words[0]:
                usable_words = words[1:-1]
                number = int(words[-1])
            else:
                line = file.readline().lower()
                continue
            word = " ".join(usable_words)
            if word not in word_frequency_map.keys():
                word_frequency_map[word] = number
            else:
                word_frequency_map[word] += number
            line = file.readline().lower()
        total = sum(list(word_frequency_map.values()))
        chosen = randint(1, total)
        cumulative_sum = 0
        for index, value in enumerate(word_frequency_map.values()):
            cumulative_sum += value
            if cumulative_sum >= chosen:
                return [initial_word] + list(word_frequency_map.keys())[index].split()
    return [initial_word, EMPTY_CHAR]


def generate_word(is_title: bool, previous_words: list[str] | None = None) -> str:
    if previous_words is None:
        previous_words = [EMPTY_CHAR for _ in range(TAMANHO)]
    if is_title:
        directory = f"{DIRECTORY}chainTitle/{TAMANHO}"
    else:
        directory = f"{DIRECTORY}chainStory/{TAMANHO}"
    previous = " ".join(previous_words)
    filename = f"{directory}/chain.txt"
    with open(filename, "r", encoding="utf-8") as file:
        line = file.readline().lower()
        word_frequency_map: dict[str, int] = {}
        while line:
            words = line.split()
            word_test = " ".join(words[:-2])
            if previous != word_test:
                line = file.readline().lower()
                continue
            word = words[-2]
            number = int(words[-1])
            if word not in word_frequency_map.keys():
                word_frequency_map[word] = number
            else:
                word_frequency_map[word] += number
            line = file.readline().lower()
        total = sum(list(word_frequency_map.values()))
        chosen = randint(1, total)
        cumulative_sum = 0
        for index, value in enumerate(word_frequency_map.values()):
            cumulative_sum += value
            if cumulative_sum >= chosen:
                return list(word_frequency_map.keys())[index]
    return EMPTY_CHAR


def generate_text(is_title: bool) -> str:
    words: list[str] = []
    initial_words = generate_initial_words(is_title)
    for word in initial_words[:-1]:
        if word == EMPTY_CHAR:
            return " ".join(words)
        words.append(word)
        print(word, end=" ")
    word = initial_words[-1]
    index = 1
    while word != EMPTY_CHAR:
        words.append(word)
        print(word, end=" ")
        word = generate_word(is_title, words[index : index + TAMANHO])
        index += 1
    return " ".join(words)


def main() -> None:
    for _ in range(1000):
        generate_text(True)
        print(" : ", end="")
        generate_text(False)
        print("\n")


if __name__ == "__main__":
    main()
