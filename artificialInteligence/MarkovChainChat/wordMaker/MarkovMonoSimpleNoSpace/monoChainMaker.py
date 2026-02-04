import os
from time import time
from typing import cast

ChainData = tuple[str, str]

EMPTY_CHAR = "¨"

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


def rename_file(source_filename: str, destination_filename: str) -> None:
    with (
        open(source_filename, "r", encoding="utf-8") as source_file,
        open(destination_filename, "w", encoding="utf-8") as destination_file,
    ):
        content = source_file.read()
        destination_file.write(content)


def update_chain_file(filename: str, chain_terms: list[ChainData]) -> None:
    update_chain_file_contents(filename, chain_terms)
    rename_file(f"{filename}/c.txt", f"{filename}/chain.txt")


def update_chain_file_contents(filename: str, chain_terms: list[ChainData]) -> None:
    with open(f"{filename}/c.txt", "w", encoding="UTF-8") as file_write:

        def write_terms(terms: ChainData, frequency: int) -> None:
            terms_flat = " ".join(terms)
            file_write.write(f"{terms_flat} {frequency}\n")

        if "chain.txt" not in os.listdir(filename):
            for terms in chain_terms:
                write_terms(terms, 1)
            return
        with open(f"{filename}/chain.txt", "r", encoding="UTF-8") as file_read:
            line = file_read.readline()
            while line:
                term_list = cast(tuple[str, str, str], line.split())
                term_tuple = cast(ChainData, tuple(term_list[:-1]))
                if term_tuple not in chain_terms:
                    file_write.write(line)
                    line = file_read.readline()
                    continue
                frequency = int(term_list[-1])
                while term_tuple in chain_terms:
                    frequency += 1
                    chain_terms.remove(term_tuple)
                write_terms(term_tuple, frequency)
                line = file_read.readline()
            for terms in chain_terms:
                write_terms(terms, 1)


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
        line = file.readline()[1:-1]
        line_length = len(line)
        while line:
            line_length = len(line)
            update_chain_values: list[ChainData] = []
            for n in range(line_length):
                current_character = line[n]
                if n == 0:
                    update_chain_values.append((EMPTY_CHAR, current_character))
                    if line_length == 1:
                        update_chain_values.append((current_character, EMPTY_CHAR))
                        break
                if line_length > 1:
                    if n >= line_length - 1:
                        next_character = EMPTY_CHAR
                    else:
                        next_character = line[n + 1]
                    update_chain_values.append((current_character, next_character))
                    if next_character == EMPTY_CHAR:
                        break
            update_chain_file(filename, update_chain_values)
            line = file.readline()[:-1]
        print(line_length)
        end_time = time()
        print_elapsed_time(end_time - start_time)


if __name__ == "__main__":
    main()
