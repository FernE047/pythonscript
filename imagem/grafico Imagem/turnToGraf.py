from PIL import Image, ImageDraw

# this script takes an image and flattens it by using radial lines from the center. it's funny to use on Luigi's images, his nose becomes a big blob. poor mario brother.

IMAGE_NUMBER = "6"
SOURCE_IMAGE_PATH = f"images_{IMAGE_NUMBER}.jpg"
OUTPUT_IMAGE_PATH = f"images_graf_{IMAGE_NUMBER}.jpg"
EVEN_SAFETY_OFFSET = 2
ODD_SAFETY_OFFSET = 3
SCALING_FACTOR = 2
SCALING_SAFETY_OFFSET = 4
BACKGROUND_COLOR = (255, 255, 255, 255)
LINE_COLOR = (0, 0, 0, 255)
PRINTING_THRESHOLD = 50
LINE_WIDTH = 1


def open_image_as_rgba(image_path: str) -> Image.Image:
    with Image.open(image_path) as image:
        image_in_memory = image.copy()
        if image.mode != "RGBA":
            return image_in_memory.convert("RGBA")
        return image_in_memory


def create_base_image() -> Image.Image:
    image_source = open_image_as_rgba(SOURCE_IMAGE_PATH)
    size = image_source.size
    width, height = size
    width += EVEN_SAFETY_OFFSET if width % 2 == 0 else ODD_SAFETY_OFFSET
    height += EVEN_SAFETY_OFFSET if height % 2 == 0 else ODD_SAFETY_OFFSET
    base_image = Image.new("RGBA", (width, height))
    base_image.paste(image_source, (1, 1))
    print("the base image was created")
    return base_image


def main() -> None:
    base_image = create_base_image()
    width, height = base_image.size
    mid_point = (int((width + 1) / 2), int((height + 1) / 2))
    graph_width = int(SCALING_FACTOR * (width + height) + SCALING_SAFETY_OFFSET)
    flat_image = Image.new("RGB", (graph_width, height))
    print(graph_width)
    graf_x = 0
    for line_y in range(0, mid_point[1] + 1):
        line_image = Image.new("RGBA", (width, height), BACKGROUND_COLOR)
        draw = ImageDraw.Draw(line_image)
        line_coords = (mid_point[0], mid_point[1], 0, line_y)
        draw.line(line_coords, fill=LINE_COLOR, width=LINE_WIDTH)
        graf_y = 0
        if line_y % PRINTING_THRESHOLD == 0:
            print(line_y)
            flat_image.save(OUTPUT_IMAGE_PATH)
        for y in range(0, mid_point[1] + 1):
            for x in range(0, mid_point[0] + 1):
                if line_image.getpixel((x, y)) != LINE_COLOR:
                    continue
                pixel = base_image.getpixel((x, y))
                if pixel is None:
                    pixel = BACKGROUND_COLOR
                flat_image.putpixel((graf_x, graf_y), pixel)
                graf_y += 1
        graf_x += 1
    for line_y in range(mid_point[1] + 1, height):
        line_image = Image.new("RGBA", (width, height), BACKGROUND_COLOR)
        draw = ImageDraw.Draw(line_image)
        line_coords = (mid_point[0], mid_point[1], 0, line_y)
        draw.line(line_coords, fill=LINE_COLOR, width=LINE_WIDTH)
        graf_y = 0
        if line_y % PRINTING_THRESHOLD == 0:
            print(line_y)
            flat_image.save(OUTPUT_IMAGE_PATH)
        for y in range(height - 1, mid_point[1] - 1, -1):
            for x in range(0, mid_point[0] + 1):
                if line_image.getpixel((x, y)) != LINE_COLOR:
                    continue
                pixel = base_image.getpixel((x, y))
                if pixel is None:
                    pixel = BACKGROUND_COLOR
                flat_image.putpixel((graf_x, graf_y), pixel)
                graf_y += 1
        graf_x += 1
    for line_x in range(0, mid_point[0] + 1):
        line_image = Image.new("RGBA", (width, height), BACKGROUND_COLOR)
        draw = ImageDraw.Draw(line_image)
        line_coords = (mid_point[0], mid_point[1], line_x, height - 1)
        draw.line(line_coords, fill=LINE_COLOR, width=LINE_WIDTH)
        graf_y = 0
        if line_x % PRINTING_THRESHOLD == 0:
            print(line_x)
            flat_image.save(OUTPUT_IMAGE_PATH)
        for y in range(height - 1, mid_point[1] - 1, -1):
            for x in range(0, mid_point[0] + 1):
                if line_image.getpixel((x, y)) != LINE_COLOR:
                    continue
                pixel = base_image.getpixel((x, y))
                if pixel is None:
                    pixel = BACKGROUND_COLOR
                flat_image.putpixel((graf_x, graf_y), pixel)
                graf_y += 1
        graf_x += 1
    for line_x in range(mid_point[0] + 1, width):
        line_image = Image.new("RGBA", (width, height), BACKGROUND_COLOR)
        draw = ImageDraw.Draw(line_image)
        line_coords = (mid_point[0], mid_point[1], line_x, height - 1)
        draw.line(line_coords, fill=LINE_COLOR, width=LINE_WIDTH)
        graf_y = 0
        if line_x % PRINTING_THRESHOLD == 0:
            print(line_x)
            flat_image.save(OUTPUT_IMAGE_PATH)
        for y in range(height - 1, mid_point[1] - 1, -1):
            for x in range(width - 1, mid_point[0] - 1, -1):
                if line_image.getpixel((x, y)) != LINE_COLOR:
                    continue
                pixel = base_image.getpixel((x, y))
                if pixel is None:
                    pixel = BACKGROUND_COLOR
                flat_image.putpixel((graf_x, graf_y), pixel)
                graf_y += 1
        graf_x += 1
    for line_y in range(height - 1, mid_point[1] - 1, -1):
        line_image = Image.new("RGBA", (width, height), BACKGROUND_COLOR)
        draw = ImageDraw.Draw(line_image)
        line_coords = (mid_point[0], mid_point[1], width - 1, line_y)
        draw.line(line_coords, fill=LINE_COLOR, width=LINE_WIDTH)
        graf_y = 0
        if line_y % PRINTING_THRESHOLD == 0:
            print(line_y)
            flat_image.save(OUTPUT_IMAGE_PATH)
        for y in range(height - 1, mid_point[1] - 1, -1):
            for x in range(width - 1, mid_point[0] - 1, -1):
                if line_image.getpixel((x, y)) != LINE_COLOR:
                    continue
                pixel = base_image.getpixel((x, y))
                if pixel is None:
                    pixel = BACKGROUND_COLOR
                flat_image.putpixel((graf_x, graf_y), pixel)
                graf_y += 1
        graf_x += 1
    for line_y in range(mid_point[1], -1, -1):
        line_image = Image.new("RGBA", (width, height), BACKGROUND_COLOR)
        draw = ImageDraw.Draw(line_image)
        line_coords = (mid_point[0], mid_point[1], width - 1, line_y)
        draw.line(line_coords, fill=LINE_COLOR, width=LINE_WIDTH)
        graf_y = 0
        if line_y % PRINTING_THRESHOLD == 0:
            print(line_y)
            flat_image.save(OUTPUT_IMAGE_PATH)
        for y in range(0, mid_point[1] + 1):
            for x in range(width - 1, mid_point[0] - 1, -1):
                if line_image.getpixel((x, y)) != LINE_COLOR:
                    continue
                pixel = base_image.getpixel((x, y))
                if pixel is None:
                    pixel = BACKGROUND_COLOR
                flat_image.putpixel((graf_x, graf_y), pixel)
                graf_y += 1
        graf_x += 1
    for line_x in range(width - 1, mid_point[0] - 1, -1):
        line_image = Image.new("RGBA", (width, height), BACKGROUND_COLOR)
        draw = ImageDraw.Draw(line_image)
        line_coords = (mid_point[0], mid_point[1], line_x, 0)
        draw.line(line_coords, fill=LINE_COLOR, width=LINE_WIDTH)
        graf_y = 0
        if line_x % PRINTING_THRESHOLD == 0:
            print(line_x)
            flat_image.save(OUTPUT_IMAGE_PATH)
        for y in range(0, mid_point[1] + 1):
            for x in range(width - 1, mid_point[0] - 1, -1):
                if line_image.getpixel((x, y)) != LINE_COLOR:
                    continue
                pixel = base_image.getpixel((x, y))
                if pixel is None:
                    pixel = BACKGROUND_COLOR
                flat_image.putpixel((graf_x, graf_y), pixel)
                graf_y += 1
        graf_x += 1
    for line_x in range(mid_point[0], -1, -1):
        line_image = Image.new("RGBA", (width, height), BACKGROUND_COLOR)
        draw = ImageDraw.Draw(line_image)
        line_coords = (mid_point[0], mid_point[1], line_x, 0)
        draw.line(line_coords, fill=LINE_COLOR, width=LINE_WIDTH)
        graf_y = 0
        if line_x % PRINTING_THRESHOLD == 0:
            print(line_x)
            flat_image.save(OUTPUT_IMAGE_PATH)
        for y in range(0, mid_point[1] + 1):
            for x in range(0, mid_point[0] + 1):
                if line_image.getpixel((x, y)) != LINE_COLOR:
                    continue
                pixel = base_image.getpixel((x, y))
                if pixel is None:
                    pixel = BACKGROUND_COLOR
                flat_image.putpixel((graf_x, graf_y), pixel)
                graf_y += 1
        graf_x += 1
    flat_image.save(OUTPUT_IMAGE_PATH)


if __name__ == "__main__":
    main()
