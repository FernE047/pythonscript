from pathlib import Path
from fetch_messages import CLEAN_INPUT_FILE

EMPTY_CHAR = "¨"
INPUT_FILE = CLEAN_INPUT_FILE
CHAIN_FOLDER = Path("chain")

MarkovChain = dict[str, int]
MarkovCollection = dict[int, MarkovChain]


def update_chain_file(index: int, markov_chain: MarkovChain) -> None:
    with open(CHAIN_FOLDER / f"{index:03d}.txt", "w", encoding="utf-8") as chain_file:
        for char, count in markov_chain.items():
            chain_file.write(f"{char} {count}\n")


def process_message(
    markov_collection: MarkovCollection, message: str, index: int
) -> None:
    message_length = len(message)
    if index >= message_length:
        return
    character = message[index]
    if character == "\n":
        return
    if index not in markov_collection:
        markov_collection[index] = {}
    if index + 1 not in markov_collection:
        markov_collection[index + 1] = {}
    markov_chain = markov_collection[index]
    if index == 0:
        markov_collection[index][character] = markov_chain.get(character, 0) + 1
    if message_length >= 1:
        try:
            next_character = message[index + 1]
        except IndexError:
            next_character = EMPTY_CHAR
        if next_character == "\n":
            next_character = EMPTY_CHAR
        markov_collection[index + 1][f"{character} {next_character}"] = (
            markov_chain.get(f"{character} {next_character}", 0) + 1
        )


def generate_character_chain() -> None:
    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        lines = [line.strip() for line in file.readlines()]
    markov_collection: MarkovCollection = {}
    for message in lines:
        message_length = len(message)
        for index in range(message_length):
            process_message(markov_collection, message, index)
    for index, markov_chain in markov_collection.items():
        update_chain_file(index, markov_chain)
