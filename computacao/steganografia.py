import os
from PIL import Image
import copy


def tamanhoUsavel(img):
    largura, altura = img.size
    if largura % 2 == 1:
        largura -= 1
    if altura % 2 == 1:
        altura -= 1
    return (largura, altura)


def possivelEsconder(imgEsconde, imgOriginal):
    larguraO, alturaO = tamanhoUsavel(imgOriginal)
    larguraE, alturaE = imgEsconde.size
    if (alturaE <= alturaO / 2) and (larguraE <= larguraO / 2):
        return True
    else:
        print("imagem muito grande")
        return False


def abreImagem(mensagem):
    global nomeApaga
    imagem = False
    while not (imagem):
        try:
            print(mensagem)
            nomeApaga = input()
            if nomeApaga.find("\\") == -1:
                imagem = Image.open(os.path.join(diretorio, nomeApaga))
            else:
                imagem = Image.open(nomeApaga)
        except:
            imagem = False
            print("nome invalido")
    return imagem


def viraDec(binario):
    if binario == "00":
        return 0
    elif binario == "01":
        return 1
    elif binario == "10":
        return 2
    else:
        return 3


def esconde(imgE, imgO):
    imgS = copy.deepcopy(imgO)
    largO, altO = tamanhoUsavel(imgO)
    largE, altE = imgE.size
    for y in range(altE):
        for x in range(largE):
            pixel = imgE.getpixel((x, y))
            pixelE = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
            for a in range(3):
                for b in range(4):
                    c = bin(pixel[a])
                    d = c[2:]
                    e = str(d)
                    f = int(e)
                    g = f"{f:08d}"
                    h = g[2 * b : 2 * b + 2]
                    pixelE[a][b] = h
            posicoes = (
                (2 * x, 2 * y),
                (2 * x + 1, 2 * y),
                (2 * x, 2 * y + 1),
                (2 * x + 1, 2 * y + 1),
            )
            pixelO = [imgO.getpixel(coord) for coord in posicoes]
            pixelS = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
            for a in range(3):
                for b in range(4):
                    pixelS[b][a] = (
                        pixelO[b][a] - (pixelO[b][a] % 4) + viraDec(pixelE[a][b])
                    )
            for indice in range(4):
                imgS.putpixel(posicoes[indice], tuple(pixelS[indice]))
        print(y)
    return imgS



def main() -> None:
    nomeApaga = ""
    diretorio = os.path.join("C:\\", "pythonscript", "Imagens")
    imagemOriginal = abreImagem("digite o nome da imagem original")
    nome = nomeApaga
    imagemEscondida = abreImagem("digite o nome da imagem para esconder")
    while not (possivelEsconder(imagemEscondida, imagemOriginal)):
        imagemEscondida = abreImagem("digite o nome da imagem para esconder")
    imagemSteg = esconde(imagemEscondida, imagemOriginal)
    print(os.path.join(diretorio, "steganografada", nome[:-4] + "Steg.jpg"))
    imagemSteg.save(os.path.join(diretorio, "steganografada", nome[:-4] + "Steg.jpg"))


if __name__ == "__main__":
    main()