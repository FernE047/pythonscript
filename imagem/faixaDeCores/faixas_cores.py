from PIL import Image
import os


def main() -> None:
    os.chdir("faixas")
    for index in range(1, 11):
        input_image = Image.open(f"a{index}.jpg")
        size = input_image.size
        width, height = input_image.size
        base_image = Image.new("RGB", size, "white")
        faixa = (base_image, base_image.copy(), base_image.copy())
        for x in range(width):
            for y in range(height):
                pixel_source = input_image.getpixel((x, y))
                if not isinstance(pixel_source, tuple) or len(pixel_source) < 3:
                    raise ValueError(f"Invalid pixel data at coordinate: {(x, y)}")
                pixel_red = (255, pixel_source[0], pixel_source[0])
                pixel_green = (pixel_source[1], 255, pixel_source[1])
                pixel_blue = (pixel_source[2], pixel_source[2], 255)
                faixa[0].putpixel((x, y), pixel_red)
                faixa[1].putpixel((x, y), pixel_green)
                faixa[2].putpixel((x, y), pixel_blue)
        faixa[0].save(f"b{index}-red.jpg")
        faixa[1].save(f"b{index}-green.jpg")
        faixa[2].save(f"b{index}-blue.jpg")
        print(index)


if __name__ == "__main__":
    main()
