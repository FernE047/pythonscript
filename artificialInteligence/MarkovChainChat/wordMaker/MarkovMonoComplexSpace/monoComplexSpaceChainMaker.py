import os
from typing import cast

ChainData = tuple[str, str, str]


def rename_file(source_file_name: str, destination_file_name: str) -> None:
    with (
        open(source_file_name, "r", encoding="utf-8") as source_file,
        open(destination_file_name, "w", encoding="utf-8") as destination_file,
    ):
        content = source_file.read()
        destination_file.write(content)


def update_chain_file(file_name: str, keywords: ChainData, index: int) -> None:
    update_keyword_count(file_name, keywords, index)
    rename_file(f"{file_name}/c.txt", f"{file_name}/{index:03d}.txt")


def update_keyword_count(file_name: str, keywords: ChainData, index: int) -> None:
    with open(f"{file_name}/c.txt", "w", encoding="UTF-8") as fileWrite:
        keywords_flat = " ".join(keywords)
        if f"{index:03d}.txt" not in os.listdir(file_name):
            fileWrite.write(f"{keywords_flat} 1\n")
            return
        with open(f"{file_name}/{index:03d}.txt", "r", encoding="UTF-8") as file_read:
            line = file_read.readline()
            keyword_found = False
            while line:
                palavras = cast(tuple[str, str, str, str], tuple(line.split()))
                keywords_read = cast(ChainData, tuple(palavras[:-1]))
                if keywords_read != keywords:
                    fileWrite.write(line)
                    line = file_read.readline()
                    continue
                frequency = int(palavras[-1]) + 1
                fileWrite.write(f"{keywords_flat} {frequency}\n")
                keyword_found = True
                line = file_read.readline()
            if not keyword_found:
                fileWrite.write(f"{keywords_flat} 1\n")


def get_file_name() -> str:
    is_file_name_valid = True
    file_name = "default"
    while is_file_name_valid:
        print("type the file name (without .txt): ")
        file_name = input()
        try:
            with open(f"{file_name}.txt", "r", encoding="UTF-8") as _:
                pass
        except Exception as _:
            print("invalid name")
        is_file_name_valid = False
    return file_name


file_name = get_file_name()
with open(f"{file_name}.txt", "r", encoding="UTF-8") as file:
    line = file.readline()[:-1]
    word_frequency: list[int] = []
    length = 0
    while line:
        words = line.split()
        while len(words) > len(word_frequency):
            word_frequency.append(0)
        word_frequency[len(words) - 1] += 1
        for word_index, word in enumerate(words):
            length = len(word)
            previous_character = ""
            for index, character in enumerate(word):
                if index == 0:
                    update_chain_file(file_name, ("¨", "¨", character), word_index)
                    if length == 1:
                        update_chain_file(file_name, ("¨", character, "¨"), word_index)
                        break
                    next_character = word[index + 1]
                    update_chain_file(
                        file_name, ("¨", character, next_character), word_index
                    )
                    previous_character = character
                    continue
                if length <= 1:
                    previous_character = character
                    continue
                if index >= length - 1:
                    next_character = "¨"
                else:
                    next_character = word[index + 1]
                update_chain_file(
                    file_name,
                    (previous_character, character, next_character),
                    word_index,
                )
                if next_character == "¨":
                    break
                previous_character = character
        line = file.readline()[:-1]
    with open(f"{file_name}/c.txt", "w", encoding="UTF-8") as frequency_output_file:
        for index, quantity in enumerate(word_frequency):
            frequency_output_file.write(f"{index} {quantity}\n")
    print(length)
