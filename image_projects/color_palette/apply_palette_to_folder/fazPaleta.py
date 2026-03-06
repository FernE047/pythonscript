import math
from pathlib import Path
from PIL import Image

PALLETE_FOLDER = Path("paleta")
PALLETE_FOLDER.mkdir(exist_ok=True)
PALLETE_IMAGE = PALLETE_FOLDER / "paletaBW4.png"
MAX_BRIGHTNESS = 256
MAX_SIZE = math.ceil(math.sqrt(MAX_BRIGHTNESS))
TRANSPARENT = (0, 0, 0, 0)

def main() -> None:
    image = Image.new("RGBA", (MAX_SIZE, MAX_SIZE), TRANSPARENT)
    image.save(PALLETE_IMAGE)
    for x in range(MAX_BRIGHTNESS):
        y = int(x / MAX_SIZE)
        color_value = tuple([x for _ in range(3)] + [MAX_BRIGHTNESS])
        print(color_value)
        image.putpixel((x % MAX_SIZE, y), color_value)
    image.save(PALLETE_IMAGE)


if __name__ == "__main__":
    main()
