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


def open_image_as_rgb(image_path: str) -> Image.Image:
    with Image.open(image_path) as image:
        image_in_memory = image.copy()
        if image.mode != "RGB":
            return image_in_memory.convert("RGB")
        return image_in_memory

def main() -> None:
    input_image = open_image_as_rgb(INPUT_IMAGE)
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
            if red > green:
                if red > blue:
                    faixa.putpixel(coord, RED)
                elif red < blue:
                    faixa.putpixel(coord, BLUE)
                else:
                    faixa.putpixel(coord, MAGENTA)
            elif red < green:
                if green > blue:
                    faixa.putpixel(coord, GREEN)
                elif green < blue:
                    faixa.putpixel(coord, BLUE)
                else:
                    faixa.putpixel(coord, CYAN)
            else:
                if red > blue:
                    faixa.putpixel(coord, YELLOW)
                elif red < blue:
                    faixa.putpixel(coord, BLUE)
                else:
                    faixa.putpixel(coord, WHITE)
            
    faixa.save("bContraste.jpg")
    print("veja")


if __name__ == "__main__":
    main()