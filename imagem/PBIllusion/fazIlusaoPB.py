from PIL import Image
import pastaImagens
import os

casos=[3,4,5]
divisor=50
assunto="DsRom"
imagens=pastaImagens.pegaAssunto(assunto)
for numero,imgName in enumerate(imagens):
    print(imgName)
    imagem=Image.open(imgName)
    tamanho=imagem.size
    for x in range(tamanho[0]):
        for y in range(tamanho[1]):
            if((x%divisor not in casos)and(y%divisor not in casos)):
                cor=imagem.getpixel((x,y))
                cor=tuple(3*[int((cor[0]+cor[1]+cor[2])/3)]+[255])
                imagem.putpixel((x,y),cor)
    pastaImagens.salva('{0:03d}-'.format(numero)+assunto,imagem,pasta=["Pbillusion",assunto],extensao=".png")
    print('{0:03d}-'.format(numero)+assunto+" imagem concluida")
