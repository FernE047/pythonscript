import os


def rename_file(source_file_name: str, destination_file_name: str) -> None:
    with (
        open(source_file_name, "r", encoding="utf-8") as source_file,
        open(destination_file_name, "w", encoding="utf-8") as destination_file,
    ):
        content = source_file.read()
        destination_file.write(content)


def update_chain(file_name: str, index: int, chain_element: str) -> None:
    update_chain_file(file_name, index, chain_element)
    rename_file(file_name, f"/{index:03d}.txt")


def update_chain_file(file_name: str, index: int, chain_element: str) -> None:
    with open(f"{file_name}/c.txt", "w", encoding="UTF-8") as file_write:
        if f"{index:03d}.txt" not in os.listdir(file_name):
            file_write.write(f"{chain_element} 1\n")
            return
        with open(f"{file_name}/c.txt", "r", encoding="UTF-8") as file_read:
            line = file_read.readline()
            element_found = False
            element_length = len(chain_element)
            while line:
                if line[:element_length] == chain_element:
                    number = int(line[element_length + 1 :]) + 1
                    file_write.write(f"{line[: element_length + 1]} {number}\n")
                    element_found = True
                else:
                    file_write.write(line)
                line = file_read.readline()
            if not element_found:
                file_write.write(f"{chain_element} 1\n")


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
    with open(f"{file_name}.txt", "r", encoding="UTF-8") as file:
        line = file.readline()[1:-1]
        word_frequency_map: list[int] = []
        while line:
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
                            file_name,
                            char_index,
                            " ".join([str(word_index), current_char]),
                        )
                        if word_length == 1:
                            update_chain(
                                file_name,
                                char_index + 1,
                                " ".join([str(word_index), current_char, "¨"]),
                            )
                            break
                        else:
                            next_char = word[char_index + 1]
                            update_chain(
                                file_name,
                                char_index + 1,
                                " ".join([str(word_index), current_char, next_char]),
                            )
                            previous_char = current_char
                        continue
                    if word_length > 1:
                        try:
                            next_char = word[char_index + 1]
                        except IndexError:
                            next_char = "¨"
                        update_chain(
                            file_name,
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
                        if next_char == "¨":
                            break
                    previous_char = current_char
                print(word_length)
            line = file.readline()[:-1]
        with open(f"{file_name}/c.txt", "w", encoding="UTF-8") as chain_frequency_file:
            for index, quantity in enumerate(word_frequency_map):
                chain_frequency_file.write(f"{index} {quantity}\n")


if __name__ == "__main__":
    main()
