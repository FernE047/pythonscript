from PIL import Image

# this code is legacy, I am only changing type hints and linter errors. it doesn't make sense to refactor it, since I already have a better version of it, and I don't want to break it by changing it too much

CoordData = tuple[int, int]


def get_pixel(image: Image.Image, coord: CoordData) -> tuple[int, ...]:
    pixel = image.getpixel(coord)
    if pixel is None:
        raise ValueError("Pixel not found")
    if isinstance(pixel, int):
        raise ValueError("Image is not in RGBA mode")
    if isinstance(pixel, float):
        raise ValueError("Image is not in RGBA mode")
    if len(pixel) < 4:
        raise ValueError("Image is not in RGBA mode")
    return pixel


def open_image_as_rgba(image_path: str) -> Image.Image:
    with Image.open(image_path) as image:
        image_in_memory = image.copy()
        if image.mode != "RGBA":
            return image_in_memory.convert("RGBA")
        return image_in_memory


def main() -> None:
    imagemInicial = open_image_as_rgba("./inicial.png")
    imagemFinal = Image.new("RGBA", imagemInicial.size, (0, 0, 0, 0))
    with open("./config.txt", "r", encoding="utf-8") as file:
        linha = file.readline()
        while linha:
            coords = [
                (int(coord.split(",")[0]), int(coord.split(",")[1]))
                for coord in linha.split(" ")
            ]
            coordInicial = coords[0]
            coordFinal = coords[1]
            cor = get_pixel(imagemInicial, coordInicial)
            imagemFinal.putpixel(coordFinal, cor)
            linha = file.readline()
        imagemFinal.save("./final.png")


if __name__ == "__main__":
    main()
