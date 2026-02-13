import os
from time import time
from PIL import Image

BACKGROUND_COLOR = (0, 0, 0, 0)
MAX_BRIGHTNESS = 255
MAX_COLOR_CHANNELS = 4
ALLOWED_FILE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".bmp", ".gif")


def open_image_as_rgba(image_path: str) -> Image.Image:
    with Image.open(image_path) as image:
        image_in_memory = image.copy()
        if image.mode != "RGBA":
            return image_in_memory.convert("RGBA")
        return image_in_memory


def get_image_from_folder(folder: str) -> list[str]:
    images: list[str] = []
    if not os.path.exists(folder):
        return images
    for filename in os.listdir(folder):
        if not filename.lower().endswith(ALLOWED_FILE_EXTENSIONS):
            continue
        images.append(os.path.join(folder, filename))
    return images


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


def save_image(image_name: str, image: Image.Image) -> None:
    try:
        image.save(f"{image_name}.png")
    except PermissionError:
        pass
    index = 1
    while True:
        try:
            image.save(f"{image_name}_{index}.png")
            return
        except PermissionError:
            # just in case the user has a lot of files with the same name open at the same time
            index += 1


def get_largest_image_size(image_names: list[str]) -> tuple[int, int]:
    max_width = 0
    max_height = 0
    for image_name in image_names:
        size = open_image_as_rgba(image_name).size
        if size[0] >= max_width:
            max_width = size[0]
        if size[1] >= max_height:
            max_height = size[1]
    size = (max_width, max_height)
    if size == (0, 0):
        raise ValueError("No images found in the specified folder.")
    return size


def main() -> None:
    print("enter the name of the image folder")
    folder = input()
    image_names = get_image_from_folder(folder)
    size = get_largest_image_size(image_names)
    width, height = size
    print(size)
    total = width * height
    print(total)
    average_image = Image.new("RGBA", size, BACKGROUND_COLOR)
    print("enter a name for the average image")
    output_name = input()
    start_time = time()
    percentage = 0
    tick = 0
    end_time = time()
    try:
        for y in range(height):
            for x in range(width):
                tick += 1
                new_color = [0 for _ in range(MAX_COLOR_CHANNELS)]
                divisor = 0
                for image_name in image_names:
                    current_image = Image.new("RGBA", size, BACKGROUND_COLOR)
                    image = open_image_as_rgba(image_name)
                    current_image.paste(image, (0, 0))
                    pixel = current_image.getpixel((x, y))
                    if pixel is None:
                        pixel = BACKGROUND_COLOR
                    if not isinstance(pixel, tuple):
                        pixel_int = int(pixel)
                        pixel = (pixel_int, pixel_int, pixel_int, MAX_BRIGHTNESS)
                    if pixel[-1] != 0:
                        divisor += 1
                        for index in range(MAX_COLOR_CHANNELS):
                            new_color[index] += pixel[index]
                if divisor == 0:
                    divisor = 1
                for index in range(MAX_COLOR_CHANNELS):
                    new_color[index] = int(new_color[index] / divisor)
                average_image.putpixel((x, y), tuple(new_color))
                if int(tick * 100 / total) != percentage:
                    current_time = time()
                    percentage = int(tick * 100 / total)
                    save_image(output_name, average_image)
                    print(f"{percentage}%")
                    print_elapsed_time(current_time - end_time)
                    end_time = current_time
    except KeyboardInterrupt:
        pass
    save_image(output_name, average_image)
    end_time = time()
    print_elapsed_time(end_time - start_time)


if __name__ == "__main__":
    main()
