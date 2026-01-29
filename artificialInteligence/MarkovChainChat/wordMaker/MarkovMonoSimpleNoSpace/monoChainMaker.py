import os
from time import time
from typing import cast

ChainData = tuple[str, str]


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


def update_chain_file(file_name: str, chain_terms: list[ChainData]) -> None:
    update_chain_file_contents(file_name, chain_terms)
    rename_file(f"{file_name}//c.txt", f"{file_name}//chain.txt")


def update_chain_file_contents(file_name: str, chain_terms: list[ChainData]) -> None:
    with open(f"{file_name}//c.txt", "w", encoding="UTF-8") as file_write:
        def write_terms(terms: ChainData, frequency: int) -> None:
            terms_flat = " ".join(terms)
            file_write.write(f"{terms_flat} {frequency}\n")

        if "chain.txt" not in os.listdir(file_name):
            for terms in chain_terms:
                write_terms(terms, 1)
            return
        with open(f"{file_name}//chain.txt", "r", encoding="UTF-8") as file_read:
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
start_time = time()
with open(f"{file_name}.txt", "r", encoding="UTF-8") as file:
    line = file.readline()[1:-1]
    line_length = len(line)
    while line:
        line_length = len(line)
        update_chain_values: list[ChainData] = []
        for n in range(line_length):
            current_character = line[n]
            if n == 0:
                update_chain_values.append(("¨", current_character))
                if line_length == 1:
                    update_chain_values.append((current_character, "¨"))
                    break
            if line_length > 1:
                if n >= line_length - 1:
                    next_character = "¨"
                else:
                    next_character = line[n + 1]
                update_chain_values.append((current_character, next_character))
                if next_character == "¨":
                    break
        update_chain_file(file_name, update_chain_values)
        line = file.readline()[:-1]
    print(line_length)
    end_time = time()
    print_elapsed_time(end_time - start_time)
