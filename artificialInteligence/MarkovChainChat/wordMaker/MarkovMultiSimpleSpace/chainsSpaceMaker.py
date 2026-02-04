import os


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
            file_write.write(chain_element + " 1\n")
            return
        with open(f"{filename}/{index:03d}.txt", "r", encoding="UTF-8") as file_read:
            line = file_read.readline()
            element_found = False
            element_index = len(chain_element)
            while line:
                if line[:element_index] == chain_element:
                    frequency = int(line[element_index + 1 :]) + 1
                    file_write.write(f"{line[: element_index + 1]} {frequency}\n")
                    element_found = True
                else:
                    file_write.write(line)
                line = file_read.readline()
            if not element_found:
                file_write.write(chain_element + " 1\n")


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
        line = file.readline()[1:-1]
        word_frequency_map: list[int] = []
        while line:
            words = line.split()
            while len(words) > len(word_frequency_map):
                word_frequency_map.append(0)
            word_frequency_map[len(words) - 1] += 1
            for word_index, word in enumerate(words):
                word_length = len(word)
                for chair_index in range(word_length):
                    current_char = word[chair_index]
                    if chair_index == 0:
                        """if current_char == "\n":
                            current_char = "¨" """
                        update_chain(
                            filename,
                            chair_index,
                            " ".join([str(word_index), current_char]),
                        )
                        if word_length == 1:
                            update_chain(
                                filename,
                                chair_index + 1,
                                " ".join([str(word_index), current_char, "¨"]),
                            )
                    if word_length > 1:
                        try:
                            next_char = word[chair_index + 1]
                        except IndexError:
                            next_char = "¨"
                        if next_char == "\n":
                            next_char = "¨"
                        update_chain(
                            filename,
                            chair_index + 1,
                            " ".join([str(word_index), current_char, next_char]),
                        )
                        if next_char == "¨":
                            break
                print(word_length)
            line = file.readline()[:-1]
        with open(filename + "/c.txt", "w", encoding="UTF-8") as output_chain_file:
            for index, quantity in enumerate(word_frequency_map):
                output_chain_file.write(f"{index} {quantity}\n")


if __name__ == "__main__":
    main()
