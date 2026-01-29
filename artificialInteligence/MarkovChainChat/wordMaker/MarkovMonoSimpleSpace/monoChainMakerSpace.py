import os
from typing import cast

ChainData = tuple[str, str]


def rename_file(source_file_name: str, destination_file_name: str) -> None:
    with (
        open(source_file_name, "r", encoding="utf-8") as source_file,
        open(destination_file_name, "w", encoding="utf-8") as destination_file,
    ):
        content = source_file.read()
        destination_file.write(content)


def update_chain(file_name: str, chain_terms: ChainData, index: int) -> None:
    update_chain_file(file_name, chain_terms, index)
    rename_file(f"{file_name}/c.txt", f"{file_name}/{index:03d}.txt")


def update_chain_file(file_name: str, chain_terms: ChainData, index: int) -> None:
    with open(f"{file_name}/c.txt", "w", encoding="UTF-8") as file_write:
        if f"{index:03d}.txt" not in os.listdir(file_name):
            file_write.write(" ".join(chain_terms) + " 1\n")
            return
        with open(f"{file_name}/{index:03d}.txt", "r", encoding="UTF-8") as file_read:
            line = file_read.readline()
            term_exists = False
            while line:
                characters = line.split()
                terms = cast(ChainData, tuple(characters[:-1]))
                if terms == chain_terms:
                    frequency = int(characters[-1]) + 1
                    terms_flat = " ".join(terms)
                    file_write.write(f"{terms_flat} {frequency}\n")
                    term_exists = True
                else:
                    file_write.write(line)
                line = file_read.readline()
            if not term_exists:
                file_write.write(" ".join(chain_terms) + " 1\n")


is_file_name_valid = False
file_name = "default"
while not is_file_name_valid:
    try:
        print("type the file name (without .txt): ")
        file_name = input()
        with open(f"{file_name}.txt", "r", encoding="UTF-8") as file:
            is_file_name_valid = True
            try:
                with open(f"{file_name}/c.txt", "r", encoding="UTF-8") as file_input:
                    file_input = open(f"{file_name}/c.txt", "w", encoding="UTF-8")
            except Exception as _:
                os.mkdir(file_name)
    except Exception as _:
        print("invalid name")
with open(f"{file_name}.txt", "r", encoding="UTF-8") as file:
    line = file.readline()[:-1]
    character_frequency_map:list[int] = []
    while line:
        words = line.split()
        while len(words) > len(character_frequency_map):
            character_frequency_map.append(0)
        character_frequency_map[len(words) - 1] += 1
        for word_index, word in enumerate(words):
            word_length = len(word)
            for char_index in range(word_length):
                char = word[char_index]
                if char_index == 0:
                    update_chain(file_name, ("¨", char), word_index)
                    if word_length == 1:
                        update_chain(file_name, (char, "¨"), word_index)
                        break
                if word_length > 1:
                    if char_index >= word_length - 1:
                        next_char = "¨"
                    else:
                        next_char = word[char_index + 1]
                    update_chain(file_name, (char, next_char), word_index)
                    if next_char == "¨":
                        break
            print(word_length)
        line = file.readline()[:-1]
    with open(f"{file_name}/c.txt", "w", encoding="UTF-8") as character_count_file:
        for index, quantity in enumerate(character_frequency_map):
            character_count_file.write(f"{index} ")
            character_count_file.write(f"{quantity}\n")
