from PIL import Image
import os

os.chdir("faixas")
for nome in range(1, 11):
    anyIm = Image.open("a" + str(nome) + ".jpg")
    width, height = anyIm.size
    faixa = ["", "", ""]
    faixa[0] = Image.new("RGB", (width, height), "white")
    faixa[1] = Image.new("RGB", (width, height), "white")
    faixa[2] = Image.new("RGB", (width, height), "white")
    for x in range(width):
        for y in range(height):
            pixelOrigem = anyIm.getpixel((x, y))
            pixelVermelho = tuple([255] + [pixelOrigem[0], pixelOrigem[0]])
            pixelVerde = tuple([pixelOrigem[1]] + [255] + [pixelOrigem[1]])
            pixelAzul = tuple([pixelOrigem[2], pixelOrigem[2]] + [255])
            faixa[0].putpixel((x, y), pixelVermelho)
            faixa[1].putpixel((x, y), pixelVerde)
            faixa[2].putpixel((x, y), pixelAzul)
    faixa[0].save("b" + str(nome) + "-red.jpg")
    faixa[1].save("b" + str(nome) + "-green.jpg")
    faixa[2].save("b" + str(nome) + "-azul.jpg")
    print(nome)
