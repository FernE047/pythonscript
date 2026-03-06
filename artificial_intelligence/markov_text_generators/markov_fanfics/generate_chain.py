from pathlib import Path
from time import time
from datetime import timedelta

EMPTY_CHAR = "¨"
OVERFLOWLIMIT = 50000
CHAINSIZE = 1
ALLOWED_CHARS = (".", "-", ",", "!", "?", "(", "—", ")", ":", "...", "..", "/", "/")
REPLACE_BY_QUOTE = ("“", "”", "'")
REPLACE_BY_SPACE = ("\n", "\t")


def rename_file(source_filename: Path, destination_filename: Path) -> None:
    with (
        open(source_filename, "r", encoding="utf-8") as source_file,
        open(destination_filename, "w", encoding="utf-8") as destination_file,
    ):
        content = source_file.read()
        destination_file.write(content)


def update_chain_file(keywords: list[str], is_title: bool) -> None:
    folder = Path("FanficAnime")
    if is_title:
        folder /= "chainTitle"
    else:
        folder /= "chainStory"
    folder /= f"{CHAINSIZE}"
    update_keyword_counts(keywords, folder)
    rename_file(folder / "c.txt", folder / "chain.txt")


def update_keyword_counts(keywords: list[str], directory: Path) -> None:
    with open(directory / "c.txt", "w", encoding="utf-8") as file_write:
        if "chain.txt" not in [f.name for f in directory.iterdir()]:
            for keyword in keywords:
                file_write.write(f"{keyword} 1\n")
            return
        with open(directory / "chain.txt", "r", encoding="utf-8") as file_read:
            lines = file_read.readlines()
        for line in lines:
            words = line.split()
            current_keyword = " ".join(words[:-1])
            while current_keyword in keywords:
                words[-1] = str(int(words[-1]) + 1)
                keywords.remove(current_keyword)
            file_write.write(f"{' '.join(words)}\n")
            if not keywords:
                break
        if keywords:
            for keyword in keywords:
                file_write.write(f"{keyword} 1\n")


def generate_word_chain(text: str) -> list[str]:
    for char in REPLACE_BY_SPACE:
        text = text.replace(char, " ")
    for char in REPLACE_BY_QUOTE:
        text = text.replace(char, '"')
    for char in ALLOWED_CHARS:
        text = text.replace(char, f" {char} ")
    words = text.split()
    text_word_count = len(words)
    word_combinations: list[str] = []
    phrase_chunk = " ".join([EMPTY_CHAR for _ in range(CHAINSIZE)] + [words[0]])
    word_combinations.append(phrase_chunk)
    for n in range(text_word_count):
        phrase_segment = words[n : n + CHAINSIZE + 1]
        if len(phrase_segment) <= CHAINSIZE:
            while len(phrase_segment) <= CHAINSIZE:
                phrase_segment.append(EMPTY_CHAR)
            phrase_chunk = " ".join(phrase_segment)
            word_combinations.append(phrase_chunk)
            break
        phrase_chunk = " ".join(phrase_segment)
        word_combinations.append(phrase_chunk)
    return word_combinations


def generate_markov_chain() -> None:
    title_keywords: list[str] = []
    story_keywords: list[str] = []
    stories_folder = Path("FanficAnime") / "stories"
    filenames = list(stories_folder.iterdir())
    total = len(filenames)
    quantity = 0
    start_time = time()
    for name in filenames:
        file_path = stories_folder / name
        quantity += 1
        with open(file_path, "r", encoding="utf-8") as file:
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
            print(f"duração média : {timedelta(seconds=elapsed_time)}")
            print(f"tempo Passado : {timedelta(seconds=finish_time - start_time)}")
            print(f"falta : {timedelta(seconds=elapsed_time * (total - quantity))}")
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
        print(f"falta : {timedelta(seconds=elapsed_time * (total - quantity))}")
    print()
