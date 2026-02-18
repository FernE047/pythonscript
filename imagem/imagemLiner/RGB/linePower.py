from math import sqrt
from PIL import Image

BACKGROUND_COLOR = (255, 255, 255, 255)
HIGHLIGHT_COLOR = (0, 0, 0, 255)
MAX_BRIGHTNESS = 255
VALUE_THRESHOLD_MULTIPLIER = 10
INPUT_IMAGE_COUNT = 1
TOTAL_COLOR_CHANNELS = 3
MAX_DISTANCE_BETWEEN_PIXELS = sqrt(MAX_BRIGHTNESS**2 * TOTAL_COLOR_CHANNELS)


def get_pixel(imagem: Image.Image, coord: tuple[int, int]) -> tuple[int, ...]:
    pixel = imagem.getpixel(coord)
    if pixel is None:
        return BACKGROUND_COLOR
    if not isinstance(pixel, tuple):
        pixel_int = int(pixel)
        return (pixel_int, pixel_int, pixel_int, MAX_BRIGHTNESS)
    return pixel


def euclidean_distance_between_pixels(
    pixel_a: tuple[int, ...], pixel_b: tuple[int, ...]
) -> float:
    total_squared_distance = 0.0
    for color_channel in range(TOTAL_COLOR_CHANNELS):
        channel_distance = abs(pixel_a[color_channel] - pixel_b[color_channel])
        total_squared_distance += channel_distance**2
    return sqrt(total_squared_distance)


def open_image_as_rgba(image_path: str) -> Image.Image:
    with Image.open(image_path) as image:
        image_in_memory = image.copy()
        if image.mode != "RGBA":
            return image_in_memory.convert("RGBA")
        return image_in_memory


def main() -> None:
    for input_index in range(1, INPUT_IMAGE_COUNT + 1):
        input_name = f"A{input_index:03d}_source.jpg"
        image = open_image_as_rgba(input_name)
        width, height = image.size
        print(f"\nimage {input_name} size: {image.size}\n")
        output_image = Image.new("RGBA", image.size, BACKGROUND_COLOR)
        for y in range(height):
            for x in range(width):
                current_pixel = get_pixel(image, (x, y))
                cumulative_distance: list[float] = []
                if x > 0:
                    coord = (x - 1, y)
                    neighbor_pixel = get_pixel(image, coord)
                    distance = euclidean_distance_between_pixels(
                        neighbor_pixel, current_pixel
                    )
                    cumulative_distance.append(distance)
                if x < width - 1:
                    coord = (x + 1, y)
                    neighbor_pixel = get_pixel(image, coord)
                    distance = euclidean_distance_between_pixels(
                        neighbor_pixel, current_pixel
                    )
                    cumulative_distance.append(distance)
                if y > 0:
                    coord = (x, y - 1)
                    neighbor_pixel = get_pixel(image, coord)
                    distance = euclidean_distance_between_pixels(
                        neighbor_pixel, current_pixel
                    )
                    cumulative_distance.append(distance)
                if y < height - 1:
                    coord = (x, y + 1)
                    neighbor_pixel = get_pixel(image, coord)
                    distance = euclidean_distance_between_pixels(
                        neighbor_pixel, current_pixel
                    )
                    cumulative_distance.append(distance)
                average_distance = sum(cumulative_distance) / len(cumulative_distance)
                distance_normalized = average_distance / MAX_DISTANCE_BETWEEN_PIXELS
                color = int((1 - distance_normalized) * MAX_BRIGHTNESS)
                pixel_color = (color, color, color, MAX_BRIGHTNESS)
                output_image.putpixel((x, y), pixel_color)
        output_name = f"A{input_index:03d}_output.png"
        output_image.save(output_name)
        print(f"{output_name} was created")


if __name__ == "__main__":
    main()
