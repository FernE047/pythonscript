from time import time
import os

EMPTY_CHAR = "¨"

def format_elapsed_time(seconds: float) -> str:
    if seconds < 0:
        seconds = -seconds
        sign = "-"
    else:
        sign = ""
    total_ms = int(round(seconds * 1000))
    ms = total_ms % 1000
    total_s = total_ms // 1000
    s = total_s % 60
    total_min = total_s // 60
    m = total_min % 60
    total_h = total_min // 60
    h = total_h % 24
    d = total_h // 24
    parts: list[str] = []

    def add(value: int, singular: str, plural: str) -> None:
        if value:
            parts.append(f"{value} {singular if value == 1 else plural}")

    add(d, "day", "days")
    add(h, "hour", "hours")
    add(m, "minute", "minutes")
    add(s, "second", "seconds")
    if ms or not parts:
        parts.append(f"{ms} millisecond" if ms == 1 else f"{ms} milliseconds")
    return sign + ", ".join(parts)


def rename_file(source_filename: str, destination_filename: str) -> None:
    with (
        open(source_filename, "r", encoding="utf-8") as source_file,
        open(destination_filename, "w", encoding="utf-8") as destination_file,
    ):
        content = source_file.read()
        destination_file.write(content)


def update_chain_file(keywords: list[str], chain_size: int, is_title: bool) -> None:
    if is_title:
        directory = f"chainTitle//{chain_size}"
    else:
        directory = f"chainStory//{chain_size}"
    update_keyword_frequencies(keywords, directory)
    rename_file(f"{directory}//c.txt", f"{directory}//chain.txt")


def update_keyword_frequencies(keywords: list[str], directory: str) -> None:
    with open(f"{directory}//c.txt", "w", encoding="utf-8") as file_write:
        if "chain.txt" not in os.listdir(directory):
            for keyword in keywords:
                file_write.write(keyword + " 1\n")
            return
        with open(f"{directory}//chain.txt", "r", encoding="utf-8") as file_read:
            line = file_read.readline()
            while line:
                words = line.split()
                test_keyword = " ".join(words[:-1])
                while test_keyword in keywords:
                    words[-1] = str(int(words[-1]) + 1)
                    keywords.remove(test_keyword)
                file_write.write(" ".join(words) + "\n")
                line = file_read.readline()
        if keywords:
            for keyword in keywords:
                file_write.write(keyword + " 1\n")


def generate_markov_chain(text: str, chain_size: int, is_title: bool = False) -> None:
    text = text.replace("\n", " ")
    text = text.replace("\t", " ")
    text = text.replace("“", ' " ')
    text = text.replace("”", ' " ')
    for spaced in [".", "-", ",", "!", "?", "(", "—", ")", ":", "...", "..", "/", "\\"]:
        text = text.replace(spaced, f" {spaced} ")
    words = text.split()
    text_length = len(words)
    pair_list: list[str] = []
    word_combination = " ".join([EMPTY_CHAR for _ in range(chain_size)] + [words[0]])
    pair_list.append(word_combination)
    for index in range(text_length):
        terms = words[index : index + chain_size + 1]
        if len(terms) <= chain_size:
            while len(terms) <= chain_size:
                terms.append(EMPTY_CHAR)
            word_combination = " ".join(terms)
            pair_list.append(word_combination)
            break
        word_combination = " ".join(terms)
        pair_list.append(word_combination)
    update_chain_file(pair_list, chain_size, is_title)


def main() -> None:
    chain_size = 2
    total = len(os.listdir("stories"))
    for chain_size in range(2, 3):
        processed_file_count = 0
        for name in os.listdir("stories"):
            processed_file_count += 1
            start_time = time()
            print(name)
            with open(f"stories//{name}", "r", encoding="utf-8") as file:
                title_and_story_parts = file.readline().split(" : ")
                if title_and_story_parts[:-1]:
                    title = " : ".join(title_and_story_parts[:-1])
                    generate_markov_chain(title, chain_size, is_title=True)
                if title_and_story_parts[-1:][0]:
                    story = title_and_story_parts[-1:][0]
                    generate_markov_chain(story, chain_size)
            execution_end_time = time()
            duration = execution_end_time - start_time
            print(
                f"falta : {format_elapsed_time(duration * (total - processed_file_count))}"
            )
            print()


if __name__ == "__main__":
    main()
