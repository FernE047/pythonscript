import os
from pathlib import Path

EMPTY_CHAR = "¨"
INPUT_FILE = Path("sohMensagens.txt")
CHAIN_FOLDER = Path("chain")
MAIN_CHAIN_FILE = CHAIN_FOLDER / "c.txt"


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


def update_keyword_count(index: int, keywords: list[str]) -> None:
    with open(MAIN_CHAIN_FILE, "w", encoding="utf-8") as file_write:
        if f"{index:03d}.txt" not in os.listdir(CHAIN_FOLDER):
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


def generate_markov_chain() -> None:
    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        message = file.readline()
        while message:
            words = message.split()
            word_count = len(words)
            for index, word in enumerate(words):
                if index == 0:
                    update_chain_file(index, [word])
                    if word_count == 1:
                        update_chain_file(index + 1, [word, EMPTY_CHAR])
                        break
                if word_count > 1:
                    if index >= word_count - 1:
                        next_word = EMPTY_CHAR
                    else:
                        next_word = words[index + 1]
                    update_chain_file(index + 1, [word, next_word])
                    if next_word == EMPTY_CHAR:
                        break
            message = file.readline()
