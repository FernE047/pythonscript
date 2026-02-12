from enum import Enum
import os
from PIL import Image
import multiprocessing

FRAMES_FOLDER = "./frames"

CoordData = tuple[int, int]


class Direction(Enum):
    DOWN_RIGHT = 0
    DOWN = 1
    DOWN_LEFT = 2
    LEFT = 3
    UP_LEFT = 4
    UP = 5
    UP_RIGHT = 6
    RIGHT = 7


ORTHOGONAL_DIRECTIONS = (Direction.DOWN, Direction.LEFT, Direction.UP, Direction.RIGHT)
OPAQUE_ALPHA_VALUE = 255
TRANSPARENT_ALPHA_VALUE = 0


def apply_direction(coord: CoordData, direction: Direction) -> CoordData:
    x, y = coord
    if direction == Direction.DOWN_RIGHT:
        return (x + 1, y + 1)
    if direction == Direction.DOWN:
        return (x, y + 1)
    if direction == Direction.DOWN_LEFT:
        return (x - 1, y + 1)
    if direction == Direction.LEFT:
        return (x - 1, y)
    if direction == Direction.UP_LEFT:
        return (x - 1, y - 1)
    if direction == Direction.UP:
        return (x, y - 1)
    if direction == Direction.UP_RIGHT:
        return (x + 1, y - 1)
    if direction == Direction.RIGHT:
        return (x + 1, y)


def get_pixel(image: Image.Image, coord: CoordData) -> tuple[int, ...]:
    pixel = image.getpixel(coord)
    if pixel is None:
        raise ValueError("Pixel not found")
    if isinstance(pixel, int):
        raise ValueError("Image is not in RGBA mode")
    if isinstance(pixel, float):
        raise ValueError("Image is not in RGBA mode")
    if len(pixel) < 4:
        raise ValueError("Image is not in RGBA mode")
    return pixel


def average_pixel(coord: CoordData, imagem: Image.Image) -> tuple[int, ...]:
    neighbor_pixels: list[tuple[int, ...]] = []
    for direction in Direction:
        coordenada = apply_direction(coord, direction)
        if coordenada[0] not in range(imagem.size[0]):
            continue
        if coordenada[1] not in range(imagem.size[1]):
            continue
        pixel = get_pixel(imagem, coordenada)
        if pixel[3] != OPAQUE_ALPHA_VALUE:
            continue
        neighbor_pixels.append(pixel)
    if not neighbor_pixels:
        return (0, 0, 0, 0)
    average_color = [0 for _ in neighbor_pixels[0]]
    for pixel in neighbor_pixels:
        for color_index, color in enumerate(pixel):
            average_color[color_index] += color
    neighbors_size = len(neighbor_pixels)
    if len(neighbor_pixels) == 0:
        return (0, 0, 0, 0)
    average_pixel = tuple([int(color / neighbors_size) for color in average_color])
    return average_pixel


def get_border_transparent_pixels(image: Image.Image) -> list[list[CoordData]]:
    width, height = image.size
    transparent_pixels: list[CoordData] = []

    def test_pixel(x: int, y: int) -> None:
        coord = (x, y)
        pixel = get_pixel(image, coord)
        if pixel[3] == TRANSPARENT_ALPHA_VALUE:
            transparent_pixels.append(coord)

    for x in range(width):
        test_pixel(x, 0)
        test_pixel(x, height - 1)
    for y in range(1, height - 1):
        test_pixel(0, y)
        test_pixel(width - 1, y)
    return [transparent_pixels]


def find_all_transparent_pixels(
    imagem: Image.Image, transparent_pixels: list[list[CoordData]]
) -> None:
    changed = True
    while changed:
        changed = find_more_transparent_pixels(imagem, transparent_pixels)


def find_more_transparent_pixels(
    imagem: Image.Image, transparent_pixels: list[list[CoordData]]
) -> bool:
    candidates: list[CoordData] = []
    previous_layer = transparent_pixels[-1]
    for coord in previous_layer:
        for direction in ORTHOGONAL_DIRECTIONS:
            coordenada = apply_direction(coord, direction)
            if coordenada[0] not in range(imagem.size[0]):
                continue
            if coordenada[1] not in range(imagem.size[1]):
                continue
            pixel = get_pixel(imagem, coordenada)
            if pixel[3] != TRANSPARENT_ALPHA_VALUE:
                continue
            if coordenada in previous_layer:
                continue
            if coordenada in candidates:
                continue
            if len(transparent_pixels) > 1:
                if coordenada in transparent_pixels[-2]:
                    continue
            candidates.append(coordenada)
    if candidates:
        transparent_pixels.append(candidates)
        return True
    return False


def find_hole_border(
    image: Image.Image, transparent_pixels: list[CoordData]
) -> list[CoordData]:
    width, height = image.size
    border_coordinates: list[CoordData] = []

    def test_coord(coord: CoordData) -> None:
        if coord not in transparent_pixels:
            if coord not in border_coordinates:
                border_coordinates.append(coord)

    for x in range(width):
        pixel = get_pixel(image, (x, 0))
        was_last_pixel_transparent = pixel[3] == TRANSPARENT_ALPHA_VALUE
        for y in range(height):
            pixel = get_pixel(image, (x, y))
            is_current_pixel_transparent = pixel[3] == TRANSPARENT_ALPHA_VALUE
            if was_last_pixel_transparent ^ is_current_pixel_transparent:
                if is_current_pixel_transparent:
                    test_coord((x, y))
                else:
                    test_coord((x, y - 1))
            was_last_pixel_transparent = is_current_pixel_transparent
    for y in range(height):
        pixel = get_pixel(image, (0, y))
        was_last_pixel_transparent = pixel[3] == TRANSPARENT_ALPHA_VALUE
        for x in range(width):
            pixel = get_pixel(image, (x, y))
            is_current_pixel_transparent = pixel[3] == TRANSPARENT_ALPHA_VALUE
            if was_last_pixel_transparent ^ is_current_pixel_transparent:
                if is_current_pixel_transparent:
                    test_coord((x, y))
                else:
                    test_coord((x - 1, y))
            was_last_pixel_transparent = is_current_pixel_transparent
    return border_coordinates


def extend_holes(
    image: Image.Image,
    trapped_pixels: list[CoordData],
    transparent_pixels: list[CoordData],
) -> list[CoordData]:
    coords: list[CoordData] = []
    for pixel_coord in trapped_pixels:
        for direction in ORTHOGONAL_DIRECTIONS:
            coord = apply_direction(pixel_coord, direction)
            if coord in transparent_pixels:
                continue
            if coord in coords:
                continue
            pixel = get_pixel(image, coord)
            if pixel[3] == TRANSPARENT_ALPHA_VALUE:
                coords.append(coord)
    return coords


def fix_trapped_pixels(
    image: Image.Image, transparent_pixels: list[CoordData]
) -> None:  # make it better
    trapped_pixels = find_hole_border(image, transparent_pixels)
    while trapped_pixels:
        for coord in trapped_pixels:
            image.putpixel(coord, average_pixel(coord, image))
        trapped_pixels = extend_holes(image, trapped_pixels, transparent_pixels)


def corrigeFrame(index: int) -> None:
    print(f"Fixing Frame : {index}")
    filename = f"{FRAMES_FOLDER}/frame{index:03d}.png"
    image = Image.open(filename)
    transparent_pixels = get_border_transparent_pixels(image)
    find_all_transparent_pixels(image, transparent_pixels)
    all_transparent_pixels: list[CoordData] = []
    for layer in transparent_pixels:
        for coord in layer:
            all_transparent_pixels.append(coord)
    fix_trapped_pixels(image, all_transparent_pixels)
    image.save(filename)
    image.close()
    print(f"\tFrame fixed : {index}")


def main() -> None:
    quantiaFrames = len(os.listdir(FRAMES_FOLDER))
    cpu_pool = multiprocessing.Pool(os.cpu_count())
    cpu_pool.map(corrigeFrame, range(1, quantiaFrames - 1))


if __name__ == "__main__":
    main()
