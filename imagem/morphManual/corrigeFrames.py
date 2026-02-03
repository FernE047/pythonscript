import os
from PIL import Image
import multiprocessing


def coordDirecao(coord, n):
    if n > 7:
        n = n % 8
    x, y = coord
    if n == 0:
        return (x + 1, y + 1)
    if n == 1:
        return (x, y + 1)
    if n == 2:
        return (x - 1, y + 1)
    if n == 3:
        return (x + 1, y)
    if n == 4:
        return (x - 1, y)
    if n == 5:
        return (x + 1, y - 1)
    if n == 6:
        return (x, y - 1)
    if n == 7:
        return (x - 1, y - 1)
    return (x, y)


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


def fixTrappedPixels(imagem, freePixels):  # make it better
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