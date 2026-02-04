from PIL import Image

CoordData = tuple[int, int]
PixelData = tuple[CoordData, int]

MAX_SIZE = 11
WHITE = (255, 255, 255, 255)
SEMI_WHITE = (254, 254, 254, 255)


def get_pixel_first_channel(image: Image.Image, coords: CoordData) -> int:
    # all channels are assumed to have the same value in this context
    pixel = image.getpixel(coords)
    if isinstance(pixel, int):
        return pixel
    if isinstance(pixel, float):
        return int(pixel)
    if isinstance(pixel, tuple):
        if len(pixel) >= 3:
            return pixel[0]
        if len(pixel) >= 1:
            return pixel[0]
    return 0


def get_pixels_neighborable(img: Image.Image) -> list[PixelData]:
    tamanho = img.size[0]
    pixel_with_neighbors: list[PixelData] = []
    for x in range(tamanho):
        for y in range(tamanho):
            if get_pixel_first_channel(img, (x, y)) == 255:
                neighbor_pixel_differences = [0, 0, 0, 0]
                if x == 0:
                    continue
                neighbor_pixel_differences[0] = 255 - get_pixel_first_channel(
                    img, (x - 1, y)
                )
                if x == tamanho - 1:
                    continue
                neighbor_pixel_differences[1] = 255 - get_pixel_first_channel(
                    img, (x + 1, y)
                )
                if y == 0:
                    continue
                neighbor_pixel_differences[2] = 255 - get_pixel_first_channel(
                    img, (x, y - 1)
                )
                if y == tamanho - 1:
                    continue
                neighbor_pixel_differences[3] = 255 - get_pixel_first_channel(
                    img, (x, y + 1)
                )
                value = 255 - sum(neighbor_pixel_differences) // 4
                pixel_with_neighbors.append(((x, y), value))
    return pixel_with_neighbors


def main() -> None:
    blur_image = Image.new("RGBA", (MAX_SIZE, MAX_SIZE), WHITE)
    midway = MAX_SIZE // 2
    blur_image.putpixel((midway, midway), SEMI_WHITE)
    while get_pixel_first_channel(blur_image, (0, 0)) == 255:
        pixels_with_neighbors = get_pixels_neighborable(blur_image)
        for pixel_info in pixels_with_neighbors:
            coords, color_value = pixel_info
            color = (color_value, color_value, color_value, 255)
            blur_image.putpixel(coords, color)
    blur_image.save("blur.png")


if __name__ == "__main__":
    main()
