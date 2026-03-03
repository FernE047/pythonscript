from PIL import Image
import os

RED = (255, 0, 0, 255)
BLACK = (0, 0, 0, 255)

def generate_image(lyrics:str) -> Image.Image| None:
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
    lyrics_folder = "./data/lyrics/"
    image_folder = "./data/images/"
    if not os.path.exists(image_folder):
        os.makedirs(image_folder)
    for filename in os.listdir(lyrics_folder):
        if not filename.endswith(".txt"):
            continue
        full_path = os.path.join(lyrics_folder, filename)
        with open(full_path, "r", encoding="utf-8") as f:
            lyrics = f.read()
        image = generate_image(lyrics)
        if image is not None:
            image_path = os.path.join(image_folder, f"{filename[:-4]}.png")
            image.save(image_path)

if __name__ == "__main__":
    main()