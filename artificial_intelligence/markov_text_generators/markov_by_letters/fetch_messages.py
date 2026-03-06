from pathlib import Path
import re

INPUT_FOLDER = Path("in")
INPUT_FOLDER.mkdir(exist_ok=True)
INPUT_FILE = INPUT_FOLDER / "whatsapp_messages.txt"
CLEAN_INPUT_FILE = INPUT_FOLDER / "clean_messages.txt"
DATE_PATTERN = r"\[[0-2][0-9][:][0-5][0-9], [0-3][0-9][/][0-1][0-9][/]20[21][0-9]\]"
MESSAGE_SPLIT = ": "
DATE_PART_LENGTH = 19


def parse_messages(lines: list[str]) -> list[str]:
    messages: list[str] = []
    for line in lines:
        if len(line) == 0:
            continue
        elements = line.split(MESSAGE_SPLIT)
        if len(elements) < 2:
            continue
        date_test = elements[0][:DATE_PART_LENGTH]
        if not re.search(DATE_PATTERN, date_test):
            continue
        message = "".join(elements[1:]).strip()
        messages.append(message)
    return messages


def extract_and_save_messages() -> None:
    with open(INPUT_FILE, "r", encoding="utf-8") as input_file:
        lines = input_file.readlines()
    messages = parse_messages(lines)
    with open(CLEAN_INPUT_FILE, "w", encoding="utf-8") as output_file:
        for message in messages:
            output_file.write(f"{message}\n")
