import os
from collections import Counter
from time import time
from typing import cast

ChainData = tuple[str, str, str]


EMPTY_CHAR = "¨"


def format_elapsed_time(seconds: float) -> str:
    if seconds < 0:
        seconds = -seconds
        sign = "-"
    else:
        sign = ""
    total_ms = int(round(seconds * 1000))
    ms = total_ms % 1000
    total_s = total_ms // 1000
    s = total_s % 60
    total_min = total_s // 60
    m = total_min % 60
    total_h = total_min // 60
    h = total_h % 24
    d = total_h // 24
    parts: list[str] = []

    def add(value: int, singular: str, plural: str) -> None:
        if value:
            parts.append(f"{value} {singular if value == 1 else plural}")

    add(d, "day", "days")
    add(h, "hour", "hours")
    add(m, "minute", "minutes")
    add(s, "second", "seconds")
    if ms or not parts:
        parts.append(f"{ms} millisecond" if ms == 1 else f"{ms} milliseconds")
    return f"{sign}{', '.join(parts)}"


def rename_file(source_filename: str, destination_filename: str) -> None:
    with (
        open(source_filename, "r", encoding="utf-8") as source_file,
        open(destination_filename, "w", encoding="utf-8") as destination_file,
    ):
        content = source_file.read()
        destination_file.write(content)


def update_chain_file(filename: str, keywords: list[ChainData]) -> None:
    update_keywords_in_chain(filename, keywords)
    rename_file(f"{filename}/c.txt", f"{filename}/chain.txt")


def update_keywords_in_chain(filename: str, keyword_tuples: list[ChainData]) -> None:
    with open(f"{filename}/c.txt", "w", encoding="UTF-8") as file_write:
        counter = Counter([" ".join(keyword_tuple) for keyword_tuple in keyword_tuples])
        unique_keywords: set[ChainData] = set()
        if "chain.txt" not in os.listdir(filename):
            for keyword_tuple in keyword_tuples:
                if keyword_tuple not in unique_keywords:
                    keyword_tuple_flat = " ".join(keyword_tuple)
                    keyword_tuple_frequency = counter[keyword_tuple_flat]
                    file_write.write(
                        f"{keyword_tuple_flat} {keyword_tuple_frequency}\n"
                    )
                    unique_keywords.add(keyword_tuple)
            return
        with open(f"{filename}/chain.txt", "r", encoding="UTF-8") as file_read:
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
    start_time = time()
    with open(f"{filename}.txt", "r", encoding="UTF-8") as file:
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
            update_chain_file(filename, update_chain_values)
            update_chain_values = []
            count = 0
        else:
            count += 1
    update_chain_file(filename, update_chain_values)
    with open(f"{filename}/length.txt", "w", encoding="UTF-8") as arqInput:
        for index, quantity in enumerate(word_frequency):
            arqInput.write(f"{index} {quantity}\n")
    print(word_length)
    end_time = time()
    print(format_elapsed_time(end_time - start_time))


if __name__ == "__main__":
    main()
