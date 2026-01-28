from PIL import Image
from userUtil import pegaImagem


def multiplica(numero1, numero2):
    a, b = numero1
    c, d = numero2
    numero3 = [(a * c - b * d), (a * d + c * b)]
    return numero3


def itera(numero, it):
    original = numero
    for i in range(it - 1):
        numero = multiplica(numero, original)
    return numero


def caixa(img):
    pass


imagem = Image.new("RGBA", (5, 5), (0, 0, 0, 255))  # pegaImagem()
larg, alt = imagem.size
altMin, altMax, largMin, largMax = 4 * [0]
o = 3
for xIm in range(larg):
    for yIm in range(alt):
        pixelComplex = [(larg - 1) / 2 - xIm, (alt - 1) / 2 - yIm]
        pixelComplex = itera(pixelComplex, o)
        if pixelComplex[0] > largMax:
            largMax = pixelComplex[0]
        if pixelComplex[0] < largMin:
            largMin = pixelComplex[0]
        if pixelComplex[1] > altMax:
            altMax = pixelComplex[1]
        if pixelComplex[1] < altMin:
            altMin = pixelComplex[1]
altura = int(altMax - altMin + 1)
largura = int(largMax - largMin + 1)
imagemComplexa = Image.new("RGBA", (largura, altura), (255, 255, 255, 255))
for xIm in range(larg):
    for yIm in range(alt):
        corIm = imagem.getpixel((xIm, yIm))
        pixelComplex = [(alt - 1) / 2 - xIm, (alt - 1) / 2 - yIm]
        pixelComplex = itera(pixelComplex, o)
        x = int((largura - 1) / 2 - pixelComplex[0])
        y = int((altura - 1) / 2 - pixelComplex[1])
        pixelIm = (x, y)
        imagemComplexa.putpixel(pixelIm, corIm)
imagemComplexa.save("output.png")
