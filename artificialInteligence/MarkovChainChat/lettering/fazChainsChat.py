import os


def rename_file(source_file_name: str, destination_file_name: str) -> None:
    with open(source_file_name, "r", encoding="utf-8") as source_file, open(destination_file_name, "w", encoding="utf-8") as destination_file:
        content = source_file.read()
        destination_file.write(content)

def update_term_count(index: int, keyword: str) -> None:
    with open("chain/c.txt", "w", encoding="utf-8") as file_write:
        if f"{index:03d}.txt" not in os.listdir("chain"):
            file_write.write(keyword + " 1\n")
            return
        with open(f"chain/{index:03d}.txt", "r", encoding="utf-8") as file_read:
            line = file_read.readline()
            keyword_found = False
            index = len(keyword)
            while line:
                if line[:index] == keyword:
                    count = int(line[index + 1 :]) + 1
                    file_write.write(line[: index + 1] + str(count) + "\n")
                    keyword_found = True
                else:
                    file_write.write(line)
                line = file_read.readline()
            if not keyword_found:
                file_write.write(keyword + " 1\n")


def update_chain_file(index: int, keyword: str) -> None:
    if keyword == "":
        print(index)
    update_term_count(index, keyword)
    rename_file("chain/c.txt", f"chain/{index:03d}.txt")


with open("clean_input.txt", "r", encoding="utf-8") as file:
    file.readline()
    for message in file.readlines():
        message_length = len(message)
        for index in range(message_length):
            character = message[index]
            if index == 0:
                if character == "\n":
                    character = "¨"
                if character == "<":
                    character = "~"
                    update_chain_file(index, character)
                    update_chain_file(index + 1, character + " ¨")
                    break
                update_chain_file(index, character)
            if message_length > 1:
                try:
                    next_character = message[index + 1]
                except IndexError:
                    next_character = "¨"
                if next_character == "\n":
                    next_character = "¨"
                update_chain_file(index + 1, character + " " + next_character)
                if next_character == "¨":
                    break