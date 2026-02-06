from PIL import Image

INPUT_IMAGE = "b.jpg"
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)

CoordData = tuple[int, int]

def get_pixel(image: Image.Image, coord: CoordData) -> tuple[int, int, int]:
    pixel = image.getpixel(coord)
    if pixel is None:
        raise ValueError("Pixel not found")
    if isinstance(pixel, int):
        raise ValueError("Image is not in RGB mode")
    if isinstance(pixel, float):
        raise ValueError("Image is not in RGB mode")
    if len(pixel) < 3:
        raise ValueError("Image is not in RGB mode")
    return pixel[0], pixel[1], pixel[2]

def main() -> None:
    input_image = Image.open(INPUT_IMAGE)
    size = input_image.size
    width, height = size
    faixa = Image.new("RGB", size, "white")
    for x in range(width):
        for y in range(height):
            coord = (x, y)
            pixel = get_pixel(input_image, coord)
            red = pixel[0]
            green = pixel[1]
            blue = pixel[2]
            if red == green:
                if red == blue:
                    faixa.putpixel(coord, WHITE)
                elif red > blue:
                    faixa.putpixel(coord, YELLOW)
                else:
                    faixa.putpixel(coord, BLUE)
            elif red == blue:
                if red > green:
                    faixa.putpixel(coord, MAGENTA)
                else:
                    faixa.putpixel(coord, GREEN)
            elif green == blue:
                if green > red:
                    faixa.putpixel(coord, CYAN)
                else:
                    faixa.putpixel(coord, RED)
            elif green > blue:
                if green > red:
                    faixa.putpixel(coord, GREEN)
                else:
                    faixa.putpixel(coord, RED)
            elif blue > green:
                if blue > red:
                    faixa.putpixel(coord, BLUE)
                else:
                    faixa.putpixel(coord, RED)
            else:
                faixa.putpixel(coord, BLACK)
    faixa.save("bContraste.jpg")
    print("veja")


if __name__ == "__main__":
    main()