from io import TextIOWrapper
from typing import Literal
from PIL import Image
import os
import multiprocessing
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


def hasColor(imagem: Image.Image) -> tuple[bool, bool, Literal[False] | CoordData]:
    largura, altura = imagem.size
    hasGreen = False
    hasRed = False
    hasBlue: Literal[False] | CoordData = False
    for x in range(largura):
        for y in range(altura):
            pixel = get_pixel(imagem, (x, y))
            if pixel[3] == 0:
                continue
            if pixel[1] != 0:
                hasGreen = True
                if hasBlue or hasRed:
                    return (hasRed, hasGreen, hasBlue)
                else:
                    continue
            if pixel[2] != 0:
                if pixel[2] == 200:
                    hasBlue = (x, y)
                    if hasGreen:
                        return (hasRed, hasGreen, hasBlue)
                continue
            if pixel[0] != 0:
                hasRed = True
                if hasGreen:
                    return (hasRed, hasGreen, hasBlue)
    return (hasRed, hasGreen, hasBlue)


def limpaPasta(pasta: str) -> None:
    arquivos = [f"{pasta}/{a}" for a in os.listdir(pasta)]
    if "./frames/resized" in arquivos:
        arquivos.pop(arquivos.index("./frames/resized"))
    for arquivo in arquivos:
        os.remove(arquivo)


"""

SECÇÃO VERMELHA:

pontos únicos

"""


def procuraCor(imagem: Image.Image, indexColor: int) -> list[list[CoordData]]:
    largura, altura = imagem.size
    listaDeCores: list[int] = []
    coordenadasDasCores: list[list[CoordData]] = []
    for x in range(largura):
        for y in range(altura):
            pixel = get_pixel(imagem, (x, y))
            if pixel[3] == 0:
                continue
            cor = pixel[indexColor]
            if cor != 0:
                if cor not in listaDeCores:
                    listaDeCores.append(cor)
                    coordenadasDasCores.append([(x, y)])
                else:
                    corIndex = listaDeCores.index(cor)
                    coordenadasDasCores[corIndex].append((x, y))
    return coordenadasDasCores


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


DOWN_DIRECTIONS = [Direction.DOWN_RIGHT, Direction.DOWN, Direction.DOWN_LEFT]


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

linhas que se iniciam no tom 255 e continuam no tom 254

"""


def procuraUmAzul(imagem: Image.Image, tom: int) -> CoordData:
    largura, altura = imagem.size
    for x in range(largura):
        for y in range(altura):
            pixel = get_pixel(imagem, (x, y))
            if pixel[3] == 0:
                continue
            if pixel[2] == tom:
                return (x, y)
    return (-1, -1)


def procuraLinhaAzul(
    imagem: Image.Image,
    anteriores: list[CoordData] | None = None,
    inicio: CoordData | None = None,
) -> list[CoordData]:
    if anteriores is None:
        if inicio is None:
            anteriores = [procuraUmAzul(imagem, 200)]
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


def procuraContornoVerde(imagem: Image.Image) -> list[CoordData]:  # obsolete
    contorno: list[CoordData] = []
    largura, altura = imagem.size
    elementoAtual = False
    for y in range(altura):
        ultimoElemento = False
        for x in range(largura):
            elementoAtual = get_pixel(imagem, (x, y))[1] == 255
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
            elementoAtual = get_pixel(imagem, (x, y))[1] == 255
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
    return contorno


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
        for direcao in DOWN_DIRECTIONS:
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


def divideLinha(linha: list[CoordData]) -> list[list[CoordData]]:
    linhas: list[list[CoordData]] = []
    for ponto in linha:
        pontoAppend = False
        for linha in linhas:
            for novoPonto in linha:
                if distancia(ponto, novoPonto) <= 2 ** (1 / 2) + 0.01:
                    pontoAppend = True
                    break
            if pontoAppend:
                linha.append(ponto)
                break
        if not pontoAppend:
            linhas.append([ponto])
    return linhas


def ordenaLinha(linhaOriginal: list[CoordData]) -> list[CoordData]:
    linhaTotal: list[CoordData] = []
    linhas = divideLinha(linhaOriginal)
    for linha in linhas:
        linhaTotal += ordenaLinhaInd(linha)
    return linhaTotal


def ordenaLinhaInd(linha: list[CoordData]) -> list[CoordData]:
    tamanho = len(linha)
    for tamanhoPossivel in range(tamanho, -1, -1):
        for n in range(tamanho):
            linhaTeste = linha.copy()
            primeiroPonto = linha[n]
            linhaTeste = ordenaLinhaIt(linhaTeste, inicio=primeiroPonto)
            if len(linhaTeste) == tamanhoPossivel:
                return linhaTeste
    error_message = f"não foi possível ordenar a linha, analise: {linha}"
    raise ValueError(error_message)


def ordenaLinhaIt(
    linhaDesordenada: list[CoordData],
    anteriores: list[CoordData] | None = None,
    inicio: CoordData | None = None,
) -> list[CoordData]:
    if inicio is None:
        if anteriores is None:
            inicio = linhaDesordenada[0]
        else:
            inicio = anteriores[0]
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
        if len(pontos) == 1:
            pontoInicial = pontos[0]
            linhaOrdenada.append(pontoInicial)
        else:
            linhaMaxima = linhaOrdenada.copy()
            for ponto in pontos:
                novaLinha = ordenaLinhaIt(
                    linhaDesordenada, anteriores=linhaOrdenada + [ponto]
                )
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
    """largura,altura = parteInicial.size
    for y in range(altura):
        for x in range(largura):
            pixel = get_pixel(parteInicial,(x,y))
            if pixel[3] != 0:
                if get_pixel(parteFinal,(x,y))[3]!=0:
                    fileConfig.write(f"{x},{y} {x},{y}\n")
                else:
                    fileConfig.write(f"{x},{y} fundo\n")
    parteInicial.close()
    parteFinal.close()"""


"""

SECÇÃO DEBUG:

"""


def imprimeBlob(blobs: list[list[CoordData]]) -> None:
    for n, blob in enumerate(blobs):
        print(f"\nblob {n} : \n")
        for m, camada in enumerate(blob):
            print(f"camada {m} : \n")
            for coord in camada:
                print(coord)


"""

SECÇÃO MAIN:

"""


def configPart(data: tuple[int, Image.Image, Image.Image]) -> None:
    n, parteInicial, parteFinal = data
    print(n)
    with open(
        f"partesConfig/parte{n:02d}Config.txt", "w", encoding="utf-8"
    ) as fileConfig:
        if n == 1:
            fazFundo(fileConfig, parteInicial, parteFinal)
        else:
            hasRGB = hasColor(parteInicial)
            print(hasRGB)
            coordVermelhosInicial: list[list[CoordData]] = []
            coordVermelhosFinal: list[list[CoordData]] = []
            linhaAzulInicial: list[CoordData] = []
            linhaAzulFinal: list[CoordData] = []
            if hasRGB[0]:
                coordVermelhosInicial = procuraCor(parteInicial, 0)
                coordVermelhosFinal = procuraCor(parteFinal, 0)
            if hasRGB[2]:
                linhaAzulInicial = procuraLinhaAzul(parteInicial, inicio=hasRGB[2])
                linhaAzulFinal = procuraLinhaAzul(parteFinal)
                if not hasRGB[2]:
                    escreveLinhas(linhaAzulInicial, linhaAzulFinal, fileConfig)
            if hasRGB[1]:
                if hasRGB[2]:
                    blobsInicial = [linhaAzulInicial]
                    blobsFinal = [linhaAzulFinal]
                elif hasRGB[0]:
                    blobsInicial = [[a[0] for a in coordVermelhosInicial]]
                    blobsFinal = [[a[0] for a in coordVermelhosFinal]]
                else:
                    blobsInicial = [procuraContornoVerde(parteInicial)]
                    blobsFinal = [procuraContornoVerde(parteFinal)]
                procuraBlob(parteInicial, blobsInicial)
                procuraBlob(parteFinal, blobsFinal)
                escreveBlobs(blobsInicial, blobsFinal, fileConfig)
            if hasRGB[0]:
                pass  # TODO: discover why this was here, maybe the for below was supposed to be here?
            for coordInicial, coordFinal in zip(
                coordVermelhosInicial, coordVermelhosFinal
            ):
                for coord_i, coord_f in zip(coordInicial, coordFinal):
                    fileConfig.write(f"{coord_i[0]},{coord_i[1]}")
                    fileConfig.write(f" {coord_f[0]},{coord_f[1]}\n")
            print()
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
