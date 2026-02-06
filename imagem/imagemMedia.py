from PIL import Image

IMAGE_A = "a.jpg"
IMAGE_B = "b.jpg"
OUTPUT_IMAGE = "c8.jpg"
BACKGROUND_COLOR = (255, 255, 255)


def get_pixel(imagem: Image.Image, coord: tuple[int, int]) -> tuple[int, ...]:
    pixel = imagem.getpixel(coord)
    if pixel is None:
        return BACKGROUND_COLOR
    if not isinstance(pixel, tuple):
        pixel_int = int(pixel)
        return (pixel_int, pixel_int, pixel_int)
    return pixel


def get_average_pixel(
    pixel_a: tuple[int, ...], pixel_b: tuple[int, ...]
) -> tuple[int, ...]:
    new_pixel: list[int] = []
    for a, b in zip(pixel_a, pixel_b):
        new_pixel.append(int((a + b) / 2))
    return tuple(new_pixel)


def main() -> None:
    image_a = Image.open(IMAGE_A)
    image_b = Image.open(IMAGE_B)
    width_a, height_a = image_a.size
    width_b, height_b = image_b.size
    width = min(width_a, width_b)
    height = min(height_a, height_b)
    faixa = Image.new("RGB", (width, height), BACKGROUND_COLOR)
    for x in range(width):
        for y in range(height):
            pixel_a = get_pixel(image_a, (x, y))
            pixel_b = get_pixel(image_b, (x, y))
            average_pixel = get_average_pixel(pixel_a, pixel_b)
            faixa.putpixel((x, y), average_pixel)
    faixa.save(OUTPUT_IMAGE)
    print(f"Average image created and saved as {OUTPUT_IMAGE}")


if __name__ == "__main__":
    main()
