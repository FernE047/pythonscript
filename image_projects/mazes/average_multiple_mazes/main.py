from pathlib import Path
from PIL import Image

WHITE = (255, 255, 255, 255)
MAZE_FOLDER = Path("pure_mazes")


def open_image_as_rgba(image_path: Path) -> Image.Image:
    with Image.open(image_path) as image:
        image_in_memory = image.copy()
        if image.mode != "RGBA":
            return image_in_memory.convert("RGBA")
        return image_in_memory


def main() -> None:
    white_count: list[int] = []
    black_count: list[int] = []
    for arq in MAZE_FOLDER.iterdir():
        image = open_image_as_rgba(arq)
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


if __name__ == "__main__":
    main()
