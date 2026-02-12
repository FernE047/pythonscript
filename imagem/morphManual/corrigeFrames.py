from enum import Enum
import os
from PIL import Image
import multiprocessing

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


class Direction(Enum):
    DOWN_RIGHT = 0
    DOWN = 1
    DOWN_LEFT = 2
    LEFT = 3
    UP_LEFT = 4
    UP = 5
    UP_RIGHT = 6
    RIGHT = 7


ORTHOGONAL_DIRECTIONS = (Direction.DOWN, Direction.LEFT, Direction.UP, Direction.RIGHT)


def apply_direction(coord: CoordData | None, direction: Direction) -> CoordData:
    if coord is None:
        raise ValueError("Coordinate cannot be None")
    x, y = coord
    if direction == Direction.DOWN_RIGHT:
        return (x + 1, y + 1)
    if direction == Direction.DOWN:
        return (x, y + 1)
    if direction == Direction.DOWN_LEFT:
        return (x - 1, y + 1)
    if direction == Direction.LEFT:
        return (x - 1, y)
    if direction == Direction.UP_LEFT:
        return (x - 1, y - 1)
    if direction == Direction.UP:
        return (x, y - 1)
    if direction == Direction.UP_RIGHT:
        return (x + 1, y - 1)
    if direction == Direction.RIGHT:
        return (x + 1, y)


def pixelMedio(coord, imagem):
    lista = []
    for direction in range(8):
        coordenada = coordDirecao(coord, direction)
        if coordenada[0] not in range(imagem.size[0]):
            continue
        if coordenada[1] not in range(imagem.size[1]):
            continue
        pixel = imagem.getpixel(coordenada)
        if pixel[3] == 255:
            lista.append(pixel)
    novoPixel = [0 for _ in lista[0]]
    for pixel in lista:
        for n, cor in enumerate(pixel):
            novoPixel[n] += cor
    novoPixel = tuple([int(cor / len(lista)) for cor in novoPixel])
    return novoPixel


def findBorderFreePixels(imagem):
    largura, altura = imagem.size
    freePixels = [[]]
    for x in range(largura):
        if imagem.getpixel((x, 0))[3] == 0:
            freePixels[0].append((x, 0))
        if imagem.getpixel((x, altura - 1))[3] == 0:
            freePixels[0].append((x, altura - 1))
    for y in range(1, altura - 1):
        if imagem.getpixel((0, y))[3] == 0:
            freePixels[0].append((0, y))
        if imagem.getpixel((largura - 1, y))[3] == 0:
            freePixels[0].append((largura - 1, y))
    return freePixels


def findMoreFreePixels(imagem, freePixels):
    candidates = []
    for coord in freePixels[-1]:
        for direction in (1, 3, 4, 6):
            coordenada = coordDirecao(coord, direction)
            if coordenada[0] not in range(imagem.size[0]):
                continue
            if coordenada[1] not in range(imagem.size[1]):
                continue
            pixel = imagem.getpixel(coordenada)
            if pixel[3] == 0:
                if coordenada in freePixels[-1]:
                    continue
                if coordenada in candidates:
                    continue
                if len(freePixels) > 1:
                    if coordenada in freePixels[-2]:
                        continue
                candidates.append(coordenada)
    if candidates:
        freePixels.append(candidates)
        findMoreFreePixels(imagem, freePixels)


def hasPontosProximos(imagem, ponto):
    for d in (1, 3, 4, 6):
        if imagem.getpixel(coordDirecao(ponto, d))[3] == 255:
            return True
    return False


def findHoleBorder(imagem, freePixels):
    largura, altura = imagem.size
    pontos = []
    for x in range(largura):
        isUltimoPixelTransparent = imagem.getpixel((x, 0))[3] == 0
        for y in range(altura):
            isPixelAtualTransparent = imagem.getpixel((x, y))[3] == 0
            if (not isUltimoPixelTransparent) and isPixelAtualTransparent:
                if (x, y) not in freePixels:
                    if (x, y) not in pontos:
                        pontos.append((x, y))
            if (not isPixelAtualTransparent) and isUltimoPixelTransparent:
                if (x, y - 1) not in freePixels:
                    if (x, y - 1) not in pontos:
                        pontos.append((x, y - 1))
            isUltimoPixelTransparent = isPixelAtualTransparent
    for y in range(altura):
        isUltimoPixelTransparent = imagem.getpixel((0, y))[3] == 0
        for x in range(largura):
            isPixelAtualTransparent = imagem.getpixel((x, y))[3] == 0
            if (not isUltimoPixelTransparent) and isPixelAtualTransparent:
                if (x, y) not in freePixels:
                    if (x, y) not in pontos:
                        pontos.append((x, y))
            if (not isPixelAtualTransparent) and isUltimoPixelTransparent:
                if (x - 1, y) not in freePixels:
                    if (x - 1, y) not in pontos:
                        pontos.append((x - 1, y))
            isUltimoPixelTransparent = isPixelAtualTransparent
    return pontos


def findHoleContinuation(imagem, trappedPixels, freePixels):
    largura, altura = imagem.size
    pontos = []
    for pixel in trappedPixels:
        for d in (1, 3, 4, 6):
            coord = coordDirecao(pixel, d)
            if coord not in freePixels:
                if coord not in pontos:
                    if imagem.getpixel(coord)[3] == 0:
                        pontos.append(coord)
    return pontos


def fixTrappedPixels(imagem:Image.Image, freePixels:list[tuple[int, ...]|float|int]) -> None:  # make it better
    trappedPixels = findHoleBorder(imagem, freePixels)
    while trappedPixels:
        for coordenada in trappedPixels:
            imagem.putpixel(coordenada, pixelMedio(coordenada, imagem))
        trappedPixels = findHoleContinuation(imagem, trappedPixels, freePixels)


def corrigeFrame(indice):
    print("corregindo Frame : " + str(indice))
    nome = f"C:\\pythonscript\\imagem\\morphManual\\frames\\frame{indice:03d}.png"
    imagem = Image.open(nome)
    largura, altura = imagem.size
    freePixels = findBorderFreePixels(imagem)
    findMoreFreePixels(imagem, freePixels)
    allFreePixels = []
    for camada in freePixels:
        for coord in camada:
            allFreePixels.append(coord)
    fixTrappedPixels(imagem, allFreePixels)
    imagem.save(nome)
    imagem.close()
    print("\tFrame corrigido : " + str(indice))


def main() -> None:
    quantiaFrames = len(os.listdir("C:\\pythonscript\\imagem\\morphManual\\frames"))
    p = multiprocessing.Pool(os.cpu_count())
    p.map(corrigeFrame, range(1, quantiaFrames - 1))


if __name__ == "__main__":
    main()