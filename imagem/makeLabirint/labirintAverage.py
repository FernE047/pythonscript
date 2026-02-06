from PIL import Image
from os import listdir

WHITE = (255, 255, 255, 255)
LABYRINTH_FOLDER = "pureLabyrinth"


def main() -> None:
    white_count: list[int] = []
    black_count: list[int] = []
    for arq in listdir(LABYRINTH_FOLDER):
        image = Image.open(f"{LABYRINTH_FOLDER}/{arq}")
        width, height = image.size
        if width > 500:
            continue
        white_pixels = 0
        black_pixels = 0
        for x in range(1, width - 1):
            for y in range(1, height - 1):
                if image.getpixel((x, y)) == WHITE:
                    white_pixels += 1
                else:
                    black_pixels += 1
        white_count.append(white_pixels)
        black_count.append(black_pixels)
        image.close()


if __name__ == "__main__":
    main()
