from collections import Counter
from pathlib import Path
from time import time
from datetime import timedelta

EMPTY_CHAR = "¨"


def rename_file(source_filename: Path, destination_filename: Path) -> None:
    with (
        open(source_filename, "r", encoding="utf-8") as source_file,
        open(destination_filename, "w", encoding="utf-8") as destination_file,
    ):
        content = source_file.read()
        destination_file.write(content)


def update_chain(folder: Path, file_index: int, terms: list[list[str]]) -> None:
    update_chain_file(folder, file_index, terms)
    rename_file(folder / "c.txt", folder / f"{file_index:03d}.txt")


def update_chain_file(folder: Path, file_index: int, terms: list[list[str]]) -> None:
    with open(folder / "c.txt", "w", encoding="UTF-8") as file_write:
        counter = Counter([str(a) for a in terms])
        if not any(f"{file_index:03d}.txt" == file.name for file in folder.iterdir()):
            unique_terms: list[list[str]] = []
            for term in terms:
                if term not in unique_terms:
                    file_write.write(f"{' '.join(term + [str(counter[str(term)])])}\n")
                    unique_terms.append(term)
            return
        with open(
            folder / f"{file_index:03d}.txt", "r", encoding="UTF-8"
        ) as file_read:
            lines = file_read.readlines()[:-1]
        for line in lines:
            if not line.strip():
                continue
            words = line.split()
            if words[:-1] in terms:
                frequency = int(words[-1])
                frequency += counter[str(words[:-1])]
                while words[:-1] in terms:
                    terms.remove(words[:-1])
                words[-1] = str(frequency)
                file_write.write(f"{' '.join(words)}\n")
            else:
                file_write.write(f"{' '.join(line.split())}\n")
        unique_terms = []
        for term in terms:
            if term not in unique_terms:
                file_write.write(f"{' '.join(term + [str(counter[str(term)])])}\n")
                unique_terms.append(term)


def update_chain_files(folder: Path, alterations: dict[int, list[list[str]]]) -> None:
    for file_index in alterations:
        update_chain(folder, file_index, alterations[file_index])


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
    folder = get_filename()
    start_time = time()
    with open(folder.with_suffix(".txt"), "r", encoding="UTF-8") as file:
        lines = file.readlines()
    count = 0
    alterations: dict[int, list[list[str]]] = {}
    word_frequency_map: list[int] = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if len(line) == 0:
            continue
        line = line[1:]
        words = line.split()
        while len(words) > len(word_frequency_map):
            word_frequency_map.append(0)
        word_frequency_map[len(words) - 1] += 1
        for word in words:
            word_length = len(word)
            previous_char = ""
            for char_index in range(word_length):
                current_char = word[char_index]
                if char_index == 0:
                    if char_index not in alterations:
                        alterations[char_index] = [[current_char]]
                    else:
                        alterations[char_index].append([current_char])
                    if word_length == 1:
                        if char_index + 1 not in alterations:
                            alterations[char_index + 1] = [[current_char, EMPTY_CHAR]]
                        else:
                            alterations[char_index + 1].append([current_char, EMPTY_CHAR])
                        break
                    else:
                        next_char = word[char_index + 1]
                        if char_index + 1 not in alterations:
                            alterations[char_index + 1] = [
                                [current_char, next_char]
                            ]
                        else:
                            alterations[char_index + 1].append(
                                [current_char, next_char]
                            )
                        previous_char = current_char
                    continue
                if word_length > 1:
                    try:
                        next_char = word[char_index + 1]
                    except IndexError:
                        next_char = EMPTY_CHAR
                    if char_index + 1 not in alterations:
                        alterations[char_index + 1] = [
                            [previous_char, current_char, next_char]
                        ]
                    else:
                        alterations[char_index + 1].append(
                            [previous_char, current_char, next_char]
                        )
                    if next_char == EMPTY_CHAR:
                        break
                previous_char = current_char
                print(word_length)
        if count == 100:
            update_chain_files(folder, alterations)
            alterations = {}
            count = 0
        else:
            count += 1
    update_chain_files(folder, alterations)
    with open(folder / "c.txt", "w", encoding="UTF-8") as word_count_file:
        for index, quantity in enumerate(word_frequency_map):
            word_count_file.write(f"{index} ")
            word_count_file.write(f"{quantity}\n")
    end_time = time()
    print(f"\nElapsed time: {str(timedelta(seconds=end_time - start_time))}\n\n\n")