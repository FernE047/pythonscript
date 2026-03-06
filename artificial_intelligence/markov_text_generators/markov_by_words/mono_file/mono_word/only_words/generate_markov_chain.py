from collections import Counter
from pathlib import Path
from time import time
from typing import cast
from datetime import timedelta

ChainData = tuple[str, str, str]


EMPTY_CHAR = "¨"


def rename_file(source_filename: Path, destination_filename: Path) -> None:
    with (
        open(source_filename, "r", encoding="utf-8") as source_file,
        open(destination_filename, "w", encoding="utf-8") as destination_file,
    ):
        content = source_file.read()
        destination_file.write(content)


def update_chain_file(filename: Path, keywords: list[ChainData]) -> None:
    update_keywords_in_chain(filename, keywords)
    rename_file(filename / "c.txt", filename / "chain.txt")


def update_keywords_in_chain(filename: Path, keyword_tuples: list[ChainData]) -> None:
    with open(filename / "c.txt", "w", encoding="UTF-8") as file_write:
        counter = Counter([" ".join(keyword_tuple) for keyword_tuple in keyword_tuples])
        unique_keywords: set[ChainData] = set()
        if not any("chain.txt" == file.name for file in filename.iterdir()):
            for keyword_tuple in keyword_tuples:
                if keyword_tuple not in unique_keywords:
                    keyword_tuple_flat = " ".join(keyword_tuple)
                    keyword_tuple_frequency = counter[keyword_tuple_flat]
                    file_write.write(
                        f"{keyword_tuple_flat} {keyword_tuple_frequency}\n"
                    )
                    unique_keywords.add(keyword_tuple)
            return
        with open(filename / "chain.txt", "r", encoding="UTF-8") as file_read:
            lines = file_read.readlines()
        for line in lines:
            if not line.strip():
                continue
            keywords_read = cast(tuple[str, str, str, str], tuple(line.split()))
            keyword_tuple = cast(ChainData, tuple(keywords_read[:-1]))
            if keyword_tuple not in keyword_tuples:
                file_write.write(line)
                continue
            frequency = int(keywords_read[-1])
            keyword_tuple_flat = " ".join(keyword_tuple)
            frequency += counter[keyword_tuple_flat]
            while keyword_tuple in keyword_tuples:
                keyword_tuples.remove(keyword_tuple)
            file_write.write(f"{keyword_tuple_flat} {frequency}\n")
        for keyword_tuple in keyword_tuples:
            if keyword_tuple not in unique_keywords:
                keyword_tuple_flat = " ".join(keyword_tuple)
                frequency = counter[keyword_tuple_flat]
                file_write.write(f"{keyword_tuple_flat} {frequency}\n")
                unique_keywords.add(keyword_tuple)


def get_file_path() -> Path:
    is_filename_valid = True
    filename = Path("default")
    while is_filename_valid:
        print("type the file name (without .txt): ")
        filename = Path(input())
        try:
            with open(filename.with_suffix(".txt"), "r", encoding="UTF-8") as _:
                pass
        except Exception as _:
            print("invalid name")
        is_filename_valid = False
    return filename


def generate_chain() -> None:
    file_path = get_file_path()
    start_time = time()
    with open(file_path.with_suffix(".txt"), "r", encoding="UTF-8") as file:
        lines = file.readlines()
    word_frequency: list[int] = []
    word_length = 0
    count = 0
    update_chain_values: list[ChainData] = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        words = line.split()
        while len(words) > len(word_frequency):
            word_frequency.append(0)
        word_frequency[len(words) - 1] += 1
        for word in words:
            word_length = len(word)
            previous_character = ""
            for index in range(word_length):
                current_character = word[index]
                if index == 0:
                    update_chain_values.append((EMPTY_CHAR, EMPTY_CHAR, current_character))
                    if word_length == 1:
                        update_chain_values.append((EMPTY_CHAR, current_character, EMPTY_CHAR))
                        break
                    else:
                        next_character = word[index + 1]
                        update_chain_values.append(
                            (EMPTY_CHAR, current_character, next_character)
                        )
                        previous_character = current_character
                    continue
                if word_length > 1:
                    if index >= word_length - 1:
                        next_character = EMPTY_CHAR
                    else:
                        next_character = word[index + 1]
                    update_chain_values.append(
                        (previous_character, current_character, next_character)
                    )
                    if next_character == EMPTY_CHAR:
                        break
                previous_character = current_character
        if count == 100:
            update_chain_file(file_path, update_chain_values)
            update_chain_values = []
            count = 0
        else:
            count += 1
    update_chain_file(file_path, update_chain_values)
    with open(file_path / "length.txt", "w", encoding="UTF-8") as arqInput:
        for index, quantity in enumerate(word_frequency):
            arqInput.write(f"{index} {quantity}\n")
    print(word_length)
    end_time = time()
    print(str(timedelta(seconds=end_time - start_time)))