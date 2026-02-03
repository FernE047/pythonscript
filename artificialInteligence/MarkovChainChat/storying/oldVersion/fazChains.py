import os


def rename_file(source_file_name: str, destination_file_name: str) -> None:
    with (
        open(source_file_name, "r", encoding="utf-8") as source_file,
        open(destination_file_name, "w", encoding="utf-8") as destination_file,
    ):
        content = source_file.read()
        destination_file.write(content)


def update_chain_file(index: int, keywords: list[str], is_title: bool) -> None:
    if is_title:
        directory = "chainTitle/0"
    else:
        directory = "chainStory/0"
    update_keyword_count(index, keywords, directory)
    rename_file(f"{directory}/c.txt", f"{directory}/{index:03d}.txt")


def update_keyword_count(index: int, keywords: list[str], directory: str) -> None:
    with open(f"{directory}/c.txt", "w", encoding="utf-8") as file_write:
        if f"{index:03d}.txt" not in os.listdir(directory):
            file_write.write(" ".join(keywords) + " 1\n")
            return
        with open(f"{directory}/{index:03d}.txt", "r", encoding="utf-8") as file_read:
            line = file_read.readline()
            keyword_found = False
            while line:
                words = line.split()
                if words[:-1] == keywords:
                    words[-1] = str(int(words[-1]) + 1)
                    file_write.write(" ".join(words) + "\n")
                    keyword_found = True
                else:
                    file_write.write(line)
                line = file_read.readline()
            if not keyword_found:
                file_write.write(" ".join(keywords) + " 1\n")


def faz_chain(text: str, is_title: bool = False) -> None:
    words = text.split()
    length = len(words)
    for n in range(length):
        word = words[n]
        if n == 0:
            update_chain_file(n, [word], is_title)
            if length == 1:
                update_chain_file(n + 1, [word, "¨"], is_title)
                return
        if length > 1:
            if n >= length - 1:
                next_word = "¨"
            else:
                next_word = words[n + 1]
            update_chain_file(n + 1, [word, next_word], is_title)
            if next_word == "¨":
                return


def main() -> None:
    for file_name in os.listdir("stories"):
        print(file_name)
        with open(f"stories/{file_name}", "r", encoding="utf-8") as file:
            title_and_story_parts = file.readline().split(" : ")
            story = title_and_story_parts[-1:][0]
            title = ": ".join(title_and_story_parts[:-1])
            faz_chain(title, is_title=True)
            faz_chain(story)


if __name__ == "__main__":
    main()
