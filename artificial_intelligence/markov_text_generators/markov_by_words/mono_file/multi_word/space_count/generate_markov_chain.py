import os
from typing import cast

ChainData = tuple[str, str]


EMPTY_CHAR = "¨"


def rename_file(source_filename: str, destination_filename: str) -> None:
    with (
        open(source_filename, "r", encoding="utf-8") as source_file,
        open(destination_filename, "w", encoding="utf-8") as destination_file,
    ):
        content = source_file.read()
        destination_file.write(content)


def update_chain(filename: str, chain_terms: ChainData, index: int) -> None:
    update_chain_file(filename, chain_terms, index)
    rename_file(f"{filename}/c.txt", f"{filename}/{index:03d}.txt")


def update_chain_file(filename: str, chain_terms: ChainData, index: int) -> None:
    with open(f"{filename}/c.txt", "w", encoding="UTF-8") as file_write:
        if f"{index:03d}.txt" not in os.listdir(filename):
            file_write.write(f"{' '.join(chain_terms)} 1\n")
            return
        with open(f"{filename}/{index:03d}.txt", "r", encoding="UTF-8") as file_read:
            lines = file_read.readlines()
        term_exists = False
        for line in lines:
            if not line.strip():
                continue
            characters = line.split()
            terms = cast(ChainData, tuple(characters[:-1]))
            if terms != chain_terms:
                file_write.write(line)
                continue
            frequency = int(characters[-1]) + 1
            terms_flat = " ".join(terms)
            file_write.write(f"{terms_flat} {frequency}\n")
            term_exists = True
        if not term_exists:
            file_write.write(f"{' '.join(chain_terms)} 1\n")


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
        lines = file.readlines()[:-1]
    character_frequency_map: list[int] = []
    for line in lines:
        if not line.strip():
            continue
        words = line.split()
        while len(words) > len(character_frequency_map):
            character_frequency_map.append(0)
        character_frequency_map[len(words) - 1] += 1
        for word_index, word in enumerate(words):
            word_length = len(word)
            for char_index in range(word_length):
                char = word[char_index]
                if char_index == 0:
                    update_chain(filename, (EMPTY_CHAR, char), word_index)
                    if word_length == 1:
                        update_chain(filename, (char, EMPTY_CHAR), word_index)
                        break
                if word_length > 1:
                    if char_index >= word_length - 1:
                        next_char = EMPTY_CHAR
                    else:
                        next_char = word[char_index + 1]
                    update_chain(filename, (char, next_char), word_index)
                    if next_char == EMPTY_CHAR:
                        break
            print(word_length)
    with open(f"{filename}/c.txt", "w", encoding="UTF-8") as character_count_file:
        for index, quantity in enumerate(character_frequency_map):
            character_count_file.write(f"{index} ")
            character_count_file.write(f"{quantity}\n")


if __name__ == "__main__":
    main()
