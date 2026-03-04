from PIL import Image

IMAGE_INPUT = "input.jpg"
THRESHOLD = 20
MAX_BRIGHTNESS = 255
MAX_THRESHOLD = MAX_BRIGHTNESS * 3 - THRESHOLD
HIGHLIGHT_COLOR = (0, 0, 0)
BACKGROUND_COLOR = (255, 255, 255)
IMAGE_OUTPUT = "output.jpg"


def open_image_as_rgb(image_path: str) -> Image.Image:
    with Image.open(image_path) as image:
        image_in_memory = image.copy()
        if image.mode != "RGB":
            return image_in_memory.convert("RGB")
        return image_in_memory


def main() -> None:
    print(IMAGE_INPUT)
    image = open_image_as_rgb(IMAGE_INPUT)
    width, height = image.size
    output_image = image.copy()
    for x in range(width):
        for y in range(height):
            pixel = image.getpixel((x, y))
            if not isinstance(pixel, tuple) or len(pixel) != 3:
                continue
            color_intensity_sum = sum(pixel)
            if color_intensity_sum >= MAX_THRESHOLD:
                output_image.putpixel((x, y), HIGHLIGHT_COLOR)
            else:
                output_image.putpixel((x, y), BACKGROUND_COLOR)
    output_image.save(IMAGE_OUTPUT)


if __name__ == "__main__":
    main()
