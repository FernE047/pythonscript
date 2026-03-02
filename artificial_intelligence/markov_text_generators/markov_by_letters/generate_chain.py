import os

EMPTY_CHAR = "¨"


def rename_file(source_filename: str, destination_filename: str) -> None:
    with (
        open(source_filename, "r", encoding="utf-8") as source_file,
        open(destination_filename, "w", encoding="utf-8") as destination_file,
    ):
        content = source_file.read()
        destination_file.write(content)


def update_term_count(index: int, keyword: str) -> None:
    with open("chain/c.txt", "w", encoding="utf-8") as file_write:
        if f"{index:03d}.txt" not in os.listdir("chain"):
            file_write.write(f"{keyword} 1\n")
            return
        with open(f"chain/{index:03d}.txt", "r", encoding="utf-8") as file_read:
            lines = file_read.readlines()
        keyword_found = False
        index = len(keyword)
        for line in lines:
            if not line:
                continue
            if line[:index] == keyword:
                count = int(line[index + 1 :]) + 1
                file_write.write(f"{line[: index + 1]}{count}\n")
                keyword_found = True
            else:
                file_write.write(line)
        if not keyword_found:
            file_write.write(f"{keyword} 1\n")


def update_chain_file(index: int, keyword: str) -> None:
    if keyword == "":
        print(index)
    update_term_count(index, keyword)
    rename_file("chain/c.txt", f"chain/{index:03d}.txt")


def main() -> None:
    with open("clean_input.txt", "r", encoding="utf-8") as file:
        file.readline()
        for message in file.readlines():
            message_length = len(message)
            for index in range(message_length):
                character = message[index]
                if index == 0:
                    if character == "\n":
                        character = EMPTY_CHAR
                    if character == "<":
                        character = "~"
                        update_chain_file(index, character)
                        update_chain_file(index + 1, f"{character} {EMPTY_CHAR}")
                        break
                    update_chain_file(index, character)
                if message_length > 1:
                    try:
                        next_character = message[index + 1]
                    except IndexError:
                        next_character = EMPTY_CHAR
                    if next_character == "\n":
                        next_character = EMPTY_CHAR
                    update_chain_file(index + 1, f"{character} {next_character}")
                    if next_character == EMPTY_CHAR:
                        break


if __name__ == "__main__":
    main()
