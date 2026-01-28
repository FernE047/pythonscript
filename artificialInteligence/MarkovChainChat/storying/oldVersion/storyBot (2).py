from random import randint


def generate_start_text(is_title: bool) -> list[str]:
    global CHAINSIZE
    first_word = generate_word(is_title)
    if is_title:
        chain_directory = f"chainTitle/{CHAINSIZE}"
    else:
        chain_directory = f"chainStory/{CHAINSIZE}"
    chain_file_path = f"{chain_directory}/chain.txt"
    with open(chain_file_path, "r", encoding="utf-8") as file:
        line = file.readline().lower()
        word_frequency_map: dict[str, int] = {}
        while line:
            words = line.split()
            if first_word == words[0]:
                usable_words = words[1:-1]
                number = int(words[-1])
            else:
                line = file.readline().lower()
                continue
            phrase = " ".join(usable_words)
            if phrase not in word_frequency_map.keys():
                word_frequency_map[phrase] = number
            else:
                word_frequency_map[phrase] += number
            line = file.readline().lower()
        total = sum(list(word_frequency_map.values()))
        chosen = randint(1, total)
        cumulative = 0
        for index, value in enumerate(word_frequency_map.values()):
            cumulative += value
            if cumulative >= chosen:
                return [first_word] + list(word_frequency_map.keys())[index].split()
    return ["¨" for _ in range(CHAINSIZE + 1)]


def generate_word(is_title: bool, previous_words: list[str] | None = None) -> str:
    global CHAINSIZE
    if previous_words is None:
        previous_words = ["¨" for _ in range(CHAINSIZE)]
    if is_title:
        chain_directory = f"chainTitle/{CHAINSIZE}"
    else:
        chain_directory = f"chainStory/{CHAINSIZE}"
    previous_phrase = " ".join(previous_words)
    chain_file_name = f"{chain_directory}/chain.txt"
    with open(chain_file_name, "r", encoding="utf-8") as file:
        line = file.readline().lower()
        word_frequency_map: dict[str, int] = {}
        while line:
            words = line.split()
            previous_phrase_test = " ".join(words[:-2])
            if previous_phrase == previous_phrase_test:
                word = words[-2]
                number = int(words[-1])
            else:
                line = file.readline().lower()
                continue
            if word not in word_frequency_map.keys():
                word_frequency_map[word] = number
            else:
                word_frequency_map[word] += number
            line = file.readline().lower()
        frequencies = list(word_frequency_map.values())
        total = sum(frequencies)
        chosen = randint(1, total)
        cumulative_frequency = 0
        for index, value in enumerate(frequencies):
            cumulative_frequency += value
            if cumulative_frequency >= chosen:
                return list(word_frequency_map.keys())[index]
    return "¨"


def generate_text(is_title: bool) -> str:
    global CHAINSIZE
    generated_words: list[str] = []
    initial_words = generate_start_text(is_title)
    for word in initial_words[:-1]:
        if word == "¨":
            return " ".join(generated_words)
        generated_words.append(word)
        print(word, end=" ")
    word = initial_words[-1]
    index = 1
    while word != "¨":
        generated_words.append(word)
        print(word, end=" ")
        word = generate_word(is_title, generated_words[index : index + CHAINSIZE])
        index += 1
    return " ".join(generated_words)


CHAINSIZE = 2
for a in range(10):
    generate_text(True)
    print(" : ", end="")
    generate_text(False)
    print("\n")
