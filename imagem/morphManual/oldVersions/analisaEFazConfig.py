from io import TextIOWrapper
from PIL import Image
import os
from enum import Enum

CoordData = tuple[int, int]

# this code is legacy, I am only changing type hints and linter errors. it doesn't make sense to refactor it, since I already have a better version of it, and I don't want to break it by changing it too much


def open_image_as_rgba(image_path: str) -> Image.Image:
    with Image.open(image_path) as image:
        image_in_memory = image.copy()
        if image.mode != "RGBA":
            return image_in_memory.convert("RGBA")
        return image_in_memory


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


def hasColor(imagem: Image.Image) -> tuple[bool, bool, bool, bool]:
    largura, altura = imagem.size
    hasGreen = False
    hasRed = False
    hasBlue = False
    hasBlueIterative = False
    for x in range(largura):
        for y in range(altura):
            pixel = get_pixel(imagem, (x, y))
            if pixel[3] == 0:
                continue
            if pixel[0] != 0:
                hasRed = True
                continue
            if pixel[1] != 0:
                hasGreen = True
                continue
            if pixel[2] != 0:
                hasBlue = True
            if pixel[2] == 200:
                hasBlueIterative = True
    return (hasRed, hasGreen, hasBlue, hasBlueIterative)


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

linhas que sejam direcionadas de acordo com direções de 1 a 8 com:

7 6 5
4 X 3
2 1 0

"""


def procuraInicioDaLinhaAzul(imagem: Image.Image) -> CoordData:
    largura, altura = imagem.size
    for x in range(largura):
        inicioDaLinha = False
        for y in range(altura):
            pixel = get_pixel(imagem, (x, y))
            if pixel[3] == 0:
                continue
            if pixel[2] != 0:
                inicioDaLinha = True
                for direcao in Direction:
                    try:
                        pixelAoRedor = get_pixel(
                            imagem, apply_direction((x, y), direcao)
                        )
                    except Exception:
                        continue
                    if pixelAoRedor[2] != 0:
                        if pixelAoRedor[2] % 8 == 7 - direcao.value:
                            inicioDaLinha = False
                if inicioDaLinha:
                    return (x, y)
    return (-1, -1)


def procuraLinhaAzul(imagem: Image.Image) -> list[CoordData]:
    inicioDaLinha = procuraInicioDaLinhaAzul(imagem)
    pontoAtual = inicioDaLinha
    linha = [pontoAtual]
    while True:
        pontoAtual = apply_direction(
            pontoAtual, Direction(get_pixel(imagem, pontoAtual)[2])
        )
        try:
            pixel = get_pixel(imagem, pontoAtual)
        except Exception:
            return linha
        if pixel[2] == 0:
            return linha
        else:
            linha.append(pontoAtual)


def procuraInicioDaLinhaAzulIterativa(imagem: Image.Image) -> CoordData:
    largura, altura = imagem.size
    for x in range(largura):
        for y in range(altura):
            pixel = get_pixel(imagem, (x, y))
            if pixel[3] == 0:
                continue
            if pixel[2] == 200:
                return (x, y)
    return (-1, -1)


def procuraLinhaAzulIterativo(
    imagem: Image.Image, anteriores: list[CoordData] | None = None
) -> list[CoordData]:
    if anteriores is None:
        anteriores = [procuraInicioDaLinhaAzulIterativa(imagem)]
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
                    if pixel[:3] == (0, 255, 255):
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
                novaLinha = procuraLinhaAzulIterativo(
                    imagem, anteriores=linha + [ponto]
                )
                if len(novaLinha) > len(linhaMaxima):
                    linhaMaxima = novaLinha.copy()
            return linhaMaxima


"""

SECÇÃO VERDE:

Regiões que sejam 2D, chamadas de blob
cada Blob possui camadas que são conjuntos de coordenadas

"""


def procuraContornoVerde(imagem: Image.Image, tom: int) -> list[CoordData]:
    contorno: list[CoordData] = []
    largura, altura = imagem.size
    elementoAtual = False
    for y in range(altura):
        ultimoElemento = False
        for x in range(largura):
            elementoAtual = get_pixel(imagem, (x, y))[1] == tom
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
            elementoAtual = get_pixel(imagem, (x, y))[1] == tom
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


def procuraBlob(
    linhaAtual: list[CoordData],
    imagem: Image.Image,
    tom: int,
    blob: list[list[CoordData]],
    linhaAnterior: list[CoordData] | None = None,
) -> None:
    if linhaAnterior is None:
        linhaAnterior = []
    proximaLinha: list[CoordData] = []
    for coord in linhaAtual:
        for direcao in Direction:
            coordenada = apply_direction(coord, direcao)
            try:
                pixel = get_pixel(imagem, coordenada)
            except Exception:
                continue
            if pixel[3] != 0:
                if pixel[1] == tom:
                    if coordenada not in linhaAtual:
                        if coordenada not in linhaAnterior:
                            if coordenada not in proximaLinha:
                                proximaLinha.append(coordenada)
    if len(proximaLinha) > 0:
        blob.append(proximaLinha)
        procuraBlob(proximaLinha, imagem, tom, blob, linhaAnterior=linhaAtual)


def procuraBlobs(
    imagem: Image.Image, linhaAtual: list[CoordData] | None = None
) -> list[list[list[CoordData]]]:
    blobs: list[list[list[CoordData]]] = []
    largura, altura = imagem.size
    tons: list[int] = []
    for y in range(altura):
        for x in range(largura):
            coordenada = (x, y)
            pixel = get_pixel(imagem, coordenada)
            if pixel[3] != 0:
                if pixel[1] != 0:
                    if pixel[1] not in tons:
                        tons.append(pixel[1])
    tons.sort()
    for tom in tons:
        if (tom == 255) and (linhaAtual is not None):
            blob = []
        else:
            linhaAtual = procuraContornoVerde(imagem, tom)
            blob = [linhaAtual]
        procuraBlob(linhaAtual, imagem, tom, blob)
        if len(blob) > 0:
            blobs.append(blob)
    return blobs


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
            file.write(str(linhaInicial[n][0]) + "," + str(linhaInicial[n][1]))
            file.write(" " + str(linhaFinal[n][0]) + "," + str(linhaFinal[n][1]) + "\n")
    elif pontosLinhaInicial > pontosLinhaFinal:
        if pontosLinhaInicial - 1 == 0:
            multiplicador = 0.0
        else:
            multiplicador = (pontosLinhaFinal - 1) / (pontosLinhaInicial - 1)
        for n in range(pontosLinhaInicial):
            pontoFinal = int(n * multiplicador)
            file.write(str(linhaInicial[n][0]) + "," + str(linhaInicial[n][1]))
            file.write(
                " "
                + str(linhaFinal[pontoFinal][0])
                + ","
                + str(linhaFinal[pontoFinal][1])
                + "\n"
            )
    else:
        if pontosLinhaFinal - 1 == 0:
            multiplicador = 0.0
        else:
            multiplicador = (pontosLinhaInicial - 1) / (pontosLinhaFinal - 1)
        for n in range(pontosLinhaFinal):
            pontoInicial = int(n * multiplicador)
            file.write(
                str(linhaInicial[pontoInicial][0])
                + ","
                + str(linhaInicial[pontoInicial][1])
            )
            file.write(" " + str(linhaFinal[n][0]) + "," + str(linhaFinal[n][1]) + "\n")


def escreveBlobs(
    blobsInicial: list[list[list[CoordData]]],
    blobsFinal: list[list[list[CoordData]]],
    file: TextIOWrapper,
) -> None:
    for blobInicial, blobFinal in zip(blobsInicial, blobsFinal):
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


def fazFundo(fileConfig: TextIOWrapper) -> None:
    parteInicial = open_image_as_rgba("partesIniciais/fundo.png")
    parteFinal = open_image_as_rgba("partesFinais/fundo.png")
    largura, altura = parteInicial.size
    for y in range(altura):
        for x in range(largura):
            pixel = get_pixel(parteInicial, (x, y))
            if pixel[3] != 0:
                if get_pixel(parteFinal, (x, y))[3] != 0:
                    fileConfig.write(
                        str(x) + "," + str(y) + " " + str(x) + "," + str(y) + "\n"
                    )
                else:
                    fileConfig.write(str(x) + "," + str(y) + " fundo\n")


"""

SECÇÃO DEBUG:

"""


def imprimeBlob(blobs: list[list[list[CoordData]]]) -> None:
    for n, blob in enumerate(blobs):
        print("\nblob " + str(n) + " : \n")
        for m, camada in enumerate(blob):
            print("camada " + str(m) + " : \n")
            for coord in camada:
                print(coord)


"""

SECÇÃO MAIN:

"""


def main() -> None:
    nomeInicial = "partesIniciais/parte{0:02d}inicial.png"
    nomeConfig = "partesConfig/parte{0:02d}Config.txt"
    nomeFinal = "partesFinais/parte{0:02d}final.png"
    partes: list[str] = os.listdir("partesIniciais")
    quantiaPartes = len(partes)
    with open("config.txt", "w") as file:
        if "fundo.png" in partes:
            quantiaPartes -= 1
            fazFundo(file)
        for nParte in range(quantiaPartes):
            print(nParte)
            parteInicial = open_image_as_rgba(nomeInicial.format(nParte))
            parteFinal = open_image_as_rgba(nomeFinal.format(nParte))
            with open(nomeConfig.format(nParte), "w", encoding="utf-8") as fileConfig:
                hasRGB = hasColor(parteInicial)
                coordVermelhosInicial: list[list[CoordData]] = []
                coordVermelhosFinal: list[list[CoordData]] = []
                linhaAzulInicial: list[CoordData] = []
                linhaAzulFinal: list[CoordData] = []
                print(hasRGB)
                if hasRGB[0]:
                    coordVermelhosInicial = procuraCor(parteInicial, 0)
                    coordVermelhosFinal = procuraCor(parteFinal, 0)
                if hasRGB[2]:
                    if hasRGB[3]:
                        linhaAzulInicial = procuraLinhaAzulIterativo(parteInicial)
                        linhaAzulFinal = procuraLinhaAzulIterativo(parteFinal)
                    else:
                        linhaAzulInicial = procuraLinhaAzul(parteInicial)
                        linhaAzulFinal = procuraLinhaAzul(parteFinal)
                if hasRGB[1]:
                    if hasRGB[2]:
                        blobsInicial = procuraBlobs(
                            parteInicial, linhaAtual=linhaAzulInicial
                        )
                        blobsFinal = procuraBlobs(parteFinal, linhaAtual=linhaAzulFinal)
                    elif hasRGB[0]:
                        blobsInicial = procuraBlobs(
                            parteInicial,
                            linhaAtual=[a[0] for a in coordVermelhosInicial],
                        )
                        blobsFinal = procuraBlobs(
                            parteFinal, linhaAtual=[a[0] for a in coordVermelhosFinal]
                        )
                    else:
                        blobsInicial = procuraBlobs(parteInicial)
                        blobsFinal = procuraBlobs(parteFinal)
                    escreveBlobs(blobsInicial, blobsFinal, fileConfig)
                fileConfig.write("azul\n")
                if hasRGB[2]:
                    escreveLinhas(linhaAzulInicial, linhaAzulFinal, fileConfig)
                fileConfig.write("vermelho\n")
                if hasRGB[0]:
                    for coordInicial, coordFinal in zip(
                        coordVermelhosInicial, coordVermelhosFinal
                    ):
                        for coord_i, coord_f in zip(coordInicial, coordFinal):
                            fileConfig.write(str(coord_i[0]) + "," + str(coord_i[1]))
                            fileConfig.write(
                                " " + str(coord_f[0]) + "," + str(coord_f[1]) + "\n"
                            )
                print()
        for colorIndex in range(3):
            for nParte in range(quantiaPartes):
                with open(
                    nomeConfig.format(nParte), "r", encoding="utf-8"
                ) as fileConfig:
                    linha = fileConfig.readline()
                    if colorIndex == 1:
                        while linha != "azul\n":
                            linha = fileConfig.readline()
                        linha = fileConfig.readline()
                    if colorIndex == 2:
                        while linha != "vermelho\n":
                            linha = fileConfig.readline()
                        linha = fileConfig.readline()
                    while linha:
                        if linha[0] in ["a", "v"]:
                            break
                        file.write(linha)
                        linha = fileConfig.readline()


if __name__ == "__main__":
    main()
