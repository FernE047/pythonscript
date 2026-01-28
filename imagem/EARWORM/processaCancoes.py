import shelve
import os
from PIL import Image


def imagensPasta(pasta):
    imagens = os.listdir(pasta)
    imagensCaminho = [os.path.join(pasta, imagem) for imagem in imagens]
    return imagensCaminho


def mediaDasImagens(imagens):
    imageNumber = 0
    alturaTotal = 0
    larguraTotal = 0
    for imagem in imagens:
        cancao = Image.open(imagem)
        largura, altura = cancao.size
        alturaTotal += altura
        larguraTotal += largura
        imageNumber += 1
    return (larguraTotal / imageNumber, alturaTotal / imageNumber)


diretorio = os.getcwd()
base = os.path.join(diretorio, "imagens")
imagens = imagensPasta(base)
for pastaMaior in ["artist", "album"]:
    base = os.path.join(diretorio, pastaMaior)
    pastas = os.listdir(base)
    pastasCaminho = [os.path.join(base, pasta) for pasta in pastas]
    for pastaCaminho in pastasCaminho:
        imagens += imagensPasta(pastaCaminho)
larguraMedia, alturaMedia = mediaDasImagens(imagens)
tamanhoMedio = int(larguraMedia)
xHeat = []
yHeat = []
zHeat = []
for xIndex in range(tamanhoMedio):
    for yIndex in range(tamanhoMedio):
        xHeat.append(xIndex)
        yHeat.append(yIndex)
        zHeat.append(0)
for imagem in imagens:
    print(imagem)
    cancao = Image.open(imagem)
    largura, altura = cancao.size
    if largura > tamanhoMedio:
        media = tamanhoMedio
    else:
        media = largura
    for y in range(media):
        for x in range(media):
            if x != y:
                if cancao.getpixel((x, y)) != (0, 0, 0, 255):
                    zHeat[tamanhoMedio * x + y] += 1

BD = shelve.open(os.path.join(diretorio, "dadosPreProcessados"))
BD["x"] = xHeat
BD["y"] = yHeat
BD["z"] = zHeat
BD["maximo"] = max(zHeat)
BD.close()
