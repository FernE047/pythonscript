from PIL import Image
import os

# this program was made when I used python 3.6, I didn't knew ide at the time and relied on python idle
# hence the max size that fits into idle is 165

MAX_RGB_BRIGHTNESS = 256
LEVELS = " `.,+%@#"
DIVISOR = MAX_RGB_BRIGHTNESS // len(LEVELS)
ACCEPTED_IMAGE_FORMATS = (".png", ".jpg", ".jpeg", ".bmp", ".gif")
MAX_SIZE = 165  # max size that fits into python idle
MIN_SIZE = 75  # min size that fits into python idle for decent quality
TERMINAL_SIZE = 60  # if you want to display in terminal
WHATSAPP_SIZE = 26  # if you want to display in whatsapp


def open_image_as_rgb(image_path: str) -> Image.Image:
    with Image.open(image_path) as image:
        image_in_memory = image.copy()
        if image.mode != "RGB":
            return image_in_memory.convert("RGB")
        return image_in_memory


def get_image_from_folder() -> list[str]:
    print("enter the image folder:")
    image_folder = input()
    print("quantity")
    user_input = input()
    try:
        quantity = int(user_input)
    except ValueError:
        quantity = None
    folder = f"images/{image_folder}"
    images: list[str] = []
    if not os.path.exists(folder):
        return images
    for filename in os.listdir(folder):
        if not filename.lower().endswith(ACCEPTED_IMAGE_FORMATS):
            continue
        images.append(os.path.join(folder, filename))
        if quantity is not None and len(images) >= quantity:
            return images
    return images


def resize_image_to_width(
    width_output: int, image_black_white: Image.Image
) -> Image.Image:
    width, height = image_black_white.size
    if width <= width_output:
        return image_black_white
    aspect_ratio = width_output / width
    height_output = int(height * aspect_ratio)
    return image_black_white.resize((width_output, height_output))


def set_display_width() -> int:
    print("size")
    print(f"{MAX_SIZE} - max")
    print(f"{MIN_SIZE} - min")
    print(f"{TERMINAL_SIZE} - terminal")
    print(f"{WHATSAPP_SIZE} - whats")
    size = input()
    if size == "whats":
        return WHATSAPP_SIZE
    if size == "max":
        return MAX_SIZE
    if size == "min":
        return MIN_SIZE
    if size == "terminal":
        return TERMINAL_SIZE
    try:
        return int(size)
    except ValueError:
        return MIN_SIZE


def main() -> None:
    image_paths = get_image_from_folder()
    width_output = set_display_width()
    for image in image_paths:
        print("\n" + image + "\n")
        image_colored = open_image_as_rgb(image)
        image_black_white = image_colored.convert("L")
        image_output = resize_image_to_width(width_output, image_black_white)
        width, height = image_output.size
        for y in range(height):
            row = ""
            for x in range(width):
                pixel = image_output.getpixel((x, y))
                assert isinstance(pixel, int)  # since the image is in 'L' mode
                row += LEVELS[int(pixel / DIVISOR) - 1]
            print(row)


if __name__ == "__main__":
    main()
