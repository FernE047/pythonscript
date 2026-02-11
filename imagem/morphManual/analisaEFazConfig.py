from enum import Enum
from io import TextIOWrapper
from typing import Literal, cast
from PIL import Image
import os
import multiprocessing
from random import randint

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


class Linha:
    def __init__(
        self, pontos: list[CoordData] | None = None, circular: bool = False
    ) -> None:
        self.circular = circular
        if pontos is None:
            self.pontos: list[CoordData] = []
            self.inicio = None
            self.fim = None
            return
        self.pontos = pontos.copy()
        if len(self.pontos) == 0:
            self.inicio = None
            self.fim = None
            return
        self.inicio = self.pontos[0]
        self.fim = self.pontos[-1]

    def procuraLinhaAzul(self, imagem: Image.Image) -> None:
        while True:
            pontoInicial = self.fim
            pontos: list[CoordData] = []
            for direction in Direction:
                pontoAtual = apply_direction(pontoInicial, direction)
                if pontoAtual in self:
                    continue
                try:
                    pixel = get_pixel(imagem, pontoAtual)
                except IndexError:
                    continue
                if pixel[3] == 0:
                    continue
                if pixel[2] == 255:
                    pontos.append(pontoAtual)
            if len(pontos) == 1:
                self.append(pontos[0])
                continue
            for ponto in pontos:
                novaLinha = self.copy()
                novaLinha.append(ponto)
                novaLinha.procuraLinhaAzul(imagem)
                if len(novaLinha) <= len(self):
                    continue
                self.clone(novaLinha)
            break

    def sortAll(self) -> None:
        linhas = self.separa()
        self.pontos = []
        for linha in linhas:
            linha.sort()
            self.clone(self + linha)

    def separa(self) -> list["Linha"]:
        linhas: list[Linha] = []
        neighbor_distance = 2 ** (1 / 2) + 0.01
        for ponto in self.pontos:
            linhasQueTemOPonto: list[int] = []
            for index, linha in enumerate(linhas):
                for novoPonto in linha.pontos:
                    if distancia(ponto, novoPonto) > neighbor_distance:
                        continue
                    linhasQueTemOPonto.append(index)
                    break
            if len(linhasQueTemOPonto) == 0:
                linhas.append(Linha([ponto], circular=self.circular))
                continue
            if len(linhasQueTemOPonto) == 1:
                linhas[linhasQueTemOPonto[0]].append(ponto)
                continue
            superLinha = linhas[linhasQueTemOPonto[0]].copy()
            for line_index in linhasQueTemOPonto[1:]:
                superLinha += linhas[line_index]
            for line_index in reversed(sorted(linhasQueTemOPonto)):
                linhas.pop(line_index)
            superLinha.append(ponto)
            linhas.append(superLinha)
        return linhas

    def sort(self) -> None:
        tamanho = len(self)
        maiorLinha = Linha(circular=self.circular)
        for coord_index in range(min(4, tamanho)):
            linhaTeste = self.copy()
            primeiroPonto = self.pontos[coord_index]
            linhaTeste.sortIt(Linha([primeiroPonto], circular=self.circular))
            if len(linhaTeste) == tamanho:
                maiorLinha = linhaTeste.copy()
                break
            if len(linhaTeste) <= len(maiorLinha):
                continue
            maiorLinha = linhaTeste.copy()
        self.clone(maiorLinha)

    def sortIt(self, linhaOrdenada: "Linha") -> None:
        while True:
            pontoInicial = linhaOrdenada.pontos[-1]
            pontos = self.pontosProximos(pontoInicial, exceptions=linhaOrdenada)
            if len(pontos) == 1:
                linhaOrdenada.append(pontos[0])
                continue
            if len(pontos) == 0:
                if not self.circular:
                    maiorLinha = linhaOrdenada.copy()
                    continue
                indice = self.pontos.index(pontoInicial)
                if indice < len(self) - 1:
                    linhaOrdenada.append(self.pontos[indice + 1])
                    continue
                maiorLinha = linhaOrdenada.copy()
                continue
            antes = len(linhaOrdenada)
            for ponto in pontos:
                pontosProximosDele = self.pontosProximos(
                    ponto, exceptions=linhaOrdenada
                )
                if len(pontosProximosDele) != 1:
                    continue
                if pontosProximosDele[0] in pontos:
                    linhaOrdenada.append(ponto)
                    linhaOrdenada.append(pontosProximosDele[0])
                    break
            if len(linhaOrdenada) != antes:
                continue
            maiorLinha = linhaOrdenada.copy()
            for ponto in pontos:
                novaLinha = self.copy()
                novaLinha.sortIt(linhaOrdenada + [ponto])
                if len(novaLinha) == len(self):
                    maiorLinha = novaLinha.copy()
                    break
                if len(novaLinha) <= len(maiorLinha):
                    continue
                maiorLinha = novaLinha.copy()
            break
        self.clone(maiorLinha)

    def pontosProximos(
        self, ponto: CoordData, exceptions: "Linha | None" = None
    ) -> list[CoordData]:
        if exceptions is None:
            exceptions = Linha()
        pontos: list[CoordData] = []
        for direction in Direction:
            pontoAtual = apply_direction(ponto, direction)
            if pontoAtual not in self:
                continue
            if pontoAtual in exceptions:
                continue
            if not self.circular:
                pontos.append(pontoAtual)
                continue
            distance = self.pontos.index(pontoAtual) - self.pontos.index(ponto)
            if abs(distance) < 5:
                pontos.append(pontoAtual)
        return pontos

    def divide(self, divisor: int, inicio: int) -> list["Linha"]:
        particoes = [0] * divisor
        for index in range(len(self)):
            particoes[index % divisor] += 1
        linhas: list[Linha] = []
        for index in range(divisor):
            linha = Linha(circular=self.circular)
            inicioParticao = inicio + sum(particoes[:index])
            fimParticao = inicioParticao + particoes[index]
            for ponto in self.pontos[inicioParticao:fimParticao]:
                linha.append(ponto)
            if index == divisor - 1:
                for ponto in self.pontos[:inicio]:
                    linha.append(ponto)
            linhas.append(linha)
        return linhas

    def melhorPonto(self) -> CoordData:
        melhor = (float("inf"), float("inf"))
        for ponto in self.pontos:
            if ponto[1] < melhor[1]:
                melhor = ponto
                continue
            if ponto[1] != melhor[1]:
                continue
            if ponto[0] < melhor[0]:
                melhor = ponto
        if melhor == (float("inf"), float("inf")):
            raise Exception("Linha sem pontos")
        return cast(CoordData, melhor)

    def gira(self, novoInicio: CoordData) -> None:
        if novoInicio not in self:
            return
        while self.pontos[0] != novoInicio:
            self.append(self.pontos[0])
            self.pontos.pop(0)
            self.inicio = self.pontos[0]

    def makeCamada(self) -> list["Linha"]:
        perimetro = len(self)
        tamanhoSeccao = int((perimetro - 0.1) // 4 + 1)
        if perimetro <= 4:
            camada: list[Linha] = []
            for a in range(perimetro):
                camada.append(Linha([self.pontos[a]], circular=self.circular))
            while len(camada) != 4:
                camada.append(Linha([self.pontos[-1]], circular=self.circular))
            return camada
        camada = []
        melhorPontuacao = float("inf")
        for inicioSeccao in range(tamanhoSeccao):
            novaCamada = self.divide(4, inicioSeccao)
            maiorY = novaCamada[0].pontoMedio()[1]
            linhaDeBaixo = novaCamada[0]
            for n in range(1, 4):
                if novaCamada[n].pontoMedio()[1] <= maiorY:
                    continue
                maiorY = novaCamada[n].pontoMedio()[1]
                linhaDeBaixo = novaCamada[n]
            while novaCamada[0] != linhaDeBaixo:
                novaCamada = [novaCamada[-1]] + novaCamada
                novaCamada.pop()
            pontuacao = 0
            for a in range(4):
                if a % 2 == 0:
                    pontuacao += abs(
                        novaCamada[a].pontos[-1][1] - novaCamada[a].pontos[0][1]
                    )
                else:
                    pontuacao += abs(
                        novaCamada[a].pontos[-1][0] - novaCamada[a].pontos[0][0]
                    )
            if pontuacao < melhorPontuacao:
                camada = novaCamada.copy()
                melhorPontuacao = pontuacao
        if camada[1].pontoMedio()[0] <= camada[3].pontoMedio()[0]:
            return camada
        novaCamada = [camada[a] for a in (0, 3, 2, 1)]
        for linha in camada:
            linha.pontos = list(reversed(linha.pontos))
            linha.inicio = linha.pontos[0]
            linha.fim = linha.pontos[-1]
        return novaCamada

    def pontoMedio(self) -> CoordData:
        x = 0
        y = 0
        for ponto in self.pontos:
            x += ponto[0]
            y += ponto[1]
        xmedio = x // len(self)
        ymedio = y // len(self)
        return (xmedio, ymedio)

    def escreve(self, other: "Linha", file: TextIOWrapper) -> None:
        if len(self) == len(other):
            for index in range(len(self)):
                file.write(f"{self.pontos[index][0]},{self.pontos[index][1]}")
                file.write(f" {other.pontos[index][0]},{other.pontos[index][1]}\n")
            return
        if len(self) > len(other):
            if len(self) - 1 == 0:
                multiplicador = 0.0
            else:
                multiplicador = (len(other) - 1) / (len(self) - 1)
            for index in range(len(self)):
                pontoInicial = self.pontos[index]
                pontoFinal = other.pontos[int(index * multiplicador)]
                file.write(f"{pontoInicial[0]},{pontoInicial[1]}")
                file.write(f" {pontoFinal[0]},{pontoFinal[1]}\n")
            return
        if len(other) - 1 == 0:
            multiplicador = 0.0
        else:
            multiplicador = (len(self) - 1) / (len(other) - 1)
        for index in range(len(other)):
            pontoInicial = self.pontos[int(index * multiplicador)]
            pontoFinal = other.pontos[index]
            file.write(f"{pontoInicial[0]},{pontoInicial[1]}")
            file.write(f" {pontoFinal[0]},{pontoFinal[1]}\n")

    def imprime(self, imagem: Image.Image) -> None:
        transparencia = 255
        for ponto in self.pontos:
            imagem.putpixel(ponto, tuple([0, 0, 0, transparencia]))
            transparencia -= 1
            if transparencia <= 80:
                transparencia = 255
        directory = "./debug"
        unique_id = len(os.listdir(directory))
        name = f"./debug/{unique_id:03d}.png"
        imagem.save(name)

    def clone(self, other: "Linha") -> "Linha":
        self.pontos = other.pontos
        self.inicio = other.inicio
        self.fim = other.fim
        self.circular = other.circular
        return self

    def copy(self) -> "Linha":
        return Linha(self.pontos, circular=self.circular)

    def append(self, elemento: "Linha | CoordData") -> None:
        if isinstance(elemento, Linha):
            for ponto in elemento.pontos:
                self.append(ponto)
            return
        self.pontos.append(elemento)
        self.fim = elemento
        if self.inicio is None:
            self.inicio = elemento

    def __contains__(self, elemento: "CoordData") -> bool:
        if elemento in self.pontos:
            return True
        return False

    def __add__(self, other: "Linha | list[CoordData]") -> "Linha":
        resultado = self.copy()
        if isinstance(other, list):
            resultado.pontos += other
            resultado.fim = other[-1]
            return resultado
        resultado.pontos += other.pontos
        resultado.fim = other.fim
        return resultado

    def __len__(self) -> int:
        return len(self.pontos)

    def __str__(self) -> str:
        return str(self.pontos)


class Area:
    def __init__(
        self, imagem: Image.Image, linhaInicial: "Linha | None" = None
    ) -> None:
        self.imagem = imagem
        self.linhas: list[Linha] = []
        if linhaInicial is None:
            self.circular = True
            self.procuraContornoVerde()
        else:
            self.circular = False
            self.linhas.append(linhaInicial)
        self.procuraLinhas()

    def procuraContornoVerde(self) -> None:
        contorno: list[CoordData] = []
        largura, altura = self.imagem.size
        for y in range(altura):
            isUltimoPixelSolid = False
            for x in range(largura):
                pixel = get_pixel(self.imagem, (x, y))
                isPixelAtualSolid = pixel[3] == 255
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
                pixel = get_pixel(self.imagem, (x, y))
                isPixelAtualSolid = pixel[3] == 255
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
        camada = linhaInicial.makeCamada()
        linhaInicial = camada[0]
        for indice in range(1, 4):
            linhaInicial.append(camada[indice])
        self.linhas.append(linhaInicial)

    def procuraLinhas(self) -> None:
        linhaAtual = Linha()
        linhaAnterior = self.linhas[-1]
        for coord in linhaAnterior.pontos:
            for direction in ORTHOGONAL_DIRECTIONS:
                coordenada = apply_direction(coord, direction)
                try:
                    pixel = get_pixel(self.imagem, coordenada)
                except IndexError:
                    continue
                if pixel[3] == 0:
                    continue
                if coordenada in linhaAtual:
                    continue
                if coordenada in self:
                    continue
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
        unique_id = len(os.listdir(path))
        imagem.save(f"{path}/debugArea{unique_id:03d}.png")

    def escreve(self, other: "Area", file: TextIOWrapper) -> None:
        if len(self) == len(other):
            for self_linha, other_linha in zip(self.linhas, other.linhas):
                self_linha.escreve(other_linha, file)
            return
        if len(self) > len(other):
            if len(self) - 1 == 0:
                multiplicador = 0.0
            else:
                multiplicador = (len(other) - 1) / (len(self) - 1)
            for index in range(len(self)):
                linhaFinal = other.linhas[int(index * multiplicador)]
                self.linhas[index].escreve(linhaFinal, file)
            return
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

    def __len__(self) -> int:
        return len(self.linhas)


class AreaVermelha:  # maybe add a separation for larger areas
    def __init__(self, imagem: Image.Image) -> None:
        self.imagem = imagem
        self.regioes: list[list[Linha]] = []
        self.procuraContornoVermelho()
        self.procuraCamadas()

    def procuraContornoVermelho(self) -> None:
        contorno: list[CoordData] = []
        largura, altura = self.imagem.size
        for y in range(altura):
            isUltimoPixelSolid = False
            for x in range(largura):
                pixel = get_pixel(self.imagem, (x, y))
                isPixelAtualSolid = pixel[3] == 255
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
                pixel = get_pixel(self.imagem, (x, y))
                isPixelAtualSolid = pixel[3] == 255
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
        linhaInicial.sort()
        camada = linhaInicial.makeCamada()
        for linha in camada:
            self.regioes.append([linha])

    def procuraCamadas(self) -> None:
        self.imprimeCamadas("nome")
        alterationDone = False
        for indice in [0, 2, 1, 3]:
            linhaAtual = Linha(circular=True)
            linhaAnterior = self.regioes[indice][-1]
            for coord in linhaAnterior.pontos:
                for direction in ORTHOGONAL_DIRECTIONS:
                    coordenada = apply_direction(coord, direction)
                    try:
                        pixel = get_pixel(self.imagem, coordenada)
                    except IndexError:
                        continue
                    if pixel[3] == 0:
                        continue
                    if coordenada in linhaAtual:
                        continue
                    if coordenada in self:
                        continue
                    linhaAtual.append(coordenada)
            if len(linhaAtual) == 0:
                continue
            linhaAtual.sortAll()
            self.regioes[indice].append(linhaAtual)
            alterationDone = True
        if alterationDone:
            self.procuraCamadas()

    def imprimeRegioes(self, nome: str, indice: int) -> None:
        for regiao in self.regioes:
            for linha in regiao:
                cor = [randint(0, 255) for _ in range(3)]
                transparencia = 255
                for coord in linha.pontos:
                    self.imagem.putpixel(coord, tuple(cor + [transparencia]))
                    if transparencia:
                        transparencia -= 1
        self.imagem.save(f"./debug/{nome}_{indice:03d}.png")

    def imprimeCamadas(self, nome: str) -> None:
        maximoLinhas = self.tamanhoMaiorRegiao()
        for indice in range(maximoLinhas):
            transparencia = 255
            for regiao in self.regioes:
                if indice >= len(regiao):
                    continue
                linha = regiao[indice]
                cor = [randint(0, 255) for _ in range(3)]
                for coord in linha.pontos:
                    self.imagem.putpixel(coord, tuple(cor + [transparencia]))
                    transparencia -= 1
                    if transparencia <= 80:
                        transparencia = 255
        directory = "./debug"
        index = sum(
            [1 if file.find(nome) != -1 else 0 for file in os.listdir(directory)]
        )
        name = f"{directory}/{index:03d}/{nome}.png"
        self.imagem.save(name)

    def escreve(self, other: "AreaVermelha", file: TextIOWrapper) -> None:
        for indice in range(4):
            if len(self.regioes[indice]) == len(other.regioes[indice]):
                for self_regiao, other_regiao in zip(
                    self.regioes[indice], other.regioes[indice]
                ):
                    self_regiao.escreve(other_regiao, file)
                continue
            if len(self.regioes[indice]) > len(other.regioes[indice]):
                if len(self.regioes[indice]) - 1 == 0:
                    multiplicador = 0.0
                else:
                    multiplicador = (len(other.regioes[indice]) - 1) / (
                        len(self.regioes[indice]) - 1
                    )
                for index in range(len(self.regioes[indice])):
                    linhaFinal = other.regioes[indice][int(index * multiplicador)]
                    self.regioes[indice][index].escreve(linhaFinal, file)
                continue
            if len(other.regioes[indice]) - 1 == 0:
                multiplicador = 0.0
            else:
                multiplicador = (len(self.regioes[indice]) - 1) / (
                    len(other.regioes[indice]) - 1
                )
            for index in range(len(other.regioes[indice])):
                linhaInicial = self.regioes[indice][int(index * multiplicador)]
                linhaInicial.escreve(other.regioes[indice][index], file)

    def __contains__(self, other: CoordData) -> bool:
        for regiao in self.regioes:
            for linha in regiao:
                if other in linha:
                    return True
        return False

    def __len__(self) -> int:
        return len(self.regioes)

    def tamanhoMaiorRegiao(self) -> int:
        tamanho = float("-inf")
        for regiao in self.regioes:
            if len(regiao) > tamanho:
                tamanho = len(regiao)
        if isinstance(tamanho, float):
            raise Exception("AreaVermelha sem regioes")
        return tamanho


class ImagemParte:
    area: Area | AreaVermelha
    has_blue: Literal[False] | CoordData
    has_red: bool

    def __init__(self, nome: str) -> None:
        imagem = Image.open(nome)
        self.hasColor(imagem)
        if self.hasRed:
            self.area = AreaVermelha(imagem)
        elif self.hasBlue:
            linha = Linha([self.hasBlue])
            linha.procuraLinhaAzul(imagem)
            self.area = Area(imagem, linhaInicial=linha)
        else:
            self.area = Area(imagem)
        imagem.close()

    def hasColor(self, imagem: Image.Image) -> None:
        largura, altura = imagem.size
        self.hasRed = False
        self.hasBlue: Literal[False] | CoordData = False
        for x in range(largura):
            for y in range(altura):
                pixel = get_pixel(imagem, (x, y))
                if pixel[3] == 0:
                    continue
                if pixel[0] == 255:
                    self.hasRed = True
                    break
                if pixel[2] == 200:
                    self.hasBlue = (x, y)
                    break
            if self.hasBlue or self.hasRed:
                break

    def escreveArea(self, other: "ImagemParte", file: TextIOWrapper) -> None:
        if isinstance(self.area, Area) and isinstance(other.area, Area):
            self.area.escreve(other.area, file)
            return
        if isinstance(self.area, AreaVermelha) and isinstance(other.area, AreaVermelha):
            self.area.escreve(other.area, file)
            return
        raise Exception("Imagens incompatíveis para escrita")


def distancia(pontoA: CoordData, pontoB: CoordData) -> float:
    soma = 0
    for coord_a, coord_b in zip(pontoA, pontoB):
        soma += abs(coord_a - coord_b) ** 2
    return soma ** (1 / 2)


def configPart(indice: int) -> None:
    print("Fazendo Parte : " + str(indice))
    parteInicial = ImagemParte(f"./partes/iniciais/{indice:03d}.png")
    parteFinal = ImagemParte(f"./partes/finais/{indice:03d}.png")
    with open(
        f"./partes/config/{indice:03d}.txt",
        "w",
        encoding="utf-8",
    ) as fileConfig:
        parteInicial.escreveArea(parteFinal, fileConfig)
        print("\tParte Terminada : " + str(indice))


def main() -> None:
    quantiaPartes = len(os.listdir("./partes/finais"))
    p = multiprocessing.Pool(os.cpu_count())
    p.map(configPart, range(quantiaPartes))


if __name__ == "__main__":
    main()
