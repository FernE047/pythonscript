from pathlib import Path
from PIL import Image

RED = (255, 0, 0, 255)
BLACK = (0, 0, 0, 255)
DATA_FOLDER = Path("data")


def generate_image(lyrics: str) -> Image.Image | None:
    words = lyrics.split(" ")
    word_counter = len(words)
    print(f"Word Count: {word_counter}\n")
    if not word_counter:
        print("No lyrics found\n")
        return None
    image = Image.new("RGBA", (word_counter, word_counter), BLACK)
    for x in range(word_counter):
        for y in range(word_counter):
            if words[x] == words[y]:
                image.putpixel((x, y), RED)
    return image


def main() -> None:
    lyrics_folder = DATA_FOLDER / "lyrics"
    image_folder = DATA_FOLDER / "images"
    image_folder.mkdir(exist_ok=True)
    for filename in lyrics_folder.iterdir():
        if not filename.name.endswith(".txt"):
            continue
        full_path = lyrics_folder / filename
        with open(full_path, "r", encoding="utf-8") as f:
            lyrics = f.read()
        image = generate_image(lyrics)
        if image is not None:
            image_path = image_folder / f"{filename.stem}.png"
            image.save(image_path)


if __name__ == "__main__":
    main()
