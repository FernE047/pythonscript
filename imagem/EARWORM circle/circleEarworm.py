import os
from PIL import Image
import math

MUSIC_FOLDER = "./musicas/"
OUTPUT_FOLDER = "./circle/"
DEFAULT_NAIL_COUNT = 25
RESIZE_FACTOR = 4
DEFAULT_IMAGE_WIDTH = RESIZE_FACTOR * DEFAULT_NAIL_COUNT
DEFAULT_CANVAS_SIZE = (DEFAULT_IMAGE_WIDTH, DEFAULT_IMAGE_WIDTH)
WHITE = (255, 255, 255, 255)
LINE_COLOR = (0, 0, 0, 255)
NAIL_COLOR = (255, 0, 0, 255)
PADDING = 5
FULL_CIRCLE_ANGLE = 360
HALF_CIRCLE_ANGLE = 180

CoordData = tuple[int, int]
ColorData = tuple[int, int, int, int]


def get_nail_coordinates(nail_index: int, nail_count: int, canvas_width: int) -> CoordData:
    radius = canvas_width // 2 - PADDING
    nail_angle = FULL_CIRCLE_ANGLE / nail_count
    radian = nail_angle * nail_index * math.pi / HALF_CIRCLE_ANGLE
    coord = (
        int(radius * math.cos(radian)) + radius + PADDING,
        int(radius * math.sin(radian)) + radius + PADDING,
    )
    return coord


def draw_line(
    initial_coordinate: CoordData,
    final_coordinate: CoordData,
    image: Image.Image,
    color: ColorData,
) -> None:
    slope = 2.0
    line_offset = 0.0
    start_x, start_y = initial_coordinate
    final_x, final_y = final_coordinate
    if start_x != final_x:
        slope = (start_y - final_y) / (start_x - final_x)
        line_offset = final_y - final_x * slope
    if (slope <= 1) and (slope >= -1):
        flow = -1 if start_x > final_x else 1
        for x in range(start_x, final_x, flow):
            y = int(slope * x + line_offset)
            image.putpixel((x, y), color)
        return
    slope = (start_x - final_x) / (start_y - final_y)
    line_offset = final_x - final_y * slope
    flow = -1 if start_y > final_y else 1
    for y in range(start_y, final_y, flow):
        x = int(slope * y + line_offset)
        image.putpixel((x, y), color)


def generate_image(song_lyrics: str) -> Image.Image:
    words = song_lyrics.split()
    word_to_nail: dict[str, int] = {}
    nails: list[str] = []
    for word in words:
        if word not in word_to_nail:
            word_to_nail[word] = len(nails)
            nails.append(word)
    nail_count = len(nails)
    image_size = get_image_size(nail_count)
    image = Image.new("RGBA", image_size, WHITE)
    for current_word, next_word in zip(words, words[1:]):
        current_nail = word_to_nail[current_word]
        next_nail = word_to_nail[next_word]
        if current_nail == next_nail:
            continue
        current_coord = get_nail_coordinates(current_nail, nail_count, image_size[0])
        next_coord = get_nail_coordinates(next_nail, nail_count, image_size[0])
        draw_line(current_coord, next_coord, image, LINE_COLOR)
    for nail_index in range(nail_count):
        coord = get_nail_coordinates(nail_index, nail_count, image_size[0])
        image.putpixel(coord, NAIL_COLOR)
    return image.rotate(90)


def get_image_size(nail_count: int) -> tuple[int, int]:
    if nail_count > DEFAULT_NAIL_COUNT:
        size = RESIZE_FACTOR * nail_count
        return (size, size)
    return DEFAULT_CANVAS_SIZE


def main() -> None:
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
    for filename in os.listdir(MUSIC_FOLDER):
        if not filename.endswith(".txt"):
            continue
        full_path = os.path.join(MUSIC_FOLDER, filename)
        with open(full_path, "r", encoding="utf-8") as file:
            song_lyrics = file.read().lower()
        image_name, _ = os.path.splitext(filename)
        image = generate_image(song_lyrics)
        image.save(os.path.join(OUTPUT_FOLDER, f"{image_name}.png"))


if __name__ == "__main__":
    main()
