from PIL import Image, ImageDraw

INPUT_IMAGE = "input.png"
OUTPUT_IMAGE = "output.png"
SAFETY_OFFSET = 2
BACKGROUND_COLOR = (0, 0, 0, 0)
LINE_COLOR = (0, 0, 0, 255)
LINE_WIDTH = 1
MAX_BRIGHTNESS = 255
COLOR_CHANNELS = 3
MAX_BRIGHTNESS_TOTAL = MAX_BRIGHTNESS * COLOR_CHANNELS

CoordData = tuple[int, int]


def get_pixel(imagem: Image.Image, coord: tuple[int, int]) -> tuple[int, ...]:
    pixel = imagem.getpixel(coord)
    if pixel is None:
        return BACKGROUND_COLOR
    if not isinstance(pixel, tuple):
        pixel_int = int(pixel)
        return (pixel_int, pixel_int, pixel_int)
    return pixel


def main() -> None:
    source_image = Image.open(INPUT_IMAGE)
    width, height = source_image.size
    new_width = width + SAFETY_OFFSET
    new_height = height + SAFETY_OFFSET
    new_size = (new_width, new_height)
    line_image = Image.new("RGBA", new_size, BACKGROUND_COLOR)
    line_image.paste(source_image, (1, 1))
    nails: list[CoordData] = []
    for x in range(new_width):
        nails.append((x, 0))
        nails.append((x, new_height - 1))
    for y in range(1, new_height - 1):
        nails.append((0, y))
        nails.append((new_width - 1, y))
    output_image = Image.new("RGBA", new_size, BACKGROUND_COLOR)
    image_draw = ImageDraw.Draw(line_image)
    output_draw = ImageDraw.Draw(output_image)
    current_nail = nails[0]
    while True:
        biggest_nail = nails[0]
        biggest_value = 0
        for nail in nails:
            analysis_image = line_image.copy()
            draw_analysis = ImageDraw.Draw(analysis_image)
            draw_analysis.line(current_nail + nail, fill=LINE_COLOR, width=LINE_WIDTH)
            total_value = 0.0
            total_line = 0
            for x in range(new_width):
                for y in range(new_height):
                    analysis_pixel = get_pixel(analysis_image, (x, y))
                    if analysis_pixel != LINE_COLOR:
                        continue
                    pixel = get_pixel(line_image, (x, y))
                    valor = sum(pixel[0:COLOR_CHANNELS])
                    total_value += valor / MAX_BRIGHTNESS_TOTAL
                    total_line += 1
            average_pixel_value = total_value / total_line if total_line != 0 else 0
            if average_pixel_value >= biggest_value:
                biggest_value = average_pixel_value
                biggest_nail = nail
        if biggest_value != 0:
            line_coords = current_nail + biggest_nail
            image_draw.line(line_coords, fill=BACKGROUND_COLOR, width=LINE_WIDTH)
            output_draw.line(line_coords, fill=LINE_COLOR, width=LINE_WIDTH)
            current_nail = biggest_nail
        else:
            break
    output_image.save(OUTPUT_IMAGE)


if __name__ == "__main__":
    main()
