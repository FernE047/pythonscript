from PIL import Image, ImageDraw
import os
import pastaImagens

imagem = pastaImagens.pegaAssunto("claudia raia", 1)
imagemOriginal = Image.open(imagem[0])
largura, altura = imagemOriginal.size
larguraNova = largura + 2
alturaNova = altura + 2
imagemLinha = Image.new("RGBA", (larguraNova, alturaNova), (0, 0, 0, 0))
imagemLinha.paste(imagemOriginal, (1, 1))
pregos = []
for x in range(larguraNova):
    pregos.append((x, 0))
    pregos.append((x, alturaNova - 1))
for y in range(1, alturaNova - 1):
    pregos.append((0, y))
    pregos.append((larguraNova - 1, y))
imagemFinal = Image.new("RGBA", (larguraNova, alturaNova), (0, 0, 0, 0))
drawLinha = ImageDraw.Draw(imagemLinha)
drawFinal = ImageDraw.Draw(imagemFinal)
pregoAtual = pregos[0]
while True:
    maiorPrego = pregos[0]
    maiorValor = 0
    for prego in pregos:
        imagemAnalise = imagemLinha.copy()
        drawAnalise = ImageDraw.Draw(imagemLinha)
        drawAnalise.line(pregoAtual + prego, fill=(0, 0, 0, 255), width=1)
        totalValor = 0
        totalLinha = 0
        for x in range(larguraNova):
            for y in range(alturaNova):
                if imagemAnalise.getpixel((x, y)) == (0, 0, 0, 255):
                    pixel = imagemLinha.getpixel((x, y))
                    valor = 0
                    valor += pixel[0]
                    valor += pixel[1]
                    valor += pixel[2]
                    totalValor += valor / (3 * 255)
                    totalLinha += 1
        if (totalValor / totalLinha) >= maiorValor:
            maiorValor = totalValor / totalLinha
            maiorPrego = prego
    if maiorValor != 0:
        drawLinha.line(pregoAtual + maiorPrego, fill=(0, 0, 0, 0), width=1)
        drawFinal.line(pregoAtual + maiorPrego, fill=(0, 0, 0, 255), width=1)
        pregoAtual = maiorPrego
    else:
        break
imagemFinal.save(os.getcwd() + "lines.png")
