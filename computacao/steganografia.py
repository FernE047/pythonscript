import os
from typing import List, cast
from PIL import Image
import copy
from PIL.ImageFile import ImageFile


def calculate_usable_dimensions(img: ImageFile) -> tuple[int, int]:
    width, height = img.size
    if width % 2 == 1:
        width -= 1
    if height % 2 == 1:
        height -= 1
    return (width, height)


def is_image_hidable(img_to_hide: ImageFile, img_source: ImageFile) -> bool:
    width_src, height_src = calculate_usable_dimensions(img_source)
    width_hide, height_hide = img_to_hide.size
    if (height_hide <= height_src / 2) and (width_hide <= width_src / 2):
        return True
    print("image to hide is too big for the source image")
    return False


def open_image_by_name(message: str) -> ImageFile:
    while True:
        try:
            print(message)
            user_input = input()
            if user_input.find("/") == -1:
                return Image.open(os.path.join("./images", user_input))
            return Image.open(user_input)
        except Exception as _:
            print("invalid name")


def viraDec(binary_input: str) -> int:
    if binary_input == "00":
        return 0
    elif binary_input == "01":
        return 1
    elif binary_input == "10":
        return 2
    else:
        return 3


def hide_image(img_to_hide: ImageFile, img_source: ImageFile) -> ImageFile:
    img_stego = copy.deepcopy(img_source)
    width_hide, height_hide = img_to_hide.size
    for y in range(height_hide):
        for x in range(width_hide):
            pixel = img_to_hide.getpixel((x, y))
            assert isinstance(pixel, tuple) and len(pixel) == 3, (
                "Pixel must be an RGB tuple"
            )
            pixel_to_hide = convert_pixel_to_binary(pixel)
            posicoes = (
                (2 * x, 2 * y),
                (2 * x + 1, 2 * y),
                (2 * x, 2 * y + 1),
                (2 * x + 1, 2 * y + 1),
            )
            pixel_source = cast(
                List[tuple[int, int, int]],
                [img_source.getpixel(coord) for coord in posicoes],
            )
            assert all(isinstance(p, tuple) and len(p) == 3 for p in pixel_source), (
                "All pixels must be RGB tuples"
            )
            pixel_stego = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
            for color_channel_index in range(3):
                for bit_index in range(4):
                    pixel_stego[bit_index][color_channel_index] = (
                        pixel_source[bit_index][color_channel_index]
                        - (pixel_source[bit_index][color_channel_index] % 4)
                        + viraDec(pixel_to_hide[color_channel_index][bit_index])
                    )
            for indice in range(4):
                img_stego.putpixel(posicoes[indice], tuple(pixel_stego[indice]))
        print(y)
    return img_stego


def convert_pixel_to_binary(pixel: tuple[int, int, int]) -> list[list[str]]:
    pixel_to_hide = [["0", "0", "0", "0"], ["0", "0", "0", "0"], ["0", "0", "0", "0"]]
    for color_index in range(3):
        for bit_pair_index in range(4):
            binary_representation = bin(pixel[color_index])
            binary_string = binary_representation[2:]
            binary_string_value = str(binary_string)
            pixel_integer = int(binary_string_value)
            binary_padded_value = f"{pixel_integer:08d}"
            bit_segment = binary_padded_value[
                2 * bit_pair_index : 2 * bit_pair_index + 2
            ]
            pixel_to_hide[color_index][bit_pair_index] = bit_segment
    return pixel_to_hide


def main() -> None:
    source_image = open_image_by_name("enter the name of the original image")
    image_to_hide = open_image_by_name("enter the name of the image to hide")
    while not (is_image_hidable(image_to_hide, source_image)):
        image_to_hide = open_image_by_name("enter the name of the image to hide")
    stego_image = hide_image(image_to_hide, source_image)
    filename = os.path.join("output_steg.jpg")
    print(f"saving stego image as {filename}")
    stego_image.save(filename)


if __name__ == "__main__":
    main()
