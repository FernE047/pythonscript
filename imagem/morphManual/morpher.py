from typing import TypeVar, cast
from PIL import Image
import os
import multiprocessing

SOURCE_IMAGE = "./inicial.png"
TARGET_IMAGE = "./final.png"
CONFIG_FOLDER = "./partes/config/"
OUTPUT_IMAGE = "./frames/frame.png"
TOTAL_FRAMES = 30
FINAL_FRAME = TOTAL_FRAMES + 1
BACKGROUND_COLOR = (255, 255, 255, 0)
BACKGROUND_IDENTIFIER = "background"
IDENTIFIER_LENGTH = len(BACKGROUND_IDENTIFIER)

# generic
R = TypeVar("R", bound=tuple[int, ...])
CoordData = tuple[int, int]


def get_coord_data(line: str) -> CoordData:
    comma_separated_values = line.split(",")
    try:
        coord_list = [int(value) for value in comma_separated_values]
    except ValueError as e:
        raise ValueError(f"Invalid coordinate value in line: {line}") from e
    if len(coord_list) != 2:
        raise ValueError(f"Expected 2 values for coordinates, got {len(coord_list)}")
    return cast(CoordData, tuple(coord_list))


def get_coords_data(line: str) -> list[CoordData]:
    coords: list[CoordData] = []
    for coord in line.split(" "):
        coords.append(get_coord_data(coord))
    if len(coords) != 2:
        raise ValueError(f"Expected 2 coordinates, got {len(coords)} in line: {line}")
    return coords


def get_pixel(imagem: Image.Image, coord: CoordData) -> tuple[int, ...]:
    pixel = imagem.getpixel(coord)
    if pixel is None:
        return BACKGROUND_COLOR
    if not isinstance(pixel, tuple):
        pixel_int = int(pixel)
        return (pixel_int, pixel_int, pixel_int)
    return pixel


def interpolate_tuples(tuple_source: R, tuple_target: R, frame_index: int) -> R:
    interpolated_values: list[int] = []
    for source_value, target_value in zip(tuple_source, tuple_target):
        difference = target_value - source_value
        interpolation_step = difference / FINAL_FRAME
        interpolated_value = int(interpolation_step * frame_index + source_value)
        interpolated_values.append(interpolated_value)
    return cast(R, tuple(interpolated_values))


def open_image_as_rgba(image_path: str) -> Image.Image:
    with Image.open(image_path) as image:
        image_in_memory = image.copy()
        if image.mode != "RGBA":
            return image_in_memory.convert("RGBA")
        return image_in_memory


def inrerpolate_frames(index: int) -> None:
    source_image = open_image_as_rgba(SOURCE_IMAGE)
    target_image = open_image_as_rgba(TARGET_IMAGE)
    print(f"generating Frame : {index}")
    frame = Image.new("RGBA", target_image.size, BACKGROUND_COLOR)
    for filename in os.listdir(CONFIG_FOLDER):
        with open(f"{CONFIG_FOLDER}{filename}", "r", encoding="utf-8") as file:
            lines = file.read().splitlines()
        for line in lines:
            if not line:
                continue
            if line.find(BACKGROUND_IDENTIFIER) != -1:
                coord = get_coord_data(line[:-IDENTIFIER_LENGTH])
                pixel = get_pixel(source_image, coord)
                frame.putpixel(coord, pixel)
                continue
            coord_source, coord_target = get_coords_data(line)
            pixel_source = get_pixel(source_image, coord_source)
            pixel_target = get_pixel(target_image, coord_target)
            output_coord = interpolate_tuples(coord_source, coord_target, index)
            output_pixel = interpolate_tuples(pixel_source, pixel_target, index)
            frame.putpixel(output_coord, output_pixel)
    print(f"\tFrame Finished : {index}")
    save_frame(frame, index)


def move_image(image_name: str, frame_index: int) -> None:
    image = open_image_as_rgba(image_name)
    print(f"\n {image_name} size: {image.size}\n")
    save_frame(image, frame_index)


def create_first_and_last_frames() -> None:
    move_image(SOURCE_IMAGE, 0)
    move_image(TARGET_IMAGE, FINAL_FRAME)


def save_frame(frame: Image.Image, index: int) -> None:
    output_name, extension = os.path.splitext(OUTPUT_IMAGE)
    filename = f"{output_name}_{index:03d}{extension}"
    frame.save(filename)


def main() -> None:
    create_first_and_last_frames()
    p = multiprocessing.Pool(os.cpu_count())
    p.map(inrerpolate_frames, range(1, FINAL_FRAME))


if __name__ == "__main__":
    main()
