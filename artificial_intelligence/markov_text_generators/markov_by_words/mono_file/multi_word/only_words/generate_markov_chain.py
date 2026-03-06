from pathlib import Path
from time import time
from typing import cast
from datetime import timedelta

ChainData = tuple[str, str]

EMPTY_CHAR = "¨"


def rename_file(source_filename: Path, destination_filename: Path) -> None:
    with (
        open(source_filename, "r", encoding="utf-8") as source_file,
        open(destination_filename, "w", encoding="utf-8") as destination_file,
    ):
        content = source_file.read()
        destination_file.write(content)


def update_chain_file(folder: Path, chain_terms: list[ChainData]) -> None:
    update_chain_file_contents(folder, chain_terms)
    rename_file(folder / "c.txt", folder / "chain.txt")


def update_chain_file_contents(folder: Path, chain_terms: list[ChainData]) -> None:
    with open(folder / "c.txt", "w", encoding="UTF-8") as file_write:

        def write_terms(terms: ChainData, frequency: int) -> None:
            terms_flat = " ".join(terms)
            file_write.write(f"{terms_flat} {frequency}\n")

        if not any("chain.txt" == file.name for file in folder.iterdir()):
            for terms in chain_terms:
                write_terms(terms, 1)
            return
        with open(folder / "chain.txt", "r", encoding="UTF-8") as file_read:
            lines = file_read.readlines()
        for line in lines:
            if not line.strip():
                continue
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


def get_filename() -> Path:
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
    filename = get_filename()
    start_time = time()
    with open(filename.with_suffix(".txt"), "r", encoding="UTF-8") as file:
        lines = file.readlines()
    line_length = 0
    for line in lines:
        if not line.strip():
            continue
        line_length = len(line)
        if line_length == 0:
            continue
        line = line[1:]
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
    print(line_length)
    end_time = time()
    print(f"\nElapsed time: {str(timedelta(seconds=end_time - start_time))}\n\n\n")
