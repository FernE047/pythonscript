import os
from collections import Counter
from time import time
from typing import cast

ChainData = tuple[str, str, str]


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
    return sign + ", ".join(parts)


def rename_file(source_file_name: str, destination_file_name: str) -> None:
    with (
        open(source_file_name, "r", encoding="utf-8") as source_file,
        open(destination_file_name, "w", encoding="utf-8") as destination_file,
    ):
        content = source_file.read()
        destination_file.write(content)


def update_chain_file(file_name: str, keywords: list[ChainData]) -> None:
    update_keywords_in_chain(file_name, keywords)
    rename_file(f"{file_name}/c.txt", f"{file_name}/chain.txt")


def update_keywords_in_chain(file_name: str, keyword_tuples: list[ChainData]) -> None:
    with open(f"{file_name}/c.txt", "w", encoding="UTF-8") as file_write:
        counter = Counter([" ".join(keyword_tuple) for keyword_tuple in keyword_tuples])
        unique_keywords: set[ChainData] = set()
        if "chain.txt" not in os.listdir(file_name):
            for keyword_tuple in keyword_tuples:
                if keyword_tuple not in unique_keywords:
                    keyword_tuple_flat = " ".join(keyword_tuple)
                    keyword_tuple_frequency = counter[keyword_tuple_flat]
                    file_write.write(
                        f"{keyword_tuple_flat} {keyword_tuple_frequency}\n"
                    )
                    unique_keywords.add(keyword_tuple)
            return
        with open(f"{file_name}/chain.txt", "r", encoding="UTF-8") as file_read:
            line = file_read.readline()
            while line:
                keywords_read = cast(tuple[str, str, str, str], tuple(line.split()))
                keyword_tuple = cast(ChainData, tuple(keywords_read[:-1]))
                if keyword_tuple not in keyword_tuples:
                    file_write.write(line)
                    line = file_read.readline()
                    continue
                frequency = int(keywords_read[-1])
                keyword_tuple_flat = " ".join(keyword_tuple)
                frequency += counter[keyword_tuple_flat]
                while keyword_tuple in keyword_tuples:
                    keyword_tuples.remove(keyword_tuple)
                file_write.write(f"{keyword_tuple_flat} {frequency}\n")
                line = file_read.readline()
            for keyword_tuple in keyword_tuples:
                if keyword_tuple not in unique_keywords:
                    keyword_tuple_flat = " ".join(keyword_tuple)
                    frequency = counter[keyword_tuple_flat]
                    file_write.write(f"{keyword_tuple_flat} {frequency}\n")
                    unique_keywords.add(keyword_tuple)


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


def main() -> None:
    file_name = get_file_name()
    start_time = time()
    with open(f"{file_name}.txt", "r", encoding="UTF-8") as file:
        line = file.readline()[:-1]
        word_frequency: list[int] = []
        word_length = 0
        count = 0
        update_chain_values: list[ChainData] = []
        while line:
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
                        update_chain_values.append(("¨", "¨", current_character))
                        if word_length == 1:
                            update_chain_values.append(("¨", current_character, "¨"))
                            break
                        else:
                            next_character = word[index + 1]
                            update_chain_values.append(
                                ("¨", current_character, next_character)
                            )
                            previous_character = current_character
                        continue
                    if word_length > 1:
                        if index >= word_length - 1:
                            next_character = "¨"
                        else:
                            next_character = word[index + 1]
                        update_chain_values.append(
                            (previous_character, current_character, next_character)
                        )
                        if next_character == "¨":
                            break
                    previous_character = current_character
            if count == 100:
                update_chain_file(file_name, update_chain_values)
                update_chain_values = []
                count = 0
            else:
                count += 1
            line = file.readline()[:-1]
        update_chain_file(file_name, update_chain_values)
        with open(f"{file_name}/length.txt", "w", encoding="UTF-8") as arqInput:
            for index, quantity in enumerate(word_frequency):
                arqInput.write(f"{index} {quantity}\n")
        print(word_length)
        end_time = time()
        print(format_elapsed_time(end_time - start_time))


if __name__ == "__main__":
    main()
