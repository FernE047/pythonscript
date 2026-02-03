from PIL import Image
import os
import math
import numpy


def coordenadasPregos(quantia, img):
    largura, altura = img.size
    hip = int(math.sqrt((largura / 2) ** 2 + (altura / 2) ** 2)) + 1
    print(hip)
    pregosAngulo = 360 / quantia
    pregos = []
    for angulo in numpy.arange(0, 360, pregosAngulo):
        radiano = angulo * math.pi / 180
        pregos.append(
            (int(hip * math.cos(radiano)) + hip, int(hip * math.sin(radiano) + hip))
        )
    return pregos


def dimensoesPorPregos(pregos):
    maiorX = 0
    maiorY = 0
    for prego in pregos:
        if prego[0] >= maiorX:
            maiorX = prego[0]
        if prego[1] >= maiorY:
            maiorY = prego[1]
    tamanho = (maiorX + 2, maiorY + 2)
    return tamanho


def ehMaior(pregoProximo, pregoAtual, menorValor, imagemPregos):
    menorValorOriginal = menorValor
    imagemAnalise = imagemPregos.copy()
    totalValor = 0
    totalLinha = 0
    """print(pregoAtual)
    print(pregoProximo)"""
    if pregoAtual == pregoProximo:
        return (menorValor, False)
    if pregoAtual[0] != pregoProximo[0]:
        auxA = (pregoAtual[1] - pregoProximo[1]) / (pregoAtual[0] - pregoProximo[0])
        auxB = pregoProximo[1] - pregoProximo[0] * auxA
        """print(auxA)
        print(auxB)"""
    else:
        auxA = 2
    if (auxA <= 1) and (auxA >= -1):
        if pregoAtual[0] > pregoProximo[0]:
            flow = -1
        else:
            flow = 1
        for x in range(pregoAtual[0], pregoProximo[0], flow):
            pixel = imagemPregos.getpixel((x, int(auxA * x + auxB)))
            if pixel[3] == 255:
                valor = 0
                valor += pixel[0]
                valor += pixel[1]
                valor += pixel[2]
                totalValor += valor / (3 * 255)
                totalLinha += 1
        if totalLinha == 0:
            totalLinha = 1
        if (totalValor / totalLinha) <= menorValor:
            menorValor = totalValor / totalLinha
    else:
        auxA = (pregoAtual[0] - pregoProximo[0]) / (pregoAtual[1] - pregoProximo[1])
        auxB = pregoProximo[0] - pregoProximo[1] * auxA
        """print(auxA)
        print(auxB)"""
        if pregoAtual[1] > pregoProximo[1]:
            flow = -1
        else:
            flow = 1
        for y in range(pregoAtual[1], pregoProximo[1], flow):
            pixel = imagemPregos.getpixel((int(auxA * y + auxB), y))
            if pixel[3] == 255:
                valor = 0
                valor += pixel[0]
                valor += pixel[1]
                valor += pixel[2]
                totalValor += valor / (3 * 255)
                totalLinha += 1
        if totalLinha == 0:
            totalLinha = 1
        if (totalValor / totalLinha) <= menorValor:
            menorValor = totalValor / totalLinha
    """print(menorValor)"""
    return (menorValor, (menorValor != menorValorOriginal))


def fazLinha(pontoInicial, pontoFinal, imagem, cor):
    if pontoInicial[0] != pontoFinal[0]:
        auxA = (pontoInicial[1] - pontoFinal[1]) / (pontoInicial[0] - pontoFinal[0])
        auxB = pontoFinal[1] - pontoFinal[0] * auxA
    else:
        auxA = 2
    if (auxA <= 1) and (auxA >= -1):
        if pontoInicial[0] > pontoFinal[0]:
            flow = -1
        else:
            flow = 1
        for x in range(pontoInicial[0], pontoFinal[0], flow):
            imagem.putpixel((x, int(auxA * x + auxB)), cor)
    else:
        auxA = (pontoInicial[0] - pontoFinal[0]) / (pontoInicial[1] - pontoFinal[1])
        auxB = pontoFinal[0] - pontoFinal[1] * auxA
        if pontoInicial[1] > pontoFinal[1]:
            flow = -1
        else:
            flow = 1
        for y in range(pontoInicial[1], pontoFinal[1], flow):
            imagem.putpixel((int(auxA * y + auxB), y), cor)
    return imagem



def main() -> None:
    quantiaPregos = 400
    imagemPasta = os.path.join("C:\\", "pythonscript", "lineImage", "imagens")
    imagens = [os.path.join(imagemPasta, imagem) for imagem in os.listdir(imagemPasta)]
    imagem = Image.open(imagens[5])
    pregos = coordenadasPregos(quantiaPregos, imagem)
    largura, altura = imagem.size
    larguraFinal, alturaFinal = dimensoesPorPregos(pregos)
    imagemFinal = Image.new("RGBA", (larguraFinal, alturaFinal), (255, 255, 255, 255))
    imagemPregos = imagemFinal.copy()
    offset = ((larguraFinal - largura) // 2, (alturaFinal - altura) // 2)
    imagemPregos.paste(imagem, offset)
    pregoAtual = pregos[0]
    imagemExemplo = imagemPregos.copy()
    for prego in pregos:
        imagemExemplo.putpixel(prego, (255, 0, 0, 255))
    imagemExemplo.save(os.path.join(imagemPasta, "valCroche400Exemplo.png"))
    while True:
        menorPrego = pregos[0]
        menorValor = 1
        for prego in pregos:
            menorValor, alterou = ehMaior(prego, pregoAtual, menorValor, imagemPregos)
            if alterou:
                menorPrego = prego
        if menorValor != 1:
            print(
                "do prego "
                + str(pregos.index(pregoAtual))
                + " para o prego "
                + str(pregos.index(menorPrego))
            )
            imagemPregos = fazLinha(
                pregoAtual, menorPrego, imagemPregos, (255, 255, 255, 255)
            )
            imagemFinal = fazLinha(pregoAtual, menorPrego, imagemFinal, (0, 0, 0, 255))
            """
            if(indice==quantiaPregos-1):
                indice=0
            else:
                indice+=1"""
            pregoAtual = menorPrego
        else:
            break
        try:
            imagemFinal.save(os.path.join(imagemPasta, "valCroche400Pregos.png"))
        except:
            imagemFinal.save(os.path.join(imagemPasta, "valCroche400PregosToSee.png"))
    imagemFinal.save(os.path.join(imagemPasta, "valCroche400Pregos.png"))


if __name__ == "__main__":
    main()