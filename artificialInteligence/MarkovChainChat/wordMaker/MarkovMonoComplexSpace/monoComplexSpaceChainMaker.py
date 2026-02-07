import os
from typing import cast

ChainData = tuple[str, str, str]


EMPTY_CHAR = "¨"


def rename_file(source_filename: str, destination_filename: str) -> None:
    with (
        open(source_filename, "r", encoding="utf-8") as source_file,
        open(destination_filename, "w", encoding="utf-8") as destination_file,
    ):
        content = source_file.read()
        destination_file.write(content)


def update_chain_file(filename: str, keywords: ChainData, index: int) -> None:
    update_keyword_count(filename, keywords, index)
    rename_file(f"{filename}/c.txt", f"{filename}/{index:03d}.txt")


def update_keyword_count(filename: str, keywords: ChainData, index: int) -> None:
    with open(f"{filename}/c.txt", "w", encoding="UTF-8") as fileWrite:
        keywords_flat = " ".join(keywords)
        if f"{index:03d}.txt" not in os.listdir(filename):
            fileWrite.write(f"{keywords_flat} 1\n")
            return
        with open(f"{filename}/{index:03d}.txt", "r", encoding="UTF-8") as file_read:
            lines = file_read.readlines()
        keyword_found = False
        for line in lines:
            palavras = cast(tuple[str, str, str, str], tuple(line.split()))
            keywords_read = cast(ChainData, tuple(palavras[:-1]))
            if keywords_read != keywords:
                fileWrite.write(line)
                continue
            frequency = int(palavras[-1]) + 1
            fileWrite.write(f"{keywords_flat} {frequency}\n")
            keyword_found = True
        if not keyword_found:
            fileWrite.write(f"{keywords_flat} 1\n")


def get_filename() -> str:
    is_filename_valid = True
    filename = "default"
    while is_filename_valid:
        print("type the file name (without .txt): ")
        filename = input()
        try:
            with open(f"{filename}.txt", "r", encoding="UTF-8") as _:
                pass
        except Exception as _:
            print("invalid name")
        is_filename_valid = False
    return filename


def main() -> None:
    filename = get_filename()
    with open(f"{filename}.txt", "r", encoding="UTF-8") as file:
        lines = file.readlines()
    word_frequency: list[int] = []
    length = 0
    for line in lines:
        line = line.strip()
        if not line:
            continue
        words = line.split()
        while len(words) > len(word_frequency):
            word_frequency.append(0)
        word_frequency[len(words) - 1] += 1
        for word_index, word in enumerate(words):
            length = len(word)
            previous_character = ""
            for index, character in enumerate(word):
                if index == 0:
                    update_chain_file(
                        filename, (EMPTY_CHAR, EMPTY_CHAR, character), word_index
                    )
                    if length == 1:
                        update_chain_file(
                            filename,
                            (EMPTY_CHAR, character, EMPTY_CHAR),
                            word_index,
                        )
                        break
                    next_character = word[index + 1]
                    update_chain_file(
                        filename,
                        (EMPTY_CHAR, character, next_character),
                        word_index,
                    )
                    previous_character = character
                    continue
                if length <= 1:
                    previous_character = character
                    continue
                if index >= length - 1:
                    next_character = EMPTY_CHAR
                else:
                    next_character = word[index + 1]
                update_chain_file(
                    filename,
                    (previous_character, character, next_character),
                    word_index,
                )
                if next_character == EMPTY_CHAR:
                    break
                previous_character = character
    with open(f"{filename}/c.txt", "w", encoding="UTF-8") as frequency_output_file:
        for index, quantity in enumerate(word_frequency):
            frequency_output_file.write(f"{index} {quantity}\n")
    print(length)


if __name__ == "__main__":
    main()
