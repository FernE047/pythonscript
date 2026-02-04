from random import randint

EMPTY_CHAR = "¨"
GENERATED_STORIES = 10

def generate_word(index: int, is_title: bool, previous_word: str = "") -> str:
    if is_title:
        chain_directory = "chainTitle/0"
    else:
        chain_directory = "chainStory/0"
    name = f"{chain_directory}/{index:03d}.txt"
    with open(name, "r", encoding="utf-8") as file:
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
        total = sum(list(word_frequency_map.values()))
        chosen = randint(1, total)
        sum_values = 0
        for index, value in enumerate(word_frequency_map.values()):
            sum_values += value
            if sum_values >= chosen:
                return list(word_frequency_map.keys())[index]
    return EMPTY_CHAR


def generate_text(is_title: bool) -> str:
    texto: list[str] = []
    word = generate_word(0, is_title)
    while word != EMPTY_CHAR:
        texto.append(word)
        word = generate_word(len(texto), is_title, word)
    return " ".join(texto)


def main() -> None:
    for _ in range(GENERATED_STORIES):
        print(generate_text(True) + " : " + generate_text(False), end="\n\n")


if __name__ == "__main__":
    main()
