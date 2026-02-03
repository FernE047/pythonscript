import os
from collections import Counter
from time import time

AlterationsData = dict[int, list[list[str]]]


def print_elapsed_time(seconds: float) -> None:
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
    print(sign + ", ".join(parts))


def rename_file(source_file_name: str, destination_file_name: str) -> None:
    with (
        open(source_file_name, "r", encoding="utf-8") as source_file,
        open(destination_file_name, "w", encoding="utf-8") as destination_file,
    ):
        content = source_file.read()
        destination_file.write(content)


def update_chain(file_name: str, index: int, chain_element: list[list[str]]) -> None:
    update_chain_file(file_name, index, chain_element)
    rename_file(file_name, f"/{index:03d}.txt")


def update_chain_file(
    file_name: str, index: int, chain_element: list[list[str]]
) -> None:
    with open(f"{file_name}/c.txt", "w", encoding="UTF-8") as file_write:
        counter = Counter([str(a) for a in chain_element])
        if f"{index:03d}.txt" not in os.listdir(file_name):
            unique_terms: list[list[str]] = []
            for term in chain_element:
                if term not in unique_terms:
                    file_write.write(" ".join(term + [str(counter[str(term)])]) + "\n")
                    unique_terms.append(term)
                    return
        with open(f"{file_name}/{index:03d}.txt", "r", encoding="UTF-8") as file_read:
            line = file_read.readline()[:-1]
            while line:
                words = line.split()
                terms = words[:-1]
                if terms in chain_element:
                    frequency = int(words[-1])
                    frequency += counter[str(terms)]
                    while terms in chain_element:
                        chain_element.remove(terms)
                    words[-1] = str(frequency)
                    file_write.write(" ".join(words) + "\n")
                else:
                    file_write.write(line + "\n")
                line = file_read.readline()[:-1]
            unique_terms = []
            for term in chain_element:
                if term not in unique_terms:
                    file_write.write(" ".join(term + [str(counter[str(term)])]) + "\n")
                    unique_terms.append(term)


def update_chain_files(file_name: str, alterations: AlterationsData) -> None:
    for index in alterations:
        update_chain(file_name, index, alterations[index])


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
        line = file.readline()[1:-1]
        count = 0
        alterations: AlterationsData = {}
        while line:
            count += 1
            line_length = len(line)
            for char_index, current_char in enumerate(line):
                if char_index == 0:
                    if char_index not in alterations:
                        alterations[char_index] = [[current_char]]
                    else:
                        alterations[char_index].append([current_char])
                if line_length > 1:
                    try:
                        next_char = line[char_index + 1]
                    except IndexError:
                        next_char = "¨"
                    if char_index + 1 not in alterations:
                        alterations[char_index + 1] = [[current_char, next_char]]
                    else:
                        alterations[char_index + 1].append([current_char, next_char])
                    if next_char == "¨":
                        break
            if count == 100:
                update_chain_files(file_name, alterations)
                alterations = {}
                count = 0
            print(line_length)
            line = file.readline()[:-1]
        update_chain_files(file_name, alterations)
        end_time = time()
        print_elapsed_time(end_time - start_time)


if __name__ == "__main__":
    main()
