from PIL import Image
import os
import pypdn
import multiprocessing
from random import randint
from enum import Enum

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
    def __init__(self, pontos=None):
        if pontos is None:
            self.pontos = []
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

    def procuraLinhaAzul(self, imagem):
        while True:
            pontoInicial = self.fim
            pontos = []
            for d in range(8):
                pontoAtual = coordDirecao(pontoInicial, d)
                if pontoAtual not in self:
                    try:
                        pixel = imagem.getpixel(pontoAtual)
                        if pixel[3] == 0:
                            continue
                        if pixel[2] == 255:
                            pontos.append(pontoAtual)
                    except:
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

    def sortAll(self):
        linhas = self.separa()
        self.pontos = []
        for linha in linhas:
            linha.sort()
            self.copy(self + linha)

    def separa(self):
        linhas = []
        for ponto in self.pontos:
            linhasQueTemOPonto = []
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

    def sort(self):
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

    def sortIt(self, linhaOrdenada):
        while True:
            pontoInicial = linhaOrdenada.fim
            pontos = []
            for d in range(8):
                pontoAtual = coordDirecao(pontoInicial, d)
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

    def divide(self, divisor, inicio):
        particoes = [0] * divisor
        for index in range(len(self)):
            particoes[index % divisor] += 1
        linhas = []
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

    def escreve(self, other, file):
        if len(self) == len(other):
            for self_ponto, other_ponto in zip(self, other):
                file.write(str(self_ponto[0]) + "," + str(self_ponto[1]))
                file.write(" " + str(other_ponto[0]) + "," + str(other_ponto[1]) + "\n")
        elif len(self) > len(other):
            if len(self) - 1 == 0:
                multiplicador = 0
            else:
                multiplicador = (len(other) - 1) / (len(self) - 1)
            for index in range(len(self)):
                pontoInicial = self.pontos[index]
                pontoFinal = other.pontos[int(index * multiplicador)]
                file.write(str(pontoInicial[0]) + "," + str(pontoInicial[1]))
                file.write(" " + str(pontoFinal[0]) + "," + str(pontoFinal[1]) + "\n")
        else:
            if len(other) - 1 == 0:
                multiplicador = 0
            else:
                multiplicador = (len(self) - 1) / (len(other) - 1)
            for index in range(len(other)):
                pontoInicial = self.pontos[int(index * multiplicador)]
                pontoFinal = other.pontos[index]
                file.write(str(pontoInicial[0]) + "," + str(pontoInicial[1]))
                file.write(" " + str(pontoFinal[0]) + "," + str(pontoFinal[1]) + "\n")

    def copy(self, other=None):
        if other is None:
            return Linha(self.pontos)
        else:
            self.pontos = other.pontos
            self.inicio = other.inicio
            self.fim = other.fim

    def append(self, elemento):
        self.pontos.append(elemento)
        self.fim = elemento
        if self.inicio is None:
            self.inicio = elemento

    def __contains__(self, elemento):
        if elemento in self.pontos:
            return True
        return False

    def __add__(self, other):
        resultado = self.copy()
        if type(other) is list:
            resultado.pontos += other
            resultado.fim = other[-1]
        elif type(other) is Linha:
            resultado.pontos += other.pontos
            resultado.fim = other.fim
        return resultado

    def __len__(self):
        return len(self.pontos)

    def __str__(self):
        return str(self.pontos)


class Area:
    def __init__(self, imagem, linhaInicial=None):
        self.imagem = imagem
        self.linhas = []
        if linhaInicial is None:
            self.procuraContornoVerde()
        else:
            self.linhas.append(linhaInicial)
        self.procuraLinhas()

    def procuraContornoVerde(self):
        contorno = []
        largura, altura = self.imagem.size
        for y in range(altura):
            isUltimoPixelSolid = False
            for x in range(largura):
                isPixelAtualSolid = self.imagem.getpixel((x, y))[3] == 255
                if (not isUltimoPixelSolid) and isPixelAtualSolid:
                    if (x, y) not in contorno:
                        contorno.append((x, y))
                if (not isPixelAtualSolid) and isUltimoPixelSolid:
                    if (x - 1, y) not in contorno:
                        contorno.append((x - 1, y))
                isUltimoPixelSolid = isPixelAtualSolid
            if isUltimoPixelSolid:
                if (x - 1, y) not in contorno:
                    contorno.append((x - 1, y))
        for x in range(largura):
            isUltimoPixelSolid = False
            for y in range(altura):
                isPixelAtualSolid = self.imagem.getpixel((x, y))[3] == 255
                if (not isUltimoPixelSolid) and isPixelAtualSolid:
                    if (x, y) not in contorno:
                        contorno.append((x, y))
                if (not isPixelAtualSolid) and isUltimoPixelSolid:
                    if (x, y - 1) not in contorno:
                        contorno.append((x, y - 1))
                isUltimoPixelSolid = isPixelAtualSolid
            if isUltimoPixelSolid:
                if (x, y - 1) not in contorno:
                    contorno.append((x, y - 1))
        linhaInicial = Linha(contorno)
        linhaInicial.sortAll()
        self.linhas.append(linhaInicial)

    def procuraLinhas(self):
        linhaAtual = Linha()
        linhaAnterior = self.linhas[-1]
        for coord in linhaAnterior.pontos:
            for direcao in (1, 3, 5, 7):
                coordenada = coordDirecao(coord, direcao)
                try:
                    pixel = self.imagem.getpixel(coordenada)
                except:
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

    def imprimeArea(self, imagem):
        for linha in self:
            linhas = [linha]  # separaLinha(linha)
            for linha in linhas:
                cor = tuple([randint(0, 255) for a in range(3)])
                for coord in linha.pontos:
                    imagem.putpixel(coord, cor)
        path = "./partesConfig"
        imagem.save(f"{path}/debugArea{len(os.listdir(path)):03d}.png")

    def escreve(self, other, file):
        if len(self) == len(other):
            for self_linha, other_linha in zip(self, other):
                self_linha.escreve(other_linha, file)
        elif len(self) > len(other):
            if len(self) - 1 == 0:
                multiplicador = 0
            else:
                multiplicador = (len(other) - 1) / (len(self) - 1)
            for index in range(len(self)):
                linhaFinal = other.linhas[int(index * multiplicador)]
                self.linhas[index].escreve(linhaFinal, file)
        else:
            if len(other) - 1 == 0:
                multiplicador = 0
            else:
                multiplicador = (len(self) - 1) / (len(other) - 1)
            for index in range(len(other)):
                linhaInicial = self.linhas[int(index * multiplicador)]
                linhaInicial.escreve(other.linhas[index], file)

    def __contains__(self, other):
        for linha in self.linhas:
            if other in linha:
                return True
        return False

    def __len__(self):
        return len(self.linhas)


class ImagemParte:
    def __init__(self, indice, nome):
        image = convertePypdnToPil(nome)
        azul = self.azulInicial(imagem)
        if azul:
            linha = Linha([azul])
            linha.procuraLinhaAzul(imagem)
            self.area = Area(imagem, linhaInicial=linha)
        else:
            self.area = Area(imagem, nome[-9:-4])
        imagem.close()

    def azulInicial(self, imagem):
        largura, altura = imagem.size
        for x in range(largura):
            for y in range(altura):
                pixel = imagem.getpixel((x, y))
                if pixel[3] == 0:
                    continue
                if pixel[2] == 200:
                    return (x, y)
        return False

    def escreveArea(self, other, file):
        self.area.escreve(other.area, file)


def limpaPasta(pasta):
    arquivos = [pasta + "/" + a for a in os.listdir(pasta)]
    if "./frames/resized" in arquivos:
        arquivos.pop(arquivos.index("./frames/resized"))
    for arquivo in arquivos:
        os.remove(arquivo)


def coordDirecao(coord, n):
    x, y = coord
    if n == 0:
        return (x + 1, y + 1)
    if n == 1:
        return (x, y + 1)
    if n == 2:
        return (x - 1, y + 1)
    if n == 3:
        return (x - 1, y)
    if n == 4:
        return (x - 1, y - 1)
    if n == 5:
        return (x, y - 1)
    if n == 6:
        return (x + 1, y - 1)
    if n == 7:
        return (x + 1, y)
    return (x, y)


def distancia(pontoA, pontoB):
    soma = 0
    for coord_a, coord_b in zip(pontoA, pontoB):
        soma += abs(coord_a - coord_b) ** 2
    return soma ** (1 / 2)


def convertePypdnToPil(nome):
    layeredImage = pypdn.read(nome)
    imageLayer = layeredImage.layers[indice]
    imageArray = imageLayer.image
    imagem = Image.fromarray(imageArray)
    layeredImage = imageLayer = imageArray = None
    return imagem


def configPart(indice):
    print("Fazendo Parte : " + str(indice))
    parteInicial = ImagemParte(indice, "./inicial.pdn")
    print("a")
    parteFinal = ImagemParte(indice, "./final.pdn")
    print("b")
    with open(
        f"./partesConfig/parte{indice:02d}Config.txt", "w", encoding="utf-8"
    ) as fileConfig:
        print("c")
        parteInicial.escreveArea(parteFinal, fileConfig)
        print("\tParte Terminada : " + str(indice))


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
    # p = multiprocessing.Pool(os.cpu_count())
    # p.map(configPart,range(2,quantiaPartes))


if __name__ == "__main__":
    main()
