import os


def rename_file(source_file_name: str, destination_file_name: str) -> None:
    with (
        open(source_file_name, "r", encoding="utf-8") as source_file,
        open(destination_file_name, "w", encoding="utf-8") as destination_file,
    ):
        content = source_file.read()
        destination_file.write(content)


def update_chain_file(index: int, keywords: list[str]) -> None:
    update_keyword_count(index, keywords)
    rename_file("chain//c.txt", f"chain//{index:03d}.txt")


def update_keyword_count(index: int, keywords: list[str]) -> None:
    with open("chain//c.txt", "w", encoding="utf-8") as file_write:
        if f"{index:03d}.txt" not in os.listdir("chain"):
            file_write.write(" ".join(keywords) + " 1\n")
            return
        with open(f"chain//{index:03d}.txt", "r", encoding="utf-8") as file_read:
            line = file_read.readline()
            keyword_exists = False
            while line:
                words = line.split()
                if words[:-1] == keywords:
                    words[-1] = str(int(words[-1]) + 1)
                    file_write.write(" ".join(words) + "\n")
                    keyword_exists = True
                else:
                    file_write.write(line)
                line = file_read.readline()
            if not keyword_exists:
                file_write.write(" ".join(keywords) + " 1\n")


def main() -> None:
    with open("sohMensagens.txt", "r", encoding="utf-8") as file:
        message = file.readline()
        while message:
            words = message.split()
            word_count = len(words)
            for index, word in enumerate(words):
                if index == 0:
                    update_chain_file(index, [word])
                    if word_count == 1:
                        update_chain_file(index + 1, [word, "¨"])
                        break
                if word_count > 1:
                    if index >= word_count - 1:
                        next_word = "¨"
                    else:
                        next_word = words[index + 1]
                    update_chain_file(index + 1, [word, next_word])
                    if next_word == "¨":
                        break
            message = file.readline()


if __name__ == "__main__":
    main()
