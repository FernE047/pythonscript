from PIL import Image
import os

IMAGES_FOLDER = "images"
EXTENSIONS_AVAILABLE = (".png", ".jpg", ".jpeg", ".bmp", ".gif")
COLOR_DISTANCE_THRESHOLD = 256 * 3
PALETTE_COMMAND_PREFIX = "palette"
FOLDER_COMMAND_PREFIX = "folder"
PALETTE_FOLDER = "palette"
if not os.path.exists(PALETTE_FOLDER):
    os.makedirs(PALETTE_FOLDER)
SAVE_IMAGE_THRESHOLD = 100
EXIT_INPUT = "0"
MAX_COLOR_CHANNELS = 3
RED_CHANNEL = 0
GREEN_CHANNEL = 1
BLUE_CHANNEL = 2

PixelData = tuple[int, ...]
PaletteData = set[PixelData]

CoordData = tuple[int, int]


def get_pixel(image: Image.Image, coord: CoordData) -> PixelData:
    pixel = image.getpixel(coord)
    if pixel is None:
        raise ValueError("Pixel not found")
    if isinstance(pixel, int):
        raise ValueError("Image is not in RGB mode")
    if isinstance(pixel, float):
        raise ValueError("Image is not in RGB mode")
    if len(pixel) < MAX_COLOR_CHANNELS:
        raise ValueError("Image is not in RGB mode")
    return pixel


def get_image_from_folder(image_sub_folder: str) -> list[str]:
    folder = f"{IMAGES_FOLDER}/{image_sub_folder}"
    images: list[str] = []
    if not os.path.exists(folder):
        return images
    for filename in os.listdir(folder):
        if filename.lower().endswith(EXTENSIONS_AVAILABLE):
            images.append(os.path.join(folder, filename))
    return images


def get_image(image_sub_folder: str) -> str:
    folder = f"{IMAGES_FOLDER}/{image_sub_folder}"
    if not os.path.exists(folder):
        return ""
    for filename in os.listdir(folder):
        if filename.lower().endswith(EXTENSIONS_AVAILABLE):
            return os.path.join(folder, filename)
    return ""


def open_image_as_rgba(image_path: str) -> Image.Image:
    with Image.open(image_path) as image:
        image_in_memory = image.copy()
        if image.mode != "RGBA":
            return image_in_memory.convert("RGBA")
        return image_in_memory


def fetch_palette(image_name: str) -> PaletteData:
    print("fetching palette, please wait, it can take a while")
    image = open_image_as_rgba(image_name)
    width, height = image.size
    palette: PaletteData = set()
    for x in range(width):
        for y in range(height):
            pixel = get_pixel(image, (x, y))
            palette.add(pixel)
    return palette


def fetch_palettes(images: list[str]) -> PaletteData:
    print("fetching palettes, please wait, it can take a while")
    palette: PaletteData = set()
    for image_name in images:
        print(image_name)
        image = open_image_as_rgba(image_name)
        width, height = image.size
        for x in range(width):
            for y in range(height):
                pixel = get_pixel(image, (x, y))
                palette.add(pixel)
    return palette


def apply_color_palette(
    nome: str, color_palette: PaletteData, image_path: str
) -> Image.Image:
    image = open_image_as_rgba(image_path)
    width, height = image.size
    color_mapped_image = image.copy()
    print(width)
    palette_list = list(color_palette)
    for x in range(width):
        if x % SAVE_IMAGE_THRESHOLD == 0:
            print(x)
            image_name, extension = os.path.splitext(nome)
            try:
                color_mapped_image.save(nome)
            except PermissionError:
                color_mapped_image.save(f"{image_name}_output{extension}")
        for y in range(height):
            pixel = get_pixel(color_mapped_image, (x, y))
            if pixel in color_palette:
                color_mapped_image.putpixel((x, y), pixel)
                continue
            new_color = palette_list[0]
            closest_color_distance = COLOR_DISTANCE_THRESHOLD
            for current_color in color_palette:
                red = abs(current_color[RED_CHANNEL] - pixel[RED_CHANNEL])
                green = abs(current_color[GREEN_CHANNEL] - pixel[GREEN_CHANNEL])
                blue = abs(current_color[BLUE_CHANNEL] - pixel[BLUE_CHANNEL])
                color_distance = red + green + blue
                if color_distance < closest_color_distance:
                    new_color = current_color
                    closest_color_distance = color_distance
            color_mapped_image.putpixel((x, y), new_color)
    return color_mapped_image


def get_int_input(prompt: str, min_value: int, max_value: int) -> int:
    full_prompt = f"{prompt} (between {min_value} and {max_value}): "
    while True:
        try:
            value = int(input(full_prompt))
            if min_value <= value <= max_value:
                return value
            else:
                print(f"Please enter a number between {min_value} and {max_value}.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")


def get_palette_from_input() -> tuple[str, PaletteData]:
    image_name = ""
    print(
        "where is the color palette? (type 'palette ' followed by the name of the palette, or 'folder ' followed by the name of the folder with the images to use as palette, or the name of the image to use as palette)"
    )
    input_folder = input()
    if not input_folder.startswith(
        f"{PALETTE_COMMAND_PREFIX} "
    ) and not input_folder.startswith(f"{FOLDER_COMMAND_PREFIX} "):
        image = get_image(input_folder)
        color_palette = fetch_palette(image)
        image_name += input_folder.title()
        return image_name, color_palette
    command, name = input_folder.split(" ", 1)
    if command == PALETTE_COMMAND_PREFIX:
        color_palette = fetch_palette(f"{PALETTE_FOLDER}/{name}.png")
        image_name += name.title()
        return image_name, color_palette
    if command == FOLDER_COMMAND_PREFIX:
        images = get_image_from_folder(name)
        color_palette = fetch_palettes(images)
        image_name += name.title()
        return image_name, color_palette
    raise ValueError("Invalid input")


def main() -> None:
    while True:
        image_name, color_palette = get_palette_from_input()
        print(f"palette's size: {len(color_palette)}")
        print(
            "\nWhere are the images to apply the palette? (type the name of the folder with the images)"
        )
        input_folder = input()
        images = get_image_from_folder(input_folder)
        for index, image in enumerate(images):
            print(f"{index}  -  {image}")
        num_imagem = get_int_input("\nWhich image?", 0, len(images) - 1)
        image = images[num_imagem]
        image_name = f"{input_folder.title()}{image_name}_{num_imagem}.png"
        image_name = os.path.join("images", image_name)
        print(image)
        color_mapped_image = apply_color_palette(image_name, color_palette, image)
        color_mapped_image.save(image_name)
        print(f"image saved as {image_name}")
        print(f"\nEnter {EXIT_INPUT} to exit, or anything else to continue")
        user_input = input()
        if user_input == EXIT_INPUT:
            break


if __name__ == "__main__":
    main()
