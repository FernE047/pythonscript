from io import TextIOWrapper
from typing import Iterable, Literal
from PIL import Image
import os
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


def hasColor(
    imagem: Image.Image,
) -> tuple[bool, bool, Literal[False] | CoordData, Literal[False] | CoordData]:
    largura, altura = imagem.size
    hasGreen = False
    hasRed = False
    hasBlue: Literal[False] | CoordData = False
    hasBlueIterative: Literal[False] | CoordData = False
    for x in range(largura):
        for y in range(altura):
            pixel = get_pixel(imagem, (x, y))
            if pixel[3] == 0:
                continue
            if pixel[1] != 0:
                if pixel[2] == 255:
                    continue
                hasGreen = True
                if hasBlueIterative or hasBlue or hasRed:
                    return (hasRed, hasGreen, hasBlue, hasBlueIterative)
                else:
                    continue
            if pixel[2] != 0:
                if pixel[2] == 200:
                    hasBlueIterative = (x, y)
                    if hasGreen:
                        return (hasRed, hasGreen, hasBlue, hasBlueIterative)
                else:
                    hasBlue = (x, y)
                    if hasGreen:
                        return (hasRed, hasGreen, hasBlue, hasBlueIterative)
                continue
            if pixel[0] != 0:
                hasRed = True
                if hasGreen:
                    return (hasRed, hasGreen, hasBlue, hasBlueIterative)
    return (hasRed, hasGreen, hasBlue, hasBlueIterative)


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

linhas que sejam direcionadas de acordo com direções de 1 a 8 com:

7 6 5
4 X 3
2 1 0

"""


def procuraLinhaAzul(
    imagem: Image.Image, primeiro: CoordData | None = None
) -> list[CoordData]:
    if primeiro is None:
        primeiro = procuraUmAzul(imagem, range(248, 256))
    linha = [primeiro]
    pontoAtual = primeiro
    while True:
        pontoAtual = apply_direction(
            pontoAtual, Direction(get_pixel(imagem, pontoAtual)[2])
        )
        try:
            pixel = get_pixel(imagem, pontoAtual)
        except Exception:
            break
        if (pixel[2] == 0) or (pixel[3] == 0):
            break
        else:
            linha.append(pontoAtual)
    inicioDaLinha = True
    while True:
        for direcao in Direction:
            try:
                coord = apply_direction(primeiro, direcao)
                pixelAoRedor = get_pixel(imagem, coord)
            except Exception:
                continue
            if pixelAoRedor[3] != 0:
                if pixelAoRedor not in linha:
                    if pixelAoRedor[2] != 0:
                        if pixelAoRedor[2] % 8 == 7 - direcao.value:
                            primeiro = coord
                            linha = [primeiro] + linha
                            inicioDaLinha = False
                            break
        if inicioDaLinha:
            return linha
        else:
            inicioDaLinha = True


def procuraUmAzul(imagem: Image.Image, tons: list[int] | Iterable[int]) -> CoordData:
    largura, altura = imagem.size
    for x in range(largura):
        for y in range(altura):
            pixel = get_pixel(imagem, (x, y))
            if pixel[3] == 0:
                continue
            if pixel[2] in tons:
                return (x, y)
    return (-1, -1)


def procuraLinhaAzulIterativo(
    imagem: Image.Image,
    anteriores: list[CoordData] | None = None,
    inicio: CoordData | None = None,
) -> list[CoordData]:
    if anteriores is None:
        if inicio is None:
            anteriores = [procuraUmAzul(imagem, [200])]
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


def procuraContornoVerde(imagem: Image.Image) -> list[CoordData]:
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


def procuraBlob(
    imagem: Image.Image,
    linhaAtual: list[CoordData],
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
                if pixel[1] == 255:
                    if coordenada not in linhaAtual:
                        if coordenada not in linhaAnterior:
                            if coordenada not in proximaLinha:
                                proximaLinha.append(coordenada)
    if len(proximaLinha) > 0:
        blob.append(proximaLinha)
        procuraBlob(imagem, proximaLinha, blob, linhaAnterior=linhaAtual)


"""

SECÇÃO ESCRITA:

ferramentas para auxiliar a escrita de linhas e blob

"""


def escreveLinhas(
    imagemInicialPNG: Image.Image,
    imagemFinalPNG: Image.Image,
    linhaInicial: list[CoordData],
    linhaFinal: list[CoordData],
    file: TextIOWrapper,
    total: int,
):
    pontosLinhaInicial = len(linhaInicial)
    pontosLinhaFinal = len(linhaFinal)
    if pontosLinhaInicial == pontosLinhaFinal:
        for n in range(pontosLinhaInicial):
            linha: list[str] = []
            for m in range(2):
                b = linhaInicial[n][m]
                a = linhaFinal[n][m] - b
                linha.append(f"{a},{b}")
            pixelInicial = get_pixel(imagemInicialPNG, linhaInicial[n])
            pixelFinal = get_pixel(imagemFinalPNG, linhaFinal[n])
            for m in range(3):
                b = pixelInicial[m]
                a = pixelFinal[m] - b
                linha.append(f"{a},{b}")
            file.write(f"{' '.join(linha)}\n")
    elif pontosLinhaInicial > pontosLinhaFinal:
        if pontosLinhaInicial - 1 == 0:
            multiplicador = 0.0
        else:
            multiplicador = (pontosLinhaFinal - 1) / (pontosLinhaInicial - 1)
        for n in range(pontosLinhaInicial):
            linha = []  # linha de texto
            pontoFinal = int(n * multiplicador)
            for m in range(2):
                b = linhaInicial[n][m]
                a = linhaFinal[pontoFinal][m] - b
                linha.append(f"{a},{b}")
            pixelInicial = get_pixel(imagemInicialPNG, linhaInicial[n])
            pixelFinal = get_pixel(imagemFinalPNG, linhaFinal[pontoFinal])
            for m in range(3):
                b = pixelInicial[m]
                a = pixelFinal[m] - b
                linha.append(f"{a},{b}")
            file.write(f"{' '.join(linha)}\n")
    else:
        if pontosLinhaFinal - 1 == 0:
            multiplicador = 0.0
        else:
            multiplicador = (pontosLinhaInicial - 1) / (pontosLinhaFinal - 1)
        for n in range(pontosLinhaFinal):
            linha = []  # linha de texto
            pontoInicial = int(n * multiplicador)
            for m in range(2):
                b = linhaInicial[pontoInicial][m]
                a = linhaFinal[n][m] - b
                linha.append(f"{a},{b}")
            pixelInicial = get_pixel(imagemInicialPNG, linhaInicial[pontoInicial])
            pixelFinal = get_pixel(imagemFinalPNG, linhaFinal[n])
            for m in range(3):
                b = pixelInicial[m]
                a = pixelFinal[m] - b
                linha.append(f"{a},{b}")
            file.write(f"{' '.join(linha)}\n")


def escreveBlobs(
    imagemInicialPNG: Image.Image,
    imagemFinalPNG: Image.Image,
    blobInicial: list[list[CoordData]],
    blobFinal: list[list[CoordData]],
    file: TextIOWrapper,
    quantiaFrames: int,
):
    pontosBlobInicial = len(blobInicial)
    pontosBlobFinal = len(blobFinal)
    if pontosBlobInicial == pontosBlobFinal:
        for n in range(pontosBlobInicial):
            escreveLinhas(
                imagemInicialPNG,
                imagemFinalPNG,
                blobInicial[n],
                blobFinal[n],
                file,
                quantiaFrames,
            )
    elif pontosBlobInicial > pontosBlobFinal:
        if pontosBlobInicial - 1 == 0:
            multiplicador = 0.0
        else:
            multiplicador = (pontosBlobFinal - 1) / (pontosBlobInicial - 1)
        for n in range(pontosBlobInicial):
            camadaFinal = int(n * multiplicador)
            escreveLinhas(
                imagemInicialPNG,
                imagemFinalPNG,
                blobInicial[n],
                blobFinal[camadaFinal],
                file,
                quantiaFrames,
            )
    else:
        if pontosBlobFinal - 1 == 0:
            multiplicador = 0.0
        else:
            multiplicador = (pontosBlobInicial - 1) / (pontosBlobFinal - 1)
        for n in range(pontosBlobFinal):
            camadaInicial = int(n * multiplicador)
            escreveLinhas(
                imagemInicialPNG,
                imagemFinalPNG,
                blobInicial[camadaInicial],
                blobFinal[n],
                file,
                quantiaFrames,
            )


"""

SECÇÃO Fundo:

"""


def fazFundo(
    fileConfig: TextIOWrapper, parteInicial: Image.Image, parteFinal: Image.Image
) -> None:
    largura, altura = parteInicial.size
    for y in range(altura):
        for x in range(largura):
            pixel = get_pixel(parteInicial, (x, y))
            if pixel[3] != 0:
                if get_pixel(parteFinal, (x, y))[3] != 0:
                    fileConfig.write(f"{x},{y} {x},{y}\n")
                else:
                    fileConfig.write(f"{x},{y} fundo\n")
    parteInicial.close()
    parteFinal.close()


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


def fazConfig(quantiaFrames: int) -> tuple[Image.Image, Image.Image]:
    nomeConfig = "partesConfig/parte{0:02d}Config.txt"
    imagemInicialPDN = pypdn.read("inicial.pdn")
    imagemFinalPDN = pypdn.read("final.pdn")
    imagemInicialPNG = Image.fromarray(imagemInicialPDN.layers[0].image)
    imagemFinalPNG = Image.fromarray(imagemFinalPDN.layers[0].image)
    quantiaPartes = len(imagemInicialPDN.layers)
    with open("config.txt", "w", encoding="utf-8") as file:
        for nParte in range(1, quantiaPartes):
            print(nParte)
            parteInicial = Image.fromarray(imagemInicialPDN.layers[nParte].image)
            parteFinal = Image.fromarray(imagemFinalPDN.layers[nParte].image)
            if nParte == 1:
                if get_pixel(parteInicial, (0, 0)) == (255, 255, 255, 255):
                    fazFundo(file, parteInicial, parteFinal)
                    continue
            with open(nomeConfig.format(nParte), "w", encoding="utf-8") as fileConfig:
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
                    linhaAzulInicial = procuraLinhaAzul(
                        parteInicial, primeiro=hasRGB[2]
                    )
                    linhaAzulFinal = procuraLinhaAzul(parteFinal)
                    escreveLinhas(
                        imagemInicialPNG,
                        imagemFinalPNG,
                        linhaAzulInicial,
                        linhaAzulFinal,
                        fileConfig,
                        quantiaFrames,
                    )
                if hasRGB[3]:
                    linhaAzulInicial = procuraLinhaAzulIterativo(
                        parteInicial, inicio=hasRGB[3]
                    )
                    linhaAzulFinal = procuraLinhaAzulIterativo(parteFinal)
                    escreveLinhas(
                        imagemInicialPNG,
                        imagemFinalPNG,
                        linhaAzulInicial,
                        linhaAzulFinal,
                        fileConfig,
                        quantiaFrames,
                    )
                if hasRGB[1]:
                    if (hasRGB[2]) or (hasRGB[3]):
                        blobsInicial: list[list[CoordData]] = [linhaAzulInicial]
                        procuraBlob(parteInicial, linhaAzulInicial, blobsInicial)
                        blobsFinal: list[list[CoordData]] = [linhaAzulFinal]
                        procuraBlob(parteFinal, linhaAzulFinal, blobsFinal)
                    elif hasRGB[0]:
                        blobsInicial = [[a[0] for a in coordVermelhosInicial]]
                        procuraBlob(parteInicial, blobsInicial[0], blobsInicial)
                        blobsFinal = [[a[0] for a in coordVermelhosFinal]]
                        procuraBlob(parteFinal, blobsFinal[0], blobsFinal)
                    else:
                        blobsInicial = []
                        procuraBlob(parteInicial, [], blobsInicial)
                        blobsFinal = []
                        procuraBlob(parteFinal, [], blobsFinal)
                    escreveBlobs(
                        imagemInicialPNG,
                        imagemFinalPNG,
                        blobsInicial,
                        blobsFinal,
                        fileConfig,
                        quantiaFrames,
                    )
                if hasRGB[0]:
                    for coordInicial, coordFinal in zip(
                        coordVermelhosInicial, coordVermelhosFinal
                    ):
                        for coord_i, coord_f in zip(coordInicial, coordFinal):
                            fileConfig.write(f"{coord_i[0]},{coord_i[1]}")
                            fileConfig.write(f" {coord_f[0]},{coord_f[1]}\n")
                print()
            parteInicial.close()
            parteFinal.close()
        for nParte in range(1, quantiaPartes):
            with open(nomeConfig.format(nParte), "r", encoding="utf-8") as fileConfig:
                linha = fileConfig.readline()
                while linha:
                    file.write(linha)
                    linha = fileConfig.readline()
    return (imagemInicialPNG, imagemFinalPNG)


def main() -> None:
    quantiaFrames = 30  # pegaInteiro("quantos frames?")
    limpaPasta("./partesConfig")
    limpaPasta("./frames")
    limpaPasta("./frames/resized")
    nomeFrame = "frames/frame{0:03d}.png"
    imagemInicial, imagemFinal = fazConfig(quantiaFrames)
    imagemInicial.save(nomeFrame.format(0))
    imagemFinal.save(nomeFrame.format(quantiaFrames + 1))
    print(f"\n tamanho: {imagemInicial.size}\n")
    for n in range(quantiaFrames):
        print(n)
        frame = Image.new("RGBA", imagemFinal.size, (255, 255, 255, 0))
        with open("config.txt", "r", encoding="utf-8") as file:
            linha = file.readline()
            while linha:
                if linha.find("fundo") != -1:
                    coord = (
                        int(linha[:-6].split(",")[0]),
                        int(linha[:-6].split(",")[1]),
                    )
                    frame.putpixel(coord, get_pixel(imagemInicial, coord))
                else:
                    dados = (
                        (
                            int(linha.split(" ")[0].split(",")[0]),
                            int(linha.split(" ")[0].split(",")[1]),
                        ),
                        (
                            int(linha.split(" ")[1].split(",")[0]),
                            int(linha.split(" ")[1].split(",")[1]),
                        ),
                    )
                    novaCoord: list[int] = []
                    for m in range(2):
                        a = dados[m][0]
                        b = dados[m][1]
                        novaCoord.append(int((n + 1) * a / (quantiaFrames + 1) + b))
                    novaCoord_tuple = tuple(novaCoord)
                    novaCor: list[int] = []
                    for m in range(3):
                        a = dados[m + 2][0]
                        b = dados[m + 2][1]
                        novaCor.append(int((n + 1) * a / (quantiaFrames + 1) + b))
                    novaCor.append(255)
                    novaCor_tuple = tuple(novaCor)
                    assert len(novaCoord_tuple) == 2  # Gambiarra :v
                    frame.putpixel(novaCoord_tuple, novaCor_tuple)
                linha = file.readline()
            frame.save(nomeFrame.format(n + 1))
            frame.close()
    imagemInicial.close()
    imagemFinal.close()


if __name__ == "__main__":
    main()
