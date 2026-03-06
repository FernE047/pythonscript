from pathlib import Path
from fetch_messages import CLEAN_INPUT_FILE

EMPTY_CHAR = "¨"
INPUT_FILE = CLEAN_INPUT_FILE
CHAIN_FOLDER = Path("chain")
MAIN_CHAIN_FILE = CHAIN_FOLDER / "c.txt"

MarkovChain = dict[str, int]
MarkovCollection = dict[int, MarkovChain]


def rename_file(source_filename: Path, destination_filename: Path) -> None:
    with (
        open(source_filename, "r", encoding="utf-8") as source_file,
        open(destination_filename, "w", encoding="utf-8") as destination_file,
    ):
        content = source_file.read()
        destination_file.write(content)


def update_chain_file(index: int, keywords: list[str]) -> None:
    update_keyword_count(index, keywords)
    rename_file(MAIN_CHAIN_FILE, CHAIN_FOLDER / f"{index:03d}.txt")


def update_keyword_count(index: int, keywords: list[str]) -> None: #stopped here
    with open(MAIN_CHAIN_FILE, "w", encoding="utf-8") as file_write:
        if not any(f"{index:03d}.txt" == file.name for file in CHAIN_FOLDER.iterdir()):
            file_write.write(f"{' '.join(keywords)} 1\n")
            return
        with open(
            CHAIN_FOLDER / f"{index:03d}.txt", "r", encoding="utf-8"
        ) as file_read:
            lines = file_read.readlines()
        keyword_exists = False
        for line in lines:
            if not line.strip():
                continue
            words = line.split()
            if words[:-1] != keywords:
                file_write.write(line)
                continue
            words[-1] = str(int(words[-1]) + 1)
            file_write.write(f"{' '.join(words)}\n")
            keyword_exists = True
        if not keyword_exists:
            file_write.write(f"{' '.join(keywords)} 1\n")

def process_message(
    markov_collection: MarkovCollection, message: list[str], index: int
) -> None:
    message_length = len(message)
    if index >= message_length:
        return
    word = message[index]
    if word == "\n":
        return
    if index not in markov_collection:
        markov_collection[index] = {}
    if index + 1 not in markov_collection:
        markov_collection[index + 1] = {}
    markov_chain = markov_collection[index]
    if index == 0:
        markov_collection[index][word] = markov_chain.get(word, 0) + 1
    if message_length >= 1:
        try:
            next_word = message[index + 1]
        except IndexError:
            next_word = EMPTY_CHAR
        if next_word == "\n":
            next_word = EMPTY_CHAR
        markov_collection[index + 1][f"{word} {next_word}"] = (
            markov_chain.get(f"{word} {next_word}", 0) + 1
        )


def generate_markov_chain() -> None:
    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        lines = [line.strip() for line in file.readlines()]
    markov_collection: MarkovCollection = {}
    for line in lines:
        words = line.split()
        word_count = len(words)
        for index in range(word_count):
            process_message(markov_collection, words, index)
    for index, markov_chain in markov_collection.items():
        update_chain_file(index, list(markov_chain.keys())[0].split()[:-1])
