from pathlib import Path
from PIL import Image

BACKGROUND_COLOR = (255, 255, 255, 255)
INPUT_PATH = Path("input.png")
OUTPUT_PATH = Path("output.png")


def build_complex(width: int, x: int, height: int, y: int) -> complex:
    real_part = (width - 1) / 2 - x
    imag_part = (height - 1) / 2 - y
    return complex(real_part, imag_part)


def main() -> None:
    input_image = Image.open(INPUT_PATH)
    width, height = input_image.size
    min_height = 0.0
    max_height = 0.0
    min_width = 0.0
    max_width = 0.0
    o = 3
    for x in range(width):
        for y in range(height):
            pixel_complex = build_complex(width, x, height, y)
            pixel_complex = pixel_complex**o
            if pixel_complex.real > max_width:
                max_width = pixel_complex.real
            if pixel_complex.real < min_width:
                min_width = pixel_complex.real
            if pixel_complex.imag > max_height:
                max_height = pixel_complex.imag
            if pixel_complex.imag < min_height:
                min_height = pixel_complex.imag
    new_height = int(max_height - min_height + 1)
    new_width = int(max_width - min_width + 1)
    complex_image = Image.new("RGBA", (new_width, new_height), BACKGROUND_COLOR)
    for x in range(width):
        for y in range(height):
            corIm = input_image.getpixel((x, y))
            if corIm is None:
                corIm = BACKGROUND_COLOR
            pixel_complex = build_complex(width, x, height, y)
            pixel_complex = pixel_complex**o
            new_x = int((new_width - 1) / 2 - pixel_complex.real)
            new_y = int((new_height - 1) / 2 - pixel_complex.imag)
            pixelIm = (new_x, new_y)
            complex_image.putpixel(pixelIm, corIm)
    complex_image.save(OUTPUT_PATH)


if __name__ == "__main__":
    main()
