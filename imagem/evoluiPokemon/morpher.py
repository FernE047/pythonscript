from PIL import Image
import os
import multiprocessing

FRAMES_TOTAL = 30
SOURCE_IMAGE = "./source.png"
TARGET_IMAGE = "./target.png"
FRAMES_FOLDER = "./frames"
TRANSPARENT_WHITE = (255, 255, 255, 0)
CONFIG_FILE = "./config.txt"

CoordData = tuple[int, int]
PixelData = tuple[int, ...] | float


def open_image_as_rgba(image_path: str) -> Image.Image:
    with Image.open(image_path) as image:
        image_in_memory = image.copy()
        if image.mode != "RGBA":
            return image_in_memory.convert("RGBA")
        return image_in_memory


def interpolate_color(
    pixel_source: PixelData, pixel_target: PixelData, index: int
) -> PixelData:
    if not isinstance(pixel_source, tuple):
        source: tuple[int, ...] = (int(pixel_source),)
    else:
        source = pixel_source
    if not isinstance(pixel_target, tuple):
        target: tuple[int, ...] = (int(pixel_target),)
    else:
        target = pixel_target
    color_values: list[int] = []
    for color_source, color_target in zip(source, target):
        interpolation_factor = (color_target - color_source) / (FRAMES_TOTAL + 1)
        color_values.append(int(interpolation_factor * index + color_source))
    return tuple(color_values)


def interpolate_coordinates(
    source: CoordData, target: CoordData, index: int
) -> CoordData:
    interpolated_coordinates: list[int] = []
    for coord_source, coord_target in zip(source, target):
        interpolation_factor = (coord_target - coord_source) / (FRAMES_TOTAL + 1)
        interpolated_coordinates.append(
            int(interpolation_factor * index + coord_source)
        )
    return (interpolated_coordinates[0], interpolated_coordinates[1])


def get_pixel(image: Image.Image, coord: tuple[int, int]) -> float | tuple[int, ...]:
    try:
        pixel = image.getpixel(coord)
    except IndexError:
        raise ValueError(
            f"Coordinate {coord} is out of bounds for the image size {image.size}"
        )
    if pixel is None:
        raise ValueError(f"Pixel not found at coordinate: {coord}")
    return pixel


def makeFrame(frame_index: int) -> None:
    def separate_coords(coord_str: str) -> tuple[int, int]:
        try:
            x_str, y_str = coord_str.split(",")
            return (int(x_str), int(y_str))
        except ValueError:
            raise ValueError(f"Invalid coordinate format: {coord_str}")

    image_source = open_image_as_rgba(SOURCE_IMAGE)
    image_target = open_image_as_rgba(TARGET_IMAGE)
    print(f"Generating Frame : {frame_index}")
    frame = Image.new("RGBA", image_target.size, TRANSPARENT_WHITE)
    with open(CONFIG_FILE, "r", encoding="utf-8") as file:
        lines = file.readlines()
    for line in lines:
        if not line.strip():
            continue
        if line.find("fundo") != -1:
            coord = separate_coords(line[: -len(" fundo")])
            if len(coord) != 2:
                raise ValueError(f"Invalid coordinate format: {line}")
            pixel = get_pixel(image_source, coord)
            frame.putpixel(coord, pixel)
            continue
        coords: list[tuple[int, int]] = []
        for coord_str in line.split(" "):
            coord = separate_coords(coord_str)
            if len(coord) != 2:
                raise ValueError(f"Invalid coordinate format: {line}")
            coords.append(coord)
        coord_target = coords[1]
        pixel_target = get_pixel(image_target, coord_target)
        coord_source = coords[0]
        pixel_source = get_pixel(image_source, coord_source)
        interpolated_coord = interpolate_coordinates(
            coord_source, coord_target, frame_index + 1
        )
        interpolated_color = interpolate_color(
            pixel_source, pixel_target, frame_index + 1
        )
        frame.putpixel(interpolated_coord, interpolated_color)
    print(f"\tFrame Completed : {frame_index}")
    frame.save(f"{FRAMES_FOLDER}/frame{frame_index + 1:03d}.png")


def move_image(image_name: str, image_rename: str) -> None:
    image = open_image_as_rgba(image_name)
    image.save(f"{FRAMES_FOLDER}/{image_rename}")


def create_first_and_last_frames() -> None:
    move_image(SOURCE_IMAGE, "frame000.png")
    move_image(TARGET_IMAGE, f"frame{FRAMES_TOTAL + 1:03d}.png")


def main() -> None:
    create_first_and_last_frames()
    with multiprocessing.Pool(os.cpu_count()) as cpu_pool:
        cpu_pool.map(makeFrame, range(FRAMES_TOTAL))


if __name__ == "__main__":
    main()
