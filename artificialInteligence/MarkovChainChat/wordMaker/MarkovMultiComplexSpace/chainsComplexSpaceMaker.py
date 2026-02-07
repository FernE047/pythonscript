import os

EMPTY_CHAR = "¨"

def rename_file(source_filename: str, destination_filename: str) -> None:
    with (
        open(source_filename, "r", encoding="utf-8") as source_file,
        open(destination_filename, "w", encoding="utf-8") as destination_file,
    ):
        content = source_file.read()
        destination_file.write(content)


def update_chain(filename: str, index: int, chain_element: str) -> None:
    update_chain_file(filename, index, chain_element)
    rename_file(filename, f"/{index:03d}.txt")


def update_chain_file(filename: str, index: int, chain_element: str) -> None:
    with open(f"{filename}/c.txt", "w", encoding="UTF-8") as file_write:
        if f"{index:03d}.txt" not in os.listdir(filename):
            file_write.write(f"{chain_element} 1\n")
            return
        with open(f"{filename}/c.txt", "r", encoding="UTF-8") as file_read:
            lines = file_read.readlines()
        element_found = False
        element_length = len(chain_element)
        for line in lines:
            if not line.strip():
                continue
            if line[:element_length] == chain_element:
                number = int(line[element_length + 1 :]) + 1
                file_write.write(f"{line[: element_length + 1]} {number}\n")
                element_found = True
            else:
                file_write.write(line)
        if not element_found:
            file_write.write(f"{chain_element} 1\n")


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
    with open(f"{filename}.txt", "r", encoding="UTF-8") as file:
        lines = file.readlines()
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
        for word_index, word in enumerate(words):
            word_length = len(word)
            previous_char = ""
            for char_index in range(word_length):
                current_char = word[char_index]
                if char_index == 0:
                    update_chain(
                        filename,
                        char_index,
                        " ".join([str(word_index), current_char]),
                    )
                    if word_length == 1:
                        update_chain(
                            filename,
                            char_index + 1,
                            " ".join([str(word_index), current_char, EMPTY_CHAR]),
                        )
                        break
                    else:
                        next_char = word[char_index + 1]
                        update_chain(
                            filename,
                            char_index + 1,
                            " ".join([str(word_index), current_char, next_char]),
                        )
                        previous_char = current_char
                    continue
                if word_length > 1:
                    try:
                        next_char = word[char_index + 1]
                    except IndexError:
                        next_char = EMPTY_CHAR
                    update_chain(
                        filename,
                        char_index + 1,
                        " ".join(
                            [
                                str(word_index),
                                previous_char,
                                current_char,
                                next_char,
                            ]
                        ),
                    )
                    if next_char == EMPTY_CHAR:
                        break
                previous_char = current_char
            print(word_length)
    with open(f"{filename}/c.txt", "w", encoding="UTF-8") as chain_frequency_file:
        for index, quantity in enumerate(word_frequency_map):
            chain_frequency_file.write(f"{index} {quantity}\n")


if __name__ == "__main__":
    main()
