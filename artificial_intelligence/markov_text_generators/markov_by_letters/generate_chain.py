from pathlib import Path
from fetch_messages import CLEAN_INPUT_FILE

EMPTY_CHAR = "¨"
INPUT_FILE = CLEAN_INPUT_FILE
CHAIN_FOLDER = Path("chain")


def is_chain_file_empty(index: int) -> bool:
    for file in CHAIN_FOLDER.iterdir():
        if f"{index:03d}.txt" == file.name:
            return False
    return True


def update_chain_file(index: int, keyword: str) -> None:
    chain_path = CHAIN_FOLDER / f"{index:03d}.txt"
    if is_chain_file_empty(index):
        with open(chain_path, "w", encoding="utf-8") as file_write:
            file_write.write(f"{keyword} 1\n")
            return
    with open(chain_path, "r", encoding="utf-8") as file_read:
        lines = file_read.readlines()
    new_lines = update_keyword_count(keyword, lines)
    with open(chain_path, "w", encoding="utf-8") as file_write:
        file_write.writelines(new_lines)


def update_keyword_count(keyword: str, lines: list[str]) -> list[str]:
    keyword_found = False
    index = len(keyword)
    new_lines: list[str] = []
    for line in lines:
        if not line:
            continue
        if line[:index] != keyword:
            new_lines.append(line)
            continue
        count = int(line[index + 1 :]) + 1
        new_lines.append(f"{line[: index + 1]}{count}\n")
        keyword_found = True
    if not keyword_found:
        new_lines.append(f"{keyword} 1\n")
    return new_lines


def process_message(message: str, index: int) -> None:
    message_length = len(message)
    if index >= message_length:
        return
    character = message[index]
    if character == "\n":
        return
    if index == 0:
        update_chain_file(index, character)
    if message_length >= 1:
        try:
            next_character = message[index + 1]
        except IndexError:
            next_character = EMPTY_CHAR
        if next_character == "\n":
            next_character = EMPTY_CHAR
        update_chain_file(index + 1, f"{character} {next_character}")


def generate_character_chain() -> None:
    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        lines = [line.strip() for line in file.readlines()]
    for message in lines:
        message_length = len(message)
        for index in range(message_length):
            process_message(message, index)