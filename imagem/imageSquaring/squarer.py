from PIL import Image
import os

def detectCorners(imagem):
    largura,altura = imagem.size
    xMenor = largura
    xMaior = 0
    yMenor = altura
    yMaior = 0
    for x in range(largura):
        for y in range(altura):
            pixel = imagem.getpixel(x,y)
            if pixel[3] == 255 :
                if x<xMenor:
                    xMenor = x
                if y<yMenor:
                    yMenor = y
                if x>xMaior:
                    xMaior = x
                if y>yMaior:
                    yMaior = y
    return(xMenor,xMaior,yMenor,yMaior)
                
                

nome = 'C:\\pythonscript\\Imagens\\PokedexSemFundo\\pokemon{0:03d}.png'
for a in range(762):
    print(nome.format(a))
    imagem = Image.open(nome.format(a))
    largura,altura = imagem
    xMenor,xMaior,yMenor,yMaior = detectCorners(imagem)
    tamanhoX = xMaior-xMenor+1
    tamanhoY = yMaior-yMenor+1
    if tamanhoX>tamanhoY:
        tamanhoMaximo = tamanhoX
    else:
        tamanhoMaximo = tamanhoY
    for t in range(tamanhoMaximo):
        for x in range(xMenor,xMaior+1):
            for y in range(yMenor,yMaior+1):
                if y+tamanhoY
