from pathlib import Path
from PIL import Image
from morph import interpolate_tuples
from correct_frames import fix_trapped_pixels

CoordData = tuple[int, int]
BACKGROUND_COLOR = (255, 255, 255, 0)
FRAME_FOLDER = Path("frames")
ALPHA_CHANNEL = 3
MAX_BRIGHTNESS = 255
PART_FOLDERS = Path("partes")
SOURCE_FOLDER = PART_FOLDERS / "iniciais"
TARGET_FOLDER = PART_FOLDERS / "finais"


def open_image_as_rgba(image_path: Path) -> Image.Image:
    with Image.open(image_path) as image:
        image_in_memory = image.copy()
        if image.mode != "RGBA":
            return image_in_memory.convert("RGBA")
        return image_in_memory


def get_pixel(imagem: Image.Image, coord: CoordData) -> tuple[int, ...]:
    pixel = imagem.getpixel(coord)
    if pixel is None:
        return BACKGROUND_COLOR
    if not isinstance(pixel, tuple):
        pixel_int = int(pixel)
        return (pixel_int, pixel_int, pixel_int)
    return pixel


def generate_background(image_name: Path) -> Image.Image:
    print("back iniciado")
    image = open_image_as_rgba(image_name.with_suffix(".png"))
    directory = SOURCE_FOLDER if image_name == Path("source") else TARGET_FOLDER
    for parts_path in [file_path for file_path in directory.iterdir()]:
        parte = open_image_as_rgba(parts_path)
        width, height = parte.size
        is_first_occurrence = True
        for x in range(width):
            alterations = 0
            for y in range(height):
                coord = (x, y)
                parte_pixel = get_pixel(parte, coord)
                if parte_pixel[ALPHA_CHANNEL] == MAX_BRIGHTNESS:
                    image.putpixel(coord, BACKGROUND_COLOR)
                    alterations += 1
            if is_first_occurrence and (alterations > 0):
                is_first_occurrence = False
            if not is_first_occurrence and (alterations == 0):
                break
    fix_trapped_pixels(image, [])
    image.save(f"./background_{image_name}.png")
    print("background finished")
    return image


def insert_background_frames() -> None:
    background_source = generate_background(Path("source"))
    background_target = generate_background(Path("target"))
    frames = [file for file in FRAME_FOLDER.iterdir()]
    frames.pop(0)
    frames.pop()
    frames.pop()
    for frame_index, frame_name in enumerate(frames):
        frame = open_image_as_rgba(frame_name)
        width, height = background_source.size
        for x in range(width):
            for y in range(height):
                coord = (x, y)
                pixel = get_pixel(frame, coord)
                if pixel[ALPHA_CHANNEL] != 0:
                    continue
                pixel_source = get_pixel(background_source, coord)
                pixel_target = get_pixel(background_target, coord)
                interpolated_pixel = interpolate_tuples(
                    pixel_source, pixel_target, frame_index
                )
                frame.putpixel(coord, interpolated_pixel)
        print(frame_index)
        frame.save(frame_name)