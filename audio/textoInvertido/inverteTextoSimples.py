from gtts import gTTS  # type: ignore


def fazAudio(file_name: str, text: str) -> None:
    tts = gTTS(text=text, lang="pt")  # type: ignore
    tts.save(f"{file_name}.mp3")  # type: ignore


def reverse_word_by_word(original_text: str) -> str:
    reversed_words: list[str] = []
    for line in original_text.split("\n"):
        for word in line.split(" "):
            reversed_words.append(reverse_word(word))
        reversed_words.append("\n")
    reversed_text = " ".join(reversed_words)
    return reversed_text


def reverse_word_by_word_no_line(original_text: str) -> str:
    reversed_words: list[str] = []
    for word in original_text.split(" "):
        reversed_words += [reverse_word(word)]
    reversed_text = " ".join(reversed_words)
    fazAudio("reversed_by_word", reversed_text)
    return reversed_text


def reverse_word(original_text: str) -> str:
    reversed_word = ""
    chars = list(original_text)
    for char in reversed(chars):
        reversed_word += char
    return reversed_word


def main() -> None:
    while True:
        file_name = input("enter the file name to save audio or press enter to skip:")
        original_text = input("enter the text to be inverted or press enter to exit:")
        if not original_text:
            break
        print("simple :\n")
        reversed_text = reverse_word(original_text)
        if file_name:
            fazAudio(f"{file_name}_reversed", reversed_text)
        print(reversed_text)
        print("\nword by word:\n")
        reversed_by_word = reverse_word_by_word(original_text)
        if file_name:
            fazAudio(f"{file_name}_reversed_by_word", reversed_by_word)
        print(reversed_by_word)


if __name__ == "__main__":
    main()
