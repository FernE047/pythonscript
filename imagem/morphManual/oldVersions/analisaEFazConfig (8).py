from io import TextIOWrapper
from typing import Literal
from PIL import Image
import os
import multiprocessing
from random import randint
import pypdn  # type: ignore

# pypdn doesn't have type hints, so I ignore it.
from enum import Enum

CoordData = tuple[int, int]

# this code is legacy, I am only changing type hints and linter errors. it doesn't make sense to refactor it, since I already have a better version of it, and I don't want to break it by changing it too much


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


"""

SECÇÃO UTILITARIOS DO MAIN:

ferramentas utilizadas pelo main

"""


def hasColor(imagem: Image.Image) -> tuple[bool, Literal[False] | CoordData]:
    largura, altura = imagem.size
    hasGreen = False
    hasBlue: Literal[False] | CoordData = False
    for x in range(largura):
        for y in range(altura):
            pixel = get_pixel(imagem, (x, y))
            if pixel[3] == 0:
                continue
            if pixel[1] != 0:
                hasGreen = True
                if hasBlue:
                    return (hasGreen, hasBlue)
                else:
                    continue
            if pixel[2] == 200:
                hasBlue = (x, y)
                if hasGreen:
                    return (hasGreen, hasBlue)
    return (hasGreen, hasBlue)


def limpaPasta(pasta: str) -> None:
    arquivos = [f"{pasta}/{a}" for a in os.listdir(pasta)]
    if "./frames/resized" in arquivos:
        arquivos.pop(arquivos.index("./frames/resized"))
    for arquivo in arquivos:
        os.remove(arquivo)


"""

SECÇÃO DE DIREÇÃO:

possui funções que funcionam com direções apontadas pela secção azul

"""


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


"""

SECÇÃO AZUL:

linhas que se iniciam no tom 200 e continuam no tom 255

"""


def procuraAzulInicial(imagem: Image.Image) -> CoordData:
    largura, altura = imagem.size
    for x in range(largura):
        for y in range(altura):
            pixel = get_pixel(imagem, (x, y))
            if pixel[3] == 0:
                continue
            if pixel[2] == 200:
                return (x, y)
    return (-1, -1)


def procuraLinhaAzul(
    imagem: Image.Image,
    anteriores: list[CoordData] | None = None,
    inicio: CoordData | None = None,
) -> list[CoordData]:
    if anteriores is None:
        if inicio is None:
            anteriores = [procuraAzulInicial(imagem)]
        else:
            anteriores = [inicio]
    linha = anteriores.copy()
    pontoInicial = anteriores[-1]
    anteriores = None
    while True:
        pontos: list[CoordData] = []
        for d in Direction:
            pontoAtual = apply_direction(pontoInicial, d)
            if pontoAtual not in linha:
                try:
                    pixel = get_pixel(imagem, pontoAtual)
                    if pixel[3] == 0:
                        continue
                    if pixel[2] == 255:
                        pontos.append(pontoAtual)
                except Exception:
                    pass
        if len(pontos) == 0:
            return linha
        elif len(pontos) == 1:
            pontoInicial = pontos[0]
            linha.append(pontoInicial)
        else:
            linhaMaxima = linha.copy()
            for ponto in pontos:
                novaLinha = procuraLinhaAzul(imagem, anteriores=linha + [ponto])
                if len(novaLinha) > len(linhaMaxima):
                    linhaMaxima = novaLinha.copy()
            return linhaMaxima


"""

SECÇÃO VERDE:

Regiões que sejam 2D, chamadas de blob
cada Blob possui camadas que são conjuntos de coordenadas

"""


def procuraContornoVerde(imagem: Image.Image) -> list[CoordData]:
    contorno: list[CoordData] = []
    largura, altura = imagem.size
    elementoAtual = False
    for y in range(altura):
        ultimoElemento = False
        for x in range(largura):
            elementoAtual = get_pixel(imagem, (x, y))[3] == 255
            if (not ultimoElemento) and elementoAtual:
                if (x, y) not in contorno:
                    contorno.append((x, y))
            if (not elementoAtual) and ultimoElemento:
                if (x - 1, y) not in contorno:
                    contorno.append((x - 1, y))
            ultimoElemento = elementoAtual
        if elementoAtual:
            if (largura - 1, y) not in contorno:
                contorno.append((largura - 1, y))
    for x in range(largura):
        ultimoElemento = False
        for y in range(altura):
            elementoAtual = get_pixel(imagem, (x, y))[3] == 255
            if (not ultimoElemento) and elementoAtual:
                if (x, y) not in contorno:
                    contorno.append((x, y))
            if (not elementoAtual) and ultimoElemento:
                if (x, y - 1) not in contorno:
                    contorno.append((x, y - 1))
            ultimoElemento = elementoAtual
        if elementoAtual:
            if (x, altura - 1) not in contorno:
                contorno.append((x, altura - 1))
    return ordenaLinha(contorno)


def isCoordInBlob(coordTeste: CoordData, blob: list[list[CoordData]]) -> bool:
    for camada in blob:
        for coord in camada:
            if coordTeste == coord:
                return True
    return False


def procuraBlob(imagem: Image.Image, blob: list[list[CoordData]]) -> None:
    linhaAtual: list[CoordData] = []
    linhaAnterior = blob[-1]
    for coord in linhaAnterior:
        for direcao in ORTHOGONAL_DIRECTIONS:
            coordenada = apply_direction(coord, direcao)
            try:
                pixel = get_pixel(imagem, coordenada)
            except Exception:
                continue
            if pixel[3] != 0:
                if pixel[1] == 255:
                    if coordenada not in linhaAtual:
                        if not isCoordInBlob(coordenada, blob):
                            linhaAtual.append(coordenada)
    if len(linhaAtual) > 0:
        linhaAtual = ordenaLinha(linhaAtual)
        if linhaAtual not in blob:
            blob.append(linhaAtual)
            procuraBlob(imagem, blob)


def ordenaLinha(linhaOriginal: list[CoordData]) -> list[CoordData]:
    linhaTotal: list[CoordData] = []
    linhas = divideLinha(linhaOriginal)
    for linha in linhas:
        linhaTotal += ordenaLinhaInd(linha)
    return linhaTotal


def divideLinha(original_linha: list[CoordData]) -> list[list[CoordData]]:
    linhas: list[list[CoordData]] = []
    for ponto in original_linha:
        linhasAppend: list[int] = []
        for i, linha in enumerate(linhas):
            for novoPonto in linha:
                if distancia(ponto, novoPonto) <= 2 ** (1 / 2) + 0.01:
                    linhasAppend.append(i)
                    break
        if len(linhasAppend) == 0:
            linhas.append([ponto])
        elif len(linhasAppend) == 1:
            linhas[linhasAppend[0]].append(ponto)
        else:
            superLinha: list[CoordData] = []
            for i in linhasAppend:
                superLinha += linhas[i].copy()
            for i in reversed(sorted(linhasAppend)):
                linhas.pop(i)
            superLinha.append(ponto)
            linhas.append(superLinha)
    return linhas


def ordenaLinhaInd(linha: list[CoordData]) -> list[CoordData]:
    tamanho = len(linha)
    maiorLinha: list[CoordData] = []
    for n in range(tamanho):
        linhaTeste = linha.copy()
        primeiroPonto = linha[n]
        linhaTeste = ordenaLinhaIt(linhaTeste, inicio=primeiroPonto)
        if len(linhaTeste) == tamanho:
            return linhaTeste
        if len(linhaTeste) > len(maiorLinha):
            maiorLinha = linhaTeste.copy()
    return maiorLinha


def ordenaLinhaIt(
    linhaDesordenada: list[CoordData],
    anteriores: list[CoordData] | None = None,
    inicio: CoordData | None = None,
) -> list[CoordData]:
    if inicio is None:
        inicio = linhaDesordenada[0]
    if anteriores is None:
        anteriores = [inicio]
    linhaOrdenada = anteriores.copy()
    pontoInicial = anteriores[-1]
    anteriores = None
    while True:
        pontos: list[CoordData] = []
        for d in Direction:
            pontoAtual = apply_direction(pontoInicial, d)
            if pontoAtual in linhaDesordenada:
                if pontoAtual not in linhaOrdenada:
                    pontos.append(pontoAtual)
        if len(pontos) == 0:
            return linhaOrdenada
        elif len(pontos) == 1:
            pontoInicial = pontos[0]
            linhaOrdenada.append(pontoInicial)
        else:
            linhaMaxima = linhaOrdenada.copy()
            for ponto in pontos:
                novaLinha = ordenaLinhaIt(
                    linhaDesordenada, anteriores=linhaOrdenada + [ponto]
                )
                if len(novaLinha) == len(linhaDesordenada):
                    return novaLinha
                if len(novaLinha) > len(linhaMaxima):
                    linhaMaxima = novaLinha.copy()
            return linhaMaxima


def distancia(pontoA: CoordData, pontoB: CoordData) -> float:
    soma = 0
    for coord_a, coord_b in zip(pontoA, pontoB):
        soma += abs(coord_a - coord_b) ** 2
    return soma ** (1 / 2)


"""

SECÇÃO ESCRITA:

ferramentas para auxiliar a escrita de linhas e blob

"""


def escreveLinhas(
    linhaInicial: list[CoordData], linhaFinal: list[CoordData], file: TextIOWrapper
) -> None:
    pontosLinhaInicial = len(linhaInicial)
    pontosLinhaFinal = len(linhaFinal)
    if pontosLinhaInicial == pontosLinhaFinal:
        for n in range(pontosLinhaInicial):
            file.write(f"{linhaInicial[n][0]},{linhaInicial[n][1]}")
            file.write(f" {linhaFinal[n][0]},{linhaFinal[n][1]}\n")
    elif pontosLinhaInicial > pontosLinhaFinal:
        if pontosLinhaInicial - 1 == 0:
            multiplicador = 0.0
        else:
            multiplicador = (pontosLinhaFinal - 1) / (pontosLinhaInicial - 1)
        for n in range(pontosLinhaInicial):
            pontoFinal = int(n * multiplicador)
            file.write(f"{linhaInicial[n][0]},{linhaInicial[n][1]}")
            file.write(
                f" {linhaFinal[pontoFinal][0]},{linhaFinal[pontoFinal][1]}\n"
            )
    else:
        if pontosLinhaFinal - 1 == 0:
            multiplicador = 0.0
        else:
            multiplicador = (pontosLinhaInicial - 1) / (pontosLinhaFinal - 1)
        for n in range(pontosLinhaFinal):
            pontoInicial = int(n * multiplicador)
            file.write(
                f"{linhaInicial[pontoInicial][0]},{linhaInicial[pontoInicial][1]}"
            )
            file.write(f" {linhaFinal[n][0]},{linhaFinal[n][1]}\n")



def escreveBlobs(
    blobInicial: list[list[CoordData]],
    blobFinal: list[list[CoordData]],
    file: TextIOWrapper,
) -> None:
    pontosBlobInicial = len(blobInicial)
    pontosBlobFinal = len(blobFinal)
    if pontosBlobInicial == pontosBlobFinal:
        for n in range(pontosBlobInicial):
            escreveLinhas(blobInicial[n], blobFinal[n], file)
    elif pontosBlobInicial > pontosBlobFinal:
        if pontosBlobInicial - 1 == 0:
            multiplicador = 0.0
        else:
            multiplicador = (pontosBlobFinal - 1) / (pontosBlobInicial - 1)
        for n in range(pontosBlobInicial):
            camadaFinal = int(n * multiplicador)
            escreveLinhas(blobInicial[n], blobFinal[camadaFinal], file)
    else:
        if pontosBlobFinal - 1 == 0:
            multiplicador = 0.0
        else:
            multiplicador = (pontosBlobInicial - 1) / (pontosBlobFinal - 1)
        for n in range(pontosBlobFinal):
            camadaInicial = int(n * multiplicador)
            escreveLinhas(blobInicial[camadaInicial], blobFinal[n], file)


"""

SECÇÃO Fundo:

"""


def fazFundo(
    fileConfig: TextIOWrapper, parteInicial: Image.Image, parteFinal: Image.Image
) -> None:  # REMAKE
    pass


"""

SECÇÃO DEBUG:

"""


def imprimeBlob(blob: list[list[CoordData]], imagem: Image.Image) -> None:
    for camada in blob:
        linhas = [camada]  # divideLinha(camada)
        for linha in linhas:
            cor = tuple([randint(0, 255) for _ in range(3)])
            for coord in linha:
                imagem.putpixel(coord, cor)
    path = "./partesConfig"
    imagem.save(f"{path}/debugBlob{len(os.listdir(path)):03d}.png")


"""

SECÇÃO MAIN:

"""


def configPart(data: tuple[int, Image.Image, Image.Image]) -> None:
    n, imagemInicial, imagemFinal = data
    print(f"Fazendo Parte : {n}")
    parteInicial = Image.fromarray(imagemInicial)
    parteFinal = Image.fromarray(imagemFinal)
    with open(
        f"partesConfig/parte{n:02d}Config.txt", "w", encoding="utf-8"
    ) as fileConfig:
        if n == 1:
            fazFundo(fileConfig, parteInicial, parteFinal)
        else:
            hasRGB = hasColor(parteInicial)
            linhaAzulInicial: list[CoordData] = []
            linhaAzulFinal: list[CoordData] = []
            if hasRGB[1]:
                linhaAzulInicial = procuraLinhaAzul(parteInicial, inicio=hasRGB[1])
                linhaAzulFinal = procuraLinhaAzul(parteFinal)
            if hasRGB[0]:
                if hasRGB[1]:
                    blobInicial = [linhaAzulInicial]
                    blobFinal = [linhaAzulFinal]
                else:
                    blobInicial = [procuraContornoVerde(parteInicial)]
                    blobFinal = [procuraContornoVerde(parteFinal)]
                procuraBlob(parteInicial, blobInicial)
                procuraBlob(parteFinal, blobFinal)
                escreveBlobs(blobInicial, blobFinal, fileConfig)
            else:
                escreveLinhas(linhaAzulInicial, linhaAzulFinal, fileConfig)
        print(f"\tParte Terminada : {n}")
    parteInicial.close()
    parteFinal.close()


def main() -> None:
    limpaPasta("./partesConfig")
    limpaPasta("./frames")
    limpaPasta("./frames/resized")
    imagemInicial = pypdn.read("inicial.pdn")
    imagemFinal = pypdn.read("final.pdn")
    Image.fromarray(imagemInicial.layers[0].image).save("inicial.png")
    Image.fromarray(imagemFinal.layers[0].image).save("final.png")
    quantiaPartes = len(imagemInicial.layers)
    with multiprocessing.Pool(os.cpu_count()) as cpu_pool:
        cpu_pool.map(
            configPart,
            [
                (
                    a,
                    Image.fromarray(imagemInicial.layers[a].image),
                    Image.fromarray(imagemFinal.layers[a].image),
                )
                for a in range(1, quantiaPartes)
            ],
        )


if __name__ == "__main__":
    main()
