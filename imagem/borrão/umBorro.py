from PIL import Image

CoordData = tuple[int, int]
PixelData = tuple[CoordData, int]


def get_pixel_green_channel(image: Image.Image, coords: CoordData) -> int:
    pixel = image.getpixel(coords)
    if isinstance(pixel, int):
        return pixel
    if isinstance(pixel, float):
        return int(pixel)
    if isinstance(pixel, tuple):
        if len(pixel) >= 3:
            return pixel[1]
        if len(pixel) >= 1:
            return pixel[0]
    return 0


def get_pixels_neighborable(img: Image.Image) -> list[PixelData]:
    tamanho = img.size[0]
    pixel_with_neighbors: list[PixelData] = []
    for x in range(tamanho):
        for y in range(tamanho):
            if get_pixel_green_channel(img, (x, y)) == 255:
                direcoes = [0, 0, 0, 0]
                if x == 0:
                    continue
                direcoes[0] = 255 - get_pixel_green_channel(img, (x - 1, y))
                if x == tamanho - 1:
                    continue
                direcoes[1] = 255 - get_pixel_green_channel(img, (x + 1, y))
                if y == 0:
                    continue
                direcoes[2] = 255 - get_pixel_green_channel(img, (x, y - 1))
                if y == tamanho - 1:
                    continue
                direcoes[3] = 255 - get_pixel_green_channel(img, (x, y + 1))
                valor = 255 - sum(direcoes) // 4
                pixel_with_neighbors.append(((x, y), valor))
    return pixel_with_neighbors


def main() -> None:
    blur_image = Image.new("RGBA", (11, 11), (255, 255, 255, 255))
    blur_image.putpixel((5, 5), (254, 254, 254, 255))
    while get_pixel_green_channel(blur_image, (0, 0)) == 255:
        pixels_with_neighbors = get_pixels_neighborable(blur_image)
        for pixel_info in pixels_with_neighbors:
            coords, color_value = pixel_info
            blur_image.putpixel(coords, (color_value, color_value, color_value, 255))
    blur_image.save("blur.png")


if __name__ == "__main__":
    main()
