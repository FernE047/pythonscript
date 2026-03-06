from collections import Counter
from pathlib import Path
from time import time
from datetime import timedelta

AlterationsData = dict[int, list[list[str]]]

EMPTY_CHAR = "¨"


def rename_file(source_filename: Path, destination_filename: Path) -> None:
    with (
        open(source_filename, "r", encoding="utf-8") as source_file,
        open(destination_filename, "w", encoding="utf-8") as destination_file,
    ):
        content = source_file.read()
        destination_file.write(content)


def update_chain(filename: Path, index: int, chain_element: list[list[str]]) -> None:
    update_chain_file(filename, index, chain_element)
    rename_file(filename / "c.txt", filename / f"{index:03d}.txt")


def update_chain_file(
    filename: Path, index: int, chain_element: list[list[str]]
) -> None:
    with open(filename / "c.txt", "w", encoding="UTF-8") as file_write:
        counter = Counter([str(a) for a in chain_element])
        if not any(f"{index:03d}.txt" == file.name for file in filename.iterdir()):
            unique_terms: list[list[str]] = []
            for term in chain_element:
                if term not in unique_terms:
                    file_write.write(f"{' '.join(term + [str(counter[str(term)])])}\n")
                    unique_terms.append(term)
                    return
        with open(filename / f"{index:03d}.txt", "r", encoding="UTF-8") as file_read:
            lines = file_read.readlines()
        for line in lines:
            if not line.strip():
                continue
            words = line.split()
            terms = words[:-1]
            if terms in chain_element:
                frequency = int(words[-1])
                frequency += counter[str(terms)]
                while terms in chain_element:
                    chain_element.remove(terms)
                words[-1] = str(frequency)
                file_write.write(f"{' '.join(words)}\n")
            else:
                file_write.write(f"{' '.join(line.split())}\n")
        unique_terms = []
        for term in chain_element:
            if term not in unique_terms:
                file_write.write(f"{' '.join(term + [str(counter[str(term)])])}\n")
                unique_terms.append(term)


def update_chain_files(filename: Path, alterations: AlterationsData) -> None:
    for index in alterations:
        update_chain(filename, index, alterations[index])


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
    count = 0
    alterations: AlterationsData = {}
    for line in lines:
        line = line.strip()
        if not line:
            continue
        line = line[1:]
        if not line:
            continue
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
                    next_char = EMPTY_CHAR
                if char_index + 1 not in alterations:
                    alterations[char_index + 1] = [[current_char, next_char]]
                else:
                    alterations[char_index + 1].append([current_char, next_char])
                if next_char == EMPTY_CHAR:
                    break
        if count == 100:
            update_chain_files(filename, alterations)
            alterations = {}
            count = 0
        print(line_length)
    update_chain_files(filename, alterations)
    end_time = time()
    print(f"\nElapsed time: {str(timedelta(seconds=end_time - start_time))}\n\n\n")