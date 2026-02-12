from PIL import Image
from time import time

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


def funcaoAfim(inicio, fim, total, n):
    elemento = []
    for elementoInicial, elementoFinal in zip(inicio, fim):
        B = elementoInicial
        A = (elementoFinal - elementoInicial) / (total + 1)
        elemento.append(int(A * n + B))
    return tuple(elemento)


def main() -> None:
    imagemInicial = Image.open("./inicial.png")
    imagemFinal = Image.new("RGBA", imagemInicial.size, (0, 0, 0, 0))
    with open("./config.txt", "r", encoding="utf-8") as file:
        linha = file.readline()
        while linha:
            coords = [
                tuple([int(b) for b in coord.split(",")]) for coord in linha.split(" ")
            ]
            coordInicial = coords[0]
            coordFinal = coords[1]
            cor = imagemInicial.getpixel(coordInicial)
            imagemFinal.putpixel(coordFinal, cor)
            linha = file.readline()
        imagemFinal.save("./final.png")
    imagemInicial.close()
    imagemFinal.close()


if __name__ == "__main__":
    main()
