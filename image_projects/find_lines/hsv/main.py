from PIL import Image
from colorsys import rgb_to_hsv

BACKGROUND_COLOR = (255, 255, 255, 255)
HIGHLIGHT_COLOR = (0, 0, 0, 255)
VALUE_THRESHOLD_MULTIPLIER = 10
OUTPUT_IMAGE_COUNT = 5
INPUT_IMAGE_COUNT = 1


def get_pixel(imagem: Image.Image, x: int, y: int) -> tuple[int, ...]:
    pixel = imagem.getpixel((x, y))
    if pixel is None:
        return BACKGROUND_COLOR
    if not isinstance(pixel, tuple):
        pixel_int = int(pixel)
        return (pixel_int, pixel_int, pixel_int, 255)
    return pixel


def get_hsv_value_difference(
    pixel_a: tuple[int, ...], pixel_b: tuple[int, ...]
) -> float:
    hsv_a = rgb_to_hsv(pixel_a[0], pixel_a[1], pixel_a[2])
    hsv_b = rgb_to_hsv(pixel_b[0], pixel_b[1], pixel_b[2])
    return abs(hsv_a[2] - hsv_b[2])


def open_image_as_rgba(image_path: str) -> Image.Image:
    with Image.open(image_path) as image:
        image_in_memory = image.copy()
        if image.mode != "RGBA":
            return image_in_memory.convert("RGBA")
        return image_in_memory


def main() -> None:
    for input_index in range(INPUT_IMAGE_COUNT):
        input_name = f"A{input_index:03d}0.jpg"
        imagem = open_image_as_rgba(input_name)
        width, height = imagem.size
        print(f"\nimage {input_name} size: {imagem.size}\n")
        for output_index in range(1, OUTPUT_IMAGE_COUNT + 1):
            output_image = Image.new("RGBA", imagem.size, BACKGROUND_COLOR)
            for y in range(height):
                for x in range(width):
                    current_pixel = get_pixel(imagem, x, y)
                    neighbor_pixels: list[tuple[int, ...]] = []
                    if x > 0:
                        neighbor_pixels.append(get_pixel(imagem, x - 1, y))
                    if x < width - 1:
                        neighbor_pixels.append(get_pixel(imagem, x + 1, y))
                    if y > 0:
                        neighbor_pixels.append(get_pixel(imagem, x, y - 1))
                    if y < height - 1:
                        neighbor_pixels.append(get_pixel(imagem, x, y + 1))
                    for pixel in neighbor_pixels:
                        value_difference = get_hsv_value_difference(
                            pixel, current_pixel
                        )
                        if value_difference > VALUE_THRESHOLD_MULTIPLIER * output_index:
                            output_image.putpixel((x, y), HIGHLIGHT_COLOR)
                            break
            output_name = f"A{input_index:03d}{output_index:01d}.png"
            output_image.save(output_name)
            print(f"{output_name} was created")


if __name__ == "__main__":
    main()
