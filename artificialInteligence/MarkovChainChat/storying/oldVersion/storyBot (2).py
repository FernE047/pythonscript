from random import randint


class ChainManager:
    def __init__(self, chain_size: int) -> None:
        self.chain_size = chain_size

    def get_chain_path(self, is_title: bool) -> str:
        if is_title:
            return f"chainTitle/{self.chain_size}/chain.txt"
        else:
            return f"chainStory/{self.chain_size}/chain.txt"


def generate_start_text(is_title: bool, chain_manager: ChainManager) -> list[str]:
    first_word = generate_word(is_title, chain_manager)
    chain_file_path = chain_manager.get_chain_path(is_title)
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
    return ["¨" for _ in range(chain_manager.chain_size + 1)]


def generate_word(
    is_title: bool, chain_manager: ChainManager, previous_words: list[str] | None = None
) -> str:
    if previous_words is None:
        previous_words = ["¨" for _ in range(chain_manager.chain_size)]
    chain_filename = chain_manager.get_chain_path(is_title)
    previous_phrase = " ".join(previous_words)
    with open(chain_filename, "r", encoding="utf-8") as file:
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


def generate_text(is_title: bool, chain_manager: ChainManager) -> str:
    generated_words: list[str] = []
    initial_words = generate_start_text(is_title, chain_manager)
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
        word = generate_word(
            is_title,
            chain_manager,
            generated_words[index : index + chain_manager.chain_size],
        )
        index += 1
    return " ".join(generated_words)


def main() -> None:
    chain_manager = ChainManager(chain_size=2)
    for _ in range(10):
        generate_text(True, chain_manager)
        print(" : ", end="")
        generate_text(False, chain_manager)
        print("\n")


if __name__ == "__main__":
    main()
