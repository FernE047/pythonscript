import os


def rename_file(source_filename: str, destination_filename: str) -> None:
    with (
        open(source_filename, "r", encoding="utf-8") as source_file,
        open(destination_filename, "w", encoding="utf-8") as destination_file,
    ):
        content = source_file.read()
        destination_file.write(content)


def update_mono_chain_file(keywords: list[str], is_title: bool) -> None:
    if is_title:
        directory = "monoChainTitle"
    else:
        directory = "monoChainStory"
    update_keyword_frequency(keywords, directory)
    rename_file(f"{directory}/c.txt", f"{directory}/chain.txt")


def update_keyword_frequency(keywords: list[str], directory: str) -> None:
    with open(f"{directory}/c.txt", "w", encoding="utf-8") as file_write:
        if "chain.txt" not in os.listdir(directory):
            file_write.write(" ".join(keywords) + " 1\n")
            return
        with open(f"{directory}/chain.txt", "r", encoding="utf-8") as file_read:
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


def generate_markov_chain(text: str, is_title: bool = False) -> None:
    words = text.split()
    length = len(words)
    for index in range(length):
        word = words[index]
        if index == 0:
            update_mono_chain_file(["¨", word], is_title)
            if length == 1:
                update_mono_chain_file([word, "¨"], is_title)
                return
        if length > 1:
            if index >= length - 1:
                next_word = "¨"
            else:
                next_word = words[index + 1]
            update_mono_chain_file([word, next_word], is_title)
            if next_word == "¨":
                return


def main() -> None:
    for name in os.listdir("stories"):
        print(name)
        with open(f"stories/{name}", "r", encoding="utf-8") as file:
            title_and_story_parts = file.readline().split(" : ")
            story = title_and_story_parts[-1:][0]
            title = " : ".join(title_and_story_parts[:-1])
            generate_markov_chain(title, is_title=True)
            generate_markov_chain(story)


if __name__ == "__main__":
    main()
