from PIL import Image
from random import randint
from numpy.random import permutation
from os import listdir


def makeALabirint(imagem, verticesAbertos, cor):
    if verticesAbertos:
        largura, altura = imagem.size
        indice = randint(0, len(verticesAbertos) - 1)
        doThePop = True
        x, y = verticesAbertos[indice]
        for direction in permutation(4).tolist():
            if direction == 0:
                if y > 1:
                    if imagem.getpixel((x, y - 2)) == PRETO:
                        imagem.putpixel((x, y - 1), cor)
                        imagem.putpixel((x, y - 2), cor)
                        verticesAbertos.append((x, y - 2))
                        doThePop = False
                        break
            if direction == 1:
                if x < largura - 2:
                    if imagem.getpixel((x + 2, y)) == PRETO:
                        imagem.putpixel((x + 1, y), cor)
                        imagem.putpixel((x + 2, y), cor)
                        verticesAbertos.append((x + 2, y))
                        doThePop = False
                        break
            if direction == 2:
                if y < altura - 2:
                    if imagem.getpixel((x, y + 2)) == PRETO:
                        imagem.putpixel((x, y + 1), cor)
                        imagem.putpixel((x, y + 2), cor)
                        verticesAbertos.append((x, y + 2))
                        doThePop = False
                        break
            if direction == 3:
                if x > 1:
                    if imagem.getpixel((x - 2, y)) == PRETO:
                        imagem.putpixel((x - 1, y), cor)
                        imagem.putpixel((x - 2, y), cor)
                        verticesAbertos.append((x - 2, y))
                        doThePop = False
                        break
        if doThePop:
            verticesAbertos.pop(indice)


def makeAPath(imagem, quant):
    largura, altura = imagem.size
    vertices = []
    for x in range(3, largura, 2):
        for y in range(1, altura, 2):
            pixelA = imagem.getpixel((x, y))
            pixelB = imagem.getpixel((x - 2, y))
            if pixelA != pixelB:
                if (x - 1, y) not in vertices:
                    vertices.append((x - 1, y))
    for x in range(1, largura, 2):
        for y in range(3, altura, 2):
            pixelA = imagem.getpixel((x, y))
            pixelB = imagem.getpixel((x, y - 2))
            if pixelA != pixelB:
                if (x, y - 1) not in vertices:
                    vertices.append((x, y - 1))
    vertices = permutation(vertices)
    if quant > len(vertices):
        quant = len(vertices)
    for a in range(quant):
        imagem.putpixel(vertices[a], BRANCO)


def corrigeLabirint(imagem):
    largura, altura = imagem.size
    for x in range(largura):
        for y in range(altura):
            if imagem.getpixel((x, y)) not in (BRANCO, PRETO):
                imagem.putpixel((x, y), BRANCO)


BRANCO = (255, 255, 255, 255)
PRETO = (0, 0, 0, 255)
AZUL = (0, 0, 255, 255)
VERMELHO = (255, 0, 0, 255)
pathQuant = 300
largura = 100
altura = 100
if not largura % 2:
    largura += 1
if not altura % 2:
    altura += 1
verticesAbertosInicio = [(1, 1)]
verticesAbertosFinal = [(largura - 2, altura - 2)]
imagem = Image.new("RGBA", (largura, altura), (0, 0, 0, 255))
imagem.putpixel((1, 1), (AZUL))
imagem.putpixel((largura - 2, altura - 2), (VERMELHO))
while verticesAbertosInicio or verticesAbertosFinal:
    makeALabirint(imagem, verticesAbertosInicio, AZUL)
    makeALabirint(imagem, verticesAbertosFinal, VERMELHO)
makeAPath(imagem, pathQuant)
corrigeLabirint(imagem)
name = f"pureLabirint//labirint{len(listdir('pureLabirint')):04d}.png"
print(name)
imagem.save(name)
imagem.close()
