import os
from time import time


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


def rename_file(source_file_name: str, destination_file_name: str) -> None:
    with (
        open(source_file_name, "r", encoding="utf-8") as source_file,
        open(destination_file_name, "w", encoding="utf-8") as destination_file,
    ):
        content = source_file.read()
        destination_file.write(content)


def update_chain_file(keywords: list[str], is_title: bool) -> None:
    if is_title:
        directory = f"./FanficAnime/chainTitle/{TAMANHO}"
    else:
        directory = f"./FanficAnime/chainStory/{TAMANHO}"
    update_keyword_counts(keywords, directory)
    rename_file(f"{directory}/c.txt", f"{directory}/chain.txt")


def update_keyword_counts(
    keywords: list[str], directory: str
) -> None:
    with open(f"{directory}/c.txt", "w", encoding="utf-8") as file_write:
        if "chain.txt" not in os.listdir(directory):
            for keyword in keywords:
                file_write.write(f"{keyword} 1\n")
            return
        with open(f"{directory}/chain.txt", "r", encoding="utf-8") as file_read:
            line = file_read.readline()
            while line:
                words = line.split()
                current_keyword = " ".join(words[:-1])
                while current_keyword in keywords:
                    words[-1] = str(int(words[-1]) + 1)
                    keywords.remove(current_keyword)
                file_write.write(" ".join(words) + "\n")
                if not keywords:
                    break
                line = file_read.readline()
        if keywords:
            for keyword in keywords:
                file_write.write(f"{keyword} 1\n")


def generate_word_chain(text: str) -> list[str]:
    text = text.replace("\n", " ")
    text = text.replace("\t", " ")
    text = text.replace("“", '"')
    text = text.replace("”", '"')
    for spaced in [".", "-", ",", "!", "?", "(", "—", ")", ":", "...", "..", "/", "/"]:
        text = text.replace(spaced, f" {spaced} ")
    words = text.split()
    text_word_count = len(words)
    word_combinations: list[str] = []
    phrase_chunk = " ".join(["¨" for _ in range(TAMANHO)] + [words[0]])
    word_combinations.append(phrase_chunk)
    for n in range(text_word_count):
        phrase_segment = words[n : n + TAMANHO + 1]
        if len(phrase_segment) <= TAMANHO:
            while len(phrase_segment) <= TAMANHO:
                phrase_segment.append("¨")
            phrase_chunk = " ".join(phrase_segment)
            word_combinations.append(phrase_chunk)
            break
        phrase_chunk = " ".join(phrase_segment)
        word_combinations.append(phrase_chunk)
    return word_combinations


OVERFLOWLIMIT = 50000
TAMANHO = 1
title_keywords: list[str] = []
story_keywords: list[str] = []
file_names = os.listdir("./FanficAnime/stories")
total = len(file_names)
quantity = 0
start_time = time()
for name in file_names:
    quantity += 1
    with open(f"./FanficAnime/stories/{name}", "r", encoding="utf-8") as file:
        story_components = file.readline().split(" : ")
        if story_components[:-1]:
            titulo = " : ".join(story_components[:-1])
            title_keywords += generate_word_chain(titulo)
        if story_components[-1:][0]:
            historia = story_components[-1:][0]
            story_keywords += generate_word_chain(historia)
    if len(story_keywords) > OVERFLOWLIMIT:
        update_chain_file(title_keywords, True)
        title_keywords = []
        update_chain_file(story_keywords, False)
        story_keywords = []
        finish_time = time()
        elapsed_time = (finish_time - start_time) / quantity
        print(name)
        print("duração média : " + format_elapsed_time(elapsed_time))
        print("tempo Passado : " + format_elapsed_time(finish_time - start_time))
        print("falta : " + format_elapsed_time(elapsed_time * (total - quantity)))
        print()
print("concluindo...")
if len(title_keywords) > OVERFLOWLIMIT:
    update_chain_file(title_keywords, True)
    title_keywords = []
if len(story_keywords) > OVERFLOWLIMIT:
    update_chain_file(story_keywords, False)
    story_keywords = []
    finish_time = time()
    elapsed_time = (finish_time - start_time) / total
    print("falta : " + format_elapsed_time(elapsed_time * (total - quantity)))
print()
