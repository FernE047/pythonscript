from PIL import Image
import os
import math
import numpy

BACKGROUND_COLOR = (255, 255, 255, 255)
NAIL_COLOR = (255, 0, 0, 255)
LINE_COLOR = (0, 0, 0, 255)
SAFETY_OFFSET = 1
FULL_CIRCLE_ANGLE = 360
HALF_CIRCLE_ANGLE = 180
NAIL_TOTAL = 400
MAX_BRIGHTNESS = 255
COLOR_CHANNELS = 3
MAX_BRIGHTNESS_TOTAL = MAX_BRIGHTNESS * COLOR_CHANNELS
ALPHA_CHANNEL = 3
INPUT_IMAGE = "input.png"
OUTPUT_IMAGE = "output.png"
EXAMPLE_IMAGE = "example.png"

CoordData = tuple[int, int]
ColorData = tuple[int, int, int, int]


def save_image(image: Image.Image, path: str) -> None:
    try:
        image.save(path)
    except PermissionError:
        image_name, extension = os.path.splitext(path)
        index_attempt = 0
        while True:
            try:
                image.save(f"{image_name}_{index_attempt}.{extension}")
                break
            except PermissionError:
                index_attempt += 1


def get_pixel(imagem: Image.Image, coord: tuple[int, int]) -> tuple[int, ...]:
    pixel = imagem.getpixel(coord)
    if pixel is None:
        return BACKGROUND_COLOR
    if not isinstance(pixel, tuple):
        pixel_int = int(pixel)
        return (pixel_int, pixel_int, pixel_int)
    return pixel


def place_nails_in_image(image: Image.Image) -> list[CoordData]:
    width, height = image.size
    width_squared = (width / 2) ** 2
    height_squared = (height / 2) ** 2
    radius_real = math.sqrt(width_squared + height_squared)
    radius = int(radius_real) + SAFETY_OFFSET
    print(radius)
    nail_angle_increment = FULL_CIRCLE_ANGLE / NAIL_TOTAL
    nail_coordinates: list[CoordData] = []
    for angle in numpy.arange(0, FULL_CIRCLE_ANGLE, nail_angle_increment):
        angle_in_radians = angle * math.pi / HALF_CIRCLE_ANGLE
        angle_cos = math.cos(angle_in_radians) + SAFETY_OFFSET
        angle_sin = math.sin(angle_in_radians) + SAFETY_OFFSET
        nail_x = int(radius * angle_cos)
        nail_y = int(radius * angle_sin)
        nail_coordinate = (nail_x, nail_y)
        nail_coordinates.append(nail_coordinate)
    return nail_coordinates


def dimension_by_nails(nail_coordinates: list[CoordData]) -> tuple[int, int]:
    high_x = 0
    high_y = 0
    for nail in nail_coordinates:
        if nail[0] >= high_x:
            high_x = nail[0]
        if nail[1] >= high_y:
            high_y = nail[1]
    size = (high_x + 2 * SAFETY_OFFSET, high_y + 2 * SAFETY_OFFSET)
    return size


def is_greater(
    source_nail: CoordData,
    target_nail: CoordData,
    lowest_value: float,
    nail_image: Image.Image,
) -> tuple[float, bool]:
    lowest_value_original = lowest_value
    total_value = 0.0
    total_line = 0
    if source_nail == target_nail:
        return (lowest_value, False)
    line_offset = 0.0
    slope = 2.0
    source_x, source_y = source_nail
    target_x, target_y = target_nail
    if source_x != target_x:
        difference_x = source_x - target_x
        difference_y = source_y - target_y
        slope = difference_y / difference_x
        line_offset = target_y - target_x * slope
    if (slope <= 1) and (slope >= -1):
        flow = 1
        if source_x > target_x:
            flow = -1
        for x in range(source_x, target_x, flow):
            y = int(slope * x + line_offset)
            pixel = get_pixel(nail_image, (x, y))
            if pixel[ALPHA_CHANNEL] != MAX_BRIGHTNESS:
                continue
            value = sum(pixel[0:COLOR_CHANNELS])
            total_value += value / MAX_BRIGHTNESS_TOTAL
            total_line += 1
        if total_line == 0:
            total_line = 1
        if (total_value / total_line) <= lowest_value:
            lowest_value = total_value / total_line
        has_changed = lowest_value != lowest_value_original
        return (lowest_value, has_changed)
    slope = (source_x - target_x) / (source_y - target_y)
    line_offset = target_x - target_y * slope
    if source_y > target_y:
        flow = -1
    else:
        flow = 1
    for y in range(source_y, target_y, flow):
        x = int(slope * y + line_offset)
        pixel = get_pixel(nail_image, (x, y))
        if pixel[ALPHA_CHANNEL] != MAX_BRIGHTNESS:
            continue
        value = sum(pixel[0:COLOR_CHANNELS])
        total_value += value / MAX_BRIGHTNESS_TOTAL
        total_line += 1
    if total_line == 0:
        total_line = 1
    if (total_value / total_line) <= lowest_value:
        lowest_value = total_value / total_line
    has_changed = lowest_value != lowest_value_original
    return (lowest_value, has_changed)


def draw_line(
    initial_coordinate: CoordData,
    final_coordinate: CoordData,
    image: Image.Image,
    color: ColorData,
) -> Image.Image:
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
        return image
    slope = (start_x - final_x) / (start_y - final_y)
    line_offset = final_x - final_y * slope
    flow = -1 if start_y > final_y else 1
    for y in range(start_y, final_y, flow):
        x = int(slope * y + line_offset)
        image.putpixel((x, y), color)
    return image


def main() -> None:
    image = Image.open(INPUT_IMAGE)
    nails = place_nails_in_image(image)
    width, height = image.size
    output_width, output_height = dimension_by_nails(nails)
    output_image = Image.new("RGBA", (output_width, output_height), BACKGROUND_COLOR)
    nails_image = output_image.copy()
    offset = ((output_width - width) // 2, (output_height - height) // 2)
    nails_image.paste(image, offset)
    current_nail = nails[0]
    example_image = nails_image.copy()
    for nail_coordinate in nails:
        example_image.putpixel(nail_coordinate, NAIL_COLOR)
    example_image.save(EXAMPLE_IMAGE)
    while True:
        closest_nail = nails[0]
        closest_distance = 1.0
        for nail_coordinate in nails:
            closest_distance, has_changed = is_greater(
                current_nail, nail_coordinate, closest_distance, nails_image
            )
            if has_changed:
                closest_nail = nail_coordinate
        if closest_distance == 1.0:
            break
        print(
            f"do prego {nails.index(current_nail)} para o prego {nails.index(closest_nail)}"
        )
        nails_image = draw_line(
            current_nail, closest_nail, nails_image, BACKGROUND_COLOR
        )
        output_image = draw_line(
            current_nail, closest_nail, output_image, LINE_COLOR
        )
        current_nail = closest_nail
        save_image(output_image, OUTPUT_IMAGE)
    save_image(output_image, OUTPUT_IMAGE)


if __name__ == "__main__":
    main()
