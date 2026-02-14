from PIL import Image
from random import randint
from time import time

IMAGE_INPUT = "input.png"
WHITE: tuple[int, ...] = (255, 255, 255, 255)
NOT_WHITE: tuple[int, ...] = (0, 0, 0, 255)

CoordData = tuple[int, int]


def get_pixel(image: Image.Image, coord: CoordData) -> tuple[int, ...]:
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


def print_elapsed_time(seconds: float) -> None:
    if seconds < 0:
        seconds = -seconds
        sign = "-"
    else:
        sign = ""
    total_ms = int(round(seconds * 1000))
    ms = total_ms % 1000
    total_s = total_ms // 1000
    s = total_s % 60
    total_min = total_s // 60
    m = total_min % 60
    total_h = total_min // 60
    h = total_h % 24
    d = total_h // 24
    parts: list[str] = []

    def add(value: int, singular: str, plural: str) -> None:
        if value:
            parts.append(f"{value} {singular if value == 1 else plural}")

    add(d, "day", "days")
    add(h, "hour", "hours")
    add(m, "minute", "minutes")
    add(s, "second", "seconds")
    if ms or not parts:
        parts.append(f"{ms} millisecond" if ms == 1 else f"{ms} milliseconds")
    print(f"{sign}{', '.join(parts)}")


def find_white_pixel(image: Image.Image, index: int) -> CoordData:
    width, height = image.size
    total = 0
    for x in range(width):
        for y in range(height):
            coord = (x, y)
            pixel = get_pixel(image, coord)
            if pixel == WHITE:
                total += 1
            if total == index:
                return coord
    raise ValueError("White pixel not found")


def shuffle_image_by_percentage(image: Image.Image, randomness: float) -> Image.Image:
    width, height = image.size
    total = width * height
    random_pixels_count = 0
    available_white_pixels = total
    current_randomness_ratio = random_pixels_count / total
    shuffled_image = Image.new("RGBA", (width, height), WHITE)
    for x in range(width):
        for y in range(height):
            coord = (x, y)
            source_pixel = get_pixel(image, coord)
            if current_randomness_ratio >= randomness:
                random_white_index = randint(1, available_white_pixels)
                swap_coord = find_white_pixel(shuffled_image, random_white_index)
                available_white_pixels -= 1
                shuffled_image.putpixel(swap_coord, source_pixel)
                continue
            swap_coord = (-1, -1)
            target_pixel = NOT_WHITE
            while target_pixel != WHITE:
                swap_x = randint(0, width - 1)
                swap_y = randint(0, height - 1)
                swap_coord = (swap_x, swap_y)
                target_pixel = get_pixel(shuffled_image, swap_coord)
            random_pixels_count += 1
            available_white_pixels -= 1
            current_randomness_ratio = random_pixels_count / total
            shuffled_image.putpixel(swap_coord, source_pixel)
    return shuffled_image


def open_image_as_rgba(image_path: str) -> Image.Image:
    with Image.open(image_path) as image:
        image_in_memory = image.copy()
        if image.mode != "RGBA":
            return image_in_memory.convert("RGBA")
        return image_in_memory


def main() -> None:
    image = open_image_as_rgba(IMAGE_INPUT)
    elapsed_times: list[float] = []
    for percentage in range(100, -1, -1):
        start_time = time()
        shuffled_image = shuffle_image_by_percentage(image, percentage)
        end_time = time()
        elapsed_time = end_time - start_time
        print(f"Randomness percentage : {percentage}%\n")
        print_elapsed_time(elapsed_time)
        shuffled_image.save(f"output_{percentage:03d}.png")
        elapsed_times.append(elapsed_time)
    sorted_times = sorted(elapsed_times)
    print("Resultados : ")
    for elapsed_time in sorted_times:
        print(f"{elapsed_times.index(elapsed_time)}% : {elapsed_time}")


if __name__ == "__main__":
    main()
