from io import TextIOWrapper
from typing import Any, Literal
from PIL import Image
import os
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


class Linha:
    inicio: CoordData | None
    fim: CoordData | None

    def __init__(self, pontos: list[CoordData] | None = None):
        if pontos is None:
            self.pontos: list[CoordData] = []
            self.inicio = None
            self.fim = None
        else:
            self.pontos = pontos.copy()
            if self.pontos:
                self.inicio = self.pontos[0]
                self.fim = self.pontos[-1]
            else:
                self.inicio = None
                self.fim = None

    def procuraLinhaAzul(self, imagem: Image.Image) -> None:
        if self.inicio is None or self.fim is None:
            raise ValueError(
                "Linha must have at least one point to search for blue line"
            )
        while True:
            pontoInicial = self.fim
            pontos: list[CoordData] = []
            for d in Direction:
                pontoAtual = apply_direction(pontoInicial, d)
                if pontoAtual not in self:
                    try:
                        pixel = get_pixel(imagem, pontoAtual)
                        if pixel[3] == 0:
                            continue
                        if pixel[2] == 255:
                            pontos.append(pontoAtual)
                    except Exception:
                        pass
            if len(pontos) == 1:
                self.append(pontos[0])
            else:
                for ponto in pontos:
                    novaLinha = self.copy()
                    novaLinha.append(ponto)
                    novaLinha.procuraLinhaAzul(imagem)
                    if len(novaLinha) > len(self):
                        self.copy(novaLinha)
                break

    def sortAll(self) -> None:
        linhas = self.separa()
        self.pontos = []
        for linha in linhas:
            linha.sort()
            self.copy(self + linha)

    def separa(self) -> list["Linha"]:
        linhas: list["Linha"] = []
        for ponto in self.pontos:
            linhasQueTemOPonto: list[int] = []
            for index, linha in enumerate(linhas):
                for novoPonto in linha.pontos:
                    if distancia(ponto, novoPonto) <= 2 ** (1 / 2) + 0.01:
                        linhasQueTemOPonto.append(index)
                        break
            if len(linhasQueTemOPonto) == 0:
                linhas.append(Linha([ponto]))
            elif len(linhasQueTemOPonto) == 1:
                linhas[linhasQueTemOPonto[0]].append(ponto)
            else:
                superLinha = linhas[linhasQueTemOPonto[0]].copy()
                for n in linhasQueTemOPonto[1:]:
                    superLinha += linhas[n]
                for n in reversed(sorted(linhasQueTemOPonto)):
                    linhas.pop(n)
                superLinha.append(ponto)
                linhas.append(superLinha)
        return linhas

    def sort(self) -> None:
        tamanho = len(self)
        maiorLinha = Linha()
        for n in range(tamanho):
            linhaTeste = self.copy()
            primeiroPonto = self.pontos[n]
            linhaTeste.sortIt(Linha([primeiroPonto]))
            if len(linhaTeste) == tamanho:
                maiorLinha = linhaTeste.copy()
                break
            if len(linhaTeste) > len(maiorLinha):
                maiorLinha = linhaTeste.copy()
        self.copy(maiorLinha)

    def sortIt(self, linhaOrdenada: "Linha") -> None:
        while True:
            pontoInicial = linhaOrdenada.fim
            pontos: list[CoordData] = []
            for d in Direction:
                pontoAtual = apply_direction(pontoInicial, d)
                if pontoAtual in self:
                    if pontoAtual not in linhaOrdenada:
                        pontos.append(pontoAtual)
            if len(pontos) == 1:
                linhaOrdenada.append(pontos[0])
            else:
                for ponto in pontos:
                    novaLinha = self.copy()
                    novaLinha.sortIt(linhaOrdenada + [ponto])
                    if len(novaLinha) == len(self):
                        linhaOrdenada = novaLinha.copy()
                        break
                    if len(novaLinha) > len(linhaOrdenada):
                        linhaOrdenada = novaLinha.copy()
                break
        self.copy(linhaOrdenada)

    def divide(self, divisor: int, inicio: int) -> list["Linha"]:
        particoes = [0] * divisor
        for index in range(len(self)):
            particoes[index % divisor] += 1
        linhas: list["Linha"] = []
        for index in range(divisor):
            linha = Linha()
            inicioParticao = inicio + sum(particoes[:index])
            fimParticao = inicioParticao + particoes[index]
            for ponto in self.pontos[inicioParticao:fimParticao]:
                linha.append(ponto)
            if index == divisor - 1:
                for ponto in self.pontos[:inicio]:
                    linha.append(ponto)
            linhas.append(linha)
        return linhas

    def escreve(self, other: "Linha", file: TextIOWrapper) -> None:
        if len(self) == len(other):
            for self_ponto, other_ponto in zip(self.pontos, other.pontos):
                file.write(f"{self_ponto[0]},{self_ponto[1]}")
                file.write(f" {other_ponto[0]},{other_ponto[1]}\n")
        elif len(self) > len(other):
            if len(self) - 1 == 0:
                multiplicador = 0.0
            else:
                multiplicador = (len(other) - 1) / (len(self) - 1)
            for index in range(len(self)):
                pontoInicial = self.pontos[index]
                pontoFinal = other.pontos[int(index * multiplicador)]
                file.write(f"{pontoInicial[0]},{pontoInicial[1]}")
                file.write(f" {pontoFinal[0]},{pontoFinal[1]}\n")
        else:
            if len(other) - 1 == 0:
                multiplicador = 0.0
            else:
                multiplicador = (len(self) - 1) / (len(other) - 1)
            for index in range(len(other)):
                pontoInicial = self.pontos[int(index * multiplicador)]
                pontoFinal = other.pontos[index]
                file.write(f"{pontoInicial[0]},{pontoInicial[1]}")
                file.write(f" {pontoFinal[0]},{pontoFinal[1]}\n")

    def copy(self, other: "Linha | None" = None) -> "Linha":
        if other is None:
            return Linha(self.pontos)
        else:
            self.pontos = other.pontos
            self.inicio = other.inicio
            self.fim = other.fim
            return self

    def append(self, elemento: CoordData) -> None:
        self.pontos.append(elemento)
        self.fim = elemento
        if self.inicio is None:
            self.inicio = elemento

    def __contains__(self, elemento: CoordData) -> bool:
        if elemento in self.pontos:
            return True
        return False

    def __add__(self, other: "Linha | list[CoordData] | Any") -> "Linha":
        resultado = self.copy()
        if isinstance(other, list):
            resultado.pontos += other
            resultado.fim = other[-1]
        elif isinstance(other, Linha):
            resultado.pontos += other.pontos
            resultado.fim = other.fim
        return resultado

    def __len__(self):
        return len(self.pontos)

    def __str__(self):
        return str(self.pontos)


class Area:
    def __init__(self, imagem: Image.Image, linhaInicial: "Linha | None" = None):
        self.imagem = imagem
        self.linhas: list["Linha"] = []
        if linhaInicial is None:
            self.procuraContornoVerde()
        else:
            self.linhas.append(linhaInicial)
        self.procuraLinhas()

    def procuraContornoVerde(self) -> None:
        contorno: list[CoordData] = []
        largura, altura = self.imagem.size
        for y in range(altura):
            isUltimoPixelSolid = False
            for x in range(largura):
                isPixelAtualSolid = get_pixel(self.imagem, (x, y))[3] == 255
                if (not isUltimoPixelSolid) and isPixelAtualSolid:
                    if (x, y) not in contorno:
                        contorno.append((x, y))
                if (not isPixelAtualSolid) and isUltimoPixelSolid:
                    if (x - 1, y) not in contorno:
                        contorno.append((x - 1, y))
                isUltimoPixelSolid = isPixelAtualSolid
            if isUltimoPixelSolid:
                if (largura - 1, y) not in contorno:
                    contorno.append((largura - 1, y))
        for x in range(largura):
            isUltimoPixelSolid = False
            for y in range(altura):
                isPixelAtualSolid = get_pixel(self.imagem, (x, y))[3] == 255
                if (not isUltimoPixelSolid) and isPixelAtualSolid:
                    if (x, y) not in contorno:
                        contorno.append((x, y))
                if (not isPixelAtualSolid) and isUltimoPixelSolid:
                    if (x, y - 1) not in contorno:
                        contorno.append((x, y - 1))
                isUltimoPixelSolid = isPixelAtualSolid
            if isUltimoPixelSolid:
                if (x, altura - 1) not in contorno:
                    contorno.append((x, altura - 1))
        linhaInicial = Linha(contorno)
        linhaInicial.sortAll()
        self.linhas.append(linhaInicial)

    def procuraLinhas(self):
        linhaAtual = Linha()
        linhaAnterior = self.linhas[-1]
        for coord in linhaAnterior.pontos:
            for direcao in ORTHOGONAL_DIRECTIONS:
                coordenada = apply_direction(coord, direcao)
                try:
                    pixel = get_pixel(self.imagem, coordenada)
                except Exception:
                    continue
                if pixel[3] != 0:
                    if pixel[1] == 255:
                        if coordenada not in linhaAtual:
                            if coordenada not in self:
                                linhaAtual.append(coordenada)
        if len(linhaAtual) > 0:
            linhaAtual.sortAll()
            self.linhas.append(linhaAtual)
            self.procuraLinhas()

    def imprimeArea(self, imagem: Image.Image) -> None:
        for linha in self.linhas:
            linhas = [linha]  # separaLinha(linha)
            for linha in linhas:
                cor = tuple([randint(0, 255) for _ in range(3)])
                for coord in linha.pontos:
                    imagem.putpixel(coord, cor)
        path = "./partesConfig"
        imagem.save(f"{path}/debugArea{len(os.listdir(path)):03d}.png")

    def escreve(self, other: "Area", file: TextIOWrapper) -> None:
        if len(self) == len(other):
            for self_linha, other_linha in zip(self.linhas, other.linhas):
                self_linha.escreve(other_linha, file)
        elif len(self) > len(other):
            if len(self) - 1 == 0:
                multiplicador = 0.0
            else:
                multiplicador = (len(other) - 1) / (len(self) - 1)
            for index in range(len(self)):
                linhaFinal = other.linhas[int(index * multiplicador)]
                self.linhas[index].escreve(linhaFinal, file)
        else:
            if len(other) - 1 == 0:
                multiplicador = 0.0
            else:
                multiplicador = (len(self) - 1) / (len(other) - 1)
            for index in range(len(other)):
                linhaInicial = self.linhas[int(index * multiplicador)]
                linhaInicial.escreve(other.linhas[index], file)

    def __contains__(self, other: CoordData) -> bool:
        for linha in self.linhas:
            if other in linha:
                return True
        return False

    def __len__(self):
        return len(self.linhas)


class ImagemParte:
    def __init__(self, indice: int, nome: str) -> None:
        imagem = convertePypdnToPil(nome, indice)
        azul = self.azulInicial(imagem)
        if azul:
            linha = Linha([azul])
            linha.procuraLinhaAzul(imagem)
            self.area = Area(imagem, linhaInicial=linha)
        else:
            self.area = Area(imagem, None)
        imagem.close()

    def azulInicial(self, imagem: Image.Image) -> CoordData | Literal[False]:
        largura, altura = imagem.size
        for x in range(largura):
            for y in range(altura):
                pixel = get_pixel(imagem, (x, y))
                if pixel[3] == 0:
                    continue
                if pixel[2] == 200:
                    return (x, y)
        return False

    def escreveArea(self, other: "ImagemParte", file: TextIOWrapper) -> None:
        self.area.escreve(other.area, file)


def limpaPasta(pasta: str) -> None:
    arquivos = [f"{pasta}/{a}" for a in os.listdir(pasta)]
    if "./frames/resized" in arquivos:
        arquivos.pop(arquivos.index("./frames/resized"))
    for arquivo in arquivos:
        os.remove(arquivo)


class Direction(Enum):
    DOWN_RIGHT = 0
    DOWN = 1
    DOWN_LEFT = 2
    LEFT = 3
    UP_LEFT = 4
    UP = 5
    UP_RIGHT = 6
    RIGHT = 7


ORTHOGONAL_DIRECTIONS = [Direction.DOWN, Direction.LEFT, Direction.UP, Direction.RIGHT]


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


def distancia(pontoA: CoordData, pontoB: CoordData) -> float:
    soma = 0
    for coord_a, coord_b in zip(pontoA, pontoB):
        soma += abs(coord_a - coord_b) ** 2
    return soma ** (1 / 2)


def convertePypdnToPil(nome: str, indice: int) -> Image.Image:
    layeredImage = pypdn.read(nome)
    imageLayer = layeredImage.layers[indice]
    imageArray = imageLayer.image
    imagem = Image.fromarray(imageArray)
    layeredImage = imageLayer = imageArray = None
    return imagem


def configPart(indice: int) -> None:
    print(f"Fazendo Parte : {indice}")
    parteInicial = ImagemParte(indice, "./inicial.pdn")
    print("a")
    parteFinal = ImagemParte(indice, "./final.pdn")
    print("b")
    with open(
        f"./partesConfig/parte{indice:02d}Config.txt", "w", encoding="utf-8"
    ) as fileConfig:
        print("c")
        parteInicial.escreveArea(parteFinal, fileConfig)
        print(f"\tParte Terminada : {indice}")


def main() -> None:
    limpaPasta("./partesConfig")
    limpaPasta("./frames")
    limpaPasta("./frames/resized")
    limpaPasta("./debug")
    imagemInicial = pypdn.read("./inicial.pdn")
    imagemFinal = pypdn.read("./final.pdn")
    Image.fromarray(imagemInicial.layers[0].image).save("./inicial.png")
    Image.fromarray(imagemFinal.layers[0].image).save("./final.png")
    quantiaPartes = len(imagemInicial.layers)
    imagemInicial = None
    imagemFinal = None
    for a in range(2, quantiaPartes):
        configPart(a)


if __name__ == "__main__":
    main()
