from PIL import Image
from pathlib import Path

BACKGROUND_COLOR = (255, 255, 255, 255)
OUTPUT_IMAGE_NAME = Path("output")
OUTPUT_EXTENSION = ".png"

CoordData = tuple[int, int]
PixelData = tuple[int, ...]


def get_pixel(image: Image.Image, coord: CoordData) -> PixelData:
    pixel = image.getpixel(coord)
    if pixel is None:
        raise ValueError("Pixel not found")
    if isinstance(pixel, int):
        raise ValueError("Image is not in RGB mode")
    if isinstance(pixel, float):
        raise ValueError("Image is not in RGB mode")
    if len(pixel) < 4:
        raise ValueError("Image is not in RGB mode")
    return pixel


def open_image_as_rgba(image_path: Path) -> Image.Image:
    with Image.open(image_path) as image:
        image_in_memory = image.copy()
        if image.mode != "RGBA":
            return image_in_memory.convert("RGBA")
        return image_in_memory


def main() -> None:
    image = open_image_as_rgba(Path("input.png"))
    size = image.size
    width, height = size
    squashed_image = Image.new("RGBA", size, BACKGROUND_COLOR)
    current_x = 0
    current_y = 0
    current_color = get_pixel(image, (0, 0))

    for scan_y in range(0, height):
        for scan_x in range(0, width):
            scan_color = get_pixel(image, (scan_x, scan_y))
            if scan_color != current_color or scan_x == width - 1:
                squashed_image.putpixel((current_x, current_y), current_color)
                current_x += 1
                current_color = scan_color
        current_y += 1
        current_x = 0
    direction = f"_top_bottom_left_right{OUTPUT_EXTENSION}"
    file_path = OUTPUT_IMAGE_NAME.with_suffix(direction)
    print(file_path)
    squashed_image.save(file_path)
    squashed_image = Image.new("RGBA", size, BACKGROUND_COLOR)
    current_x = 0
    current_y = 0
    current_color = get_pixel(image, (0, 0))

    for scan_x in range(0, width):
        for scan_y in range(0, height):
            scan_color = get_pixel(image, (scan_x, scan_y))
            if scan_color != current_color or scan_y == height - 1:
                squashed_image.putpixel((current_x, current_y), current_color)
                current_y += 1
                current_color = scan_color
        current_x += 1
        current_y = 0
    direction = f"_left_right_top_bottom{OUTPUT_EXTENSION}"
    file_path = OUTPUT_IMAGE_NAME.with_suffix(direction)
    print(file_path)
    squashed_image.save(file_path)

    squashed_image = Image.new("RGBA", size, BACKGROUND_COLOR)
    current_x = width - 1
    current_y = 0
    current_color = get_pixel(image, (width - 1, 0))
    for scan_y in range(0, height):
        for scan_x in range(width - 1, -1, -1):
            scan_color = get_pixel(image, (scan_x, scan_y))
            if scan_color != current_color or scan_x == 0:
                squashed_image.putpixel((current_x, current_y), current_color)
                current_x -= 1
                current_color = scan_color
        current_y += 1
        current_x = width - 1
    direction = f"_top_bottom_right_left{OUTPUT_EXTENSION}"
    file_path = OUTPUT_IMAGE_NAME.with_suffix(direction)
    print(file_path)
    squashed_image.save(file_path)

    squashed_image = Image.new("RGBA", size, BACKGROUND_COLOR)
    current_x = 0
    current_y = height - 1
    current_color = get_pixel(image, (0, height - 1))
    for scan_x in range(0, width):
        for scan_y in range(height - 1, -1, -1):
            scan_color = get_pixel(image, (scan_x, scan_y))
            if scan_color != current_color or scan_y == 0:
                squashed_image.putpixel((current_x, current_y), current_color)
                current_y -= 1
                current_color = scan_color
        current_x += 1
        current_y = height - 1
    direction = f"_left_right_bottom_top{OUTPUT_EXTENSION}"
    file_path = OUTPUT_IMAGE_NAME.with_suffix(direction)
    print(file_path)
    squashed_image.save(file_path)


if __name__ == "__main__":
    main()
