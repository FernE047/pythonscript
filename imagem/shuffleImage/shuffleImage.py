from PIL import Image
from userUtil import pegaImagem as pI
from random import randint
from time import time
from textos import embelezeTempo as eT

import shelve

def procuraBranco(imagem,quantia):
    largura,altura = imagem.size
    total=0
    for x in range(largura):
        for y in range(altura):
            coord=(x,y)
            pixel = imagem.getpixel(coord)
            if(pixel == (255,255,255,255)):
                total+=1
            if(total == quantia):
                return(coord)
    return(coord)

def randomTotal(imagem):
    largura,altura = imagem.size
    shuffledImage = Image.new('RGBA',(largura,altura),(255,255,255,255))
    for x in range(largura):
        for y in range(altura):
            coord=(x,y)
            pixelOriginal = imagem.getpixel(coord)
            newX = randint(0,largura-1)
            newY = randint(0,altura-1)
            newCoord = (newX,newY)
            pixel = shuffledImage.getpixel(newCoord)
            while(pixel != (255,255,255,255)):
                newX = randint(0,largura-1)
                newY = randint(0,altura-1)
                newCoord = (newX,newY)
                pixel = shuffledImage.getpixel(newCoord)
            newCoord = (newX,newY)
            shuffledImage.putpixel(newCoord,pixelOriginal)
    return shuffledImage

def brancosTotal(imagem):
    largura,altura = imagem.size
    totalBranco = largura*altura
    shuffledImage = Image.new('RGBA',(largura,altura),(255,255,255,255))
    for x in range(largura):
        for y in range(altura):
            coord=(x,y)
            pixelOriginal = imagem.getpixel(coord)
            posicao = randint(1,totalBranco)
            newCoord = procuraBranco(shuffledImage,posicao)
            totalBranco-=1
            shuffledImage.putpixel(newCoord,pixelOriginal)
    return shuffledImage

def meioAMeio(imagem,porcentagemRandom):
    largura,altura = imagem.size
    total = largura*altura
    totalRandom = 0
    totalBranco = total
    porcentagem = totalRandom/total
    shuffledImage = Image.new('RGBA',(largura,altura),(255,255,255,255))
    for x in range(largura):
        for y in range(altura):
            coord=(x,y)
            pixelOriginal = imagem.getpixel(coord)
            if(porcentagem<porcentagemRandom):
                newX = randint(0,largura-1)
                newY = randint(0,altura-1)
                newCoord = (newX,newY)
                pixel = shuffledImage.getpixel(newCoord)
                while(pixel != (255,255,255,255)):
                    newX = randint(0,largura-1)
                    newY = randint(0,altura-1)
                    newCoord = (newX,newY)
                    pixel = shuffledImage.getpixel(newCoord)
                newCoord = (newX,newY)
                totalRandom += 1
                totalBranco -= 1
                porcentagem = totalRandom/total
            else:
                posicao = randint(1,totalBranco)
                newCoord = procuraBranco(shuffledImage,posicao)
                totalBranco -= 1
            shuffledImage.putpixel(newCoord,pixelOriginal)
    return shuffledImage

imagem=pI(infoAdicional=1)
tempos=[]
for porc in range(100,-1,-1):
    BD=shelve.open('BDRandom')
    inicio=time()
    shuffledImage=meioAMeio(imagem,porc)
    fim=time()
    tempo=fim-inicio
    print("porcentagem de aleatoridade:{}%\n{}\n".format(porc,eT(tempo)))
    shuffledImage.save("output{:03d}.png".format(porc))
    tempos.append(tempo)
    BD["tempos{:03d}".format(porc)]=tempos
    BD.close()
temposOrdenados=sorted(tempos)
print("Resultados : ")
for tempo in temposOrdenados:
    print("{}% : {}".format(tempos.index(tempo),tempo))
