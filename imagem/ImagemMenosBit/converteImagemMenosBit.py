from PIL import Image

IMAGE_COUNT = 2
TOTAL_BITS = 8
MAX_BIT_VALUE = 256
DEFAULT_COLOR = (0, 0, 0)
COLOR_CHANNELS = 3


def open_image_as_rgba(image_path: str) -> Image.Image:
    with Image.open(image_path) as image:
        image_in_memory = image.copy()
        if image.mode != "RGBA":
            return image_in_memory.convert("RGBA")
        return image_in_memory


def main() -> None:
    for input_index in range(IMAGE_COUNT):
        input_name = f"A{input_index:03d}.png"
        image = open_image_as_rgba(input_name)
        size = image.size
        width, height = size
        print(f"\nimage {input_name} size: {size}\n")
        for bit in range(1, TOTAL_BITS):
            output_image = Image.new("RGBA", size)
            bit_position = 2**bit
            divisor = MAX_BIT_VALUE / bit_position
            scaling_factor = (MAX_BIT_VALUE - 1) / (bit_position - 1)
            for y in range(height):
                for x in range(width):
                    coord = (x, y)
                    input_pixel = image.getpixel(coord)
                    if input_pixel is None:
                        input_pixel = DEFAULT_COLOR
                    if not isinstance(input_pixel, tuple):
                        pixel_int = int(input_pixel)
                        input_pixel = (pixel_int, pixel_int, pixel_int)
                    output_pixel = list(input_pixel)
                    for channel_index in range(COLOR_CHANNELS):
                        color_normalized = input_pixel[channel_index] // divisor
                        output_pixel[channel_index] = int(
                            color_normalized * scaling_factor
                        )
                    output_image.putpixel(coord, tuple(output_pixel))
            output_name = f"A{input_index:03d}{bit:01d}.png"
            output_image.save(output_name)
            print(f"finalizado {output_name}\n")


if __name__ == "__main__":
    main()
