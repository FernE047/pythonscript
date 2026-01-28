import os
from PIL import Image
import multiprocessing

def coordDirecao(coord,n):
    if(n>7):
        n = n%8
    x,y = coord
    if n == 0:
        return(x+1,y+1)
    if n == 1:
        return(x,y+1)
    if n == 2:
        return(x-1,y+1)
    if n == 3:
        return(x+1,y)
    if n == 4:
        return(x-1,y)
    if n == 5:
        return(x+1,y-1)
    if n == 6:
        return(x,y-1)
    if n == 7:
        return(x-1,y-1)
    return (x,y)

def passaCorrigindo(xBegin,xEnd,yBegin,yEnd,imagem):
    if(xBegin>xEnd):
        xAdd = -1
    else:
        xAdd = 1
    if(yBegin>yEnd):
        yAdd = -1
    else:
        yAdd = 1
    alteracoes = 1
    while alteracoes != 0:
        alteracoes = 0
        for x in range(xBegin,xEnd,xAdd): 
            for y in range(yBegin,yEnd,yAdd):
                pixelAtual = imagem.getpixel((x,y))
                if(pixelAtual[3]==0):
                    lista = []
                    for direcao in range(8):
                        try:
                            pixelDir = imagem.getpixel(coordDirecao((x,y),direcao))
                            if(pixelDir[3]!=0):
                                lista.append(pixelDir)
                        except:
                            pass
                        if(lista):
                            alteracoes += 1
                            imagem.putpixel((x,y),pixelMedio(lista))
    
def superCorrigeFrame(nome):
    imagem = Image.open(nome)
    largura,altura = imagem.size
    passaCorrigindo(0,int(largura/2+1),0,altura,imagem)
    passaCorrigindo(largura-1,int(largura/2-1),0,altura,imagem)
    imagem.save(nome)
    imagem.close()

def corrigeAlguns(coords,imagem):
    excluidos = [0]
    while len(excluidos) != 0:
        excluidos = []
        for n,coord in enumerate(coords):
            lista = []
            for direcao in [1,3,4,6]:
                pixelAtual = imagem.getpixel(coordDirecao(coord,direcao))
                if(pixelAtual[3]!=0):
                    lista.append(pixelAtual)
            if(len(lista)>=3):
                excluidos.append(n)
                imagem.putpixel(coord,pixelMedio(lista))
        for n in reversed(excluidos):
            coords.pop(n)

def pixelMedio(lista):
    novoPixel = [0 for _ in lista[0]]
    for pixel in lista:
        for n,cor in enumerate(pixel):
            novoPixel[n] += cor
    novoPixel = tuple([int(cor/len(lista)) for cor in novoPixel])
    return novoPixel

def corrigeFrame(nome):
    print(nome)
    imagem = Image.open(nome)
    largura,altura = imagem.size
    verificaDepois = []
    for y in range(1,altura-1):
        possoEncontrar = False
        for x in range(1,largura-1):
            pixel = imagem.getpixel((x,y))
            if(pixel[3]==0):
                if(possoEncontrar):
                    lista = []
                    for direcao in [3,4]:
                        pixelAtual = imagem.getpixel(coordDirecao((x,y),direcao))
                        if(pixelAtual[3]!=0):
                            lista.append(pixelAtual)
                    if(len(lista)==2):
                        imagem.putpixel((x,y),pixelMedio(lista))
                        continue
                    for direcao in [1,6]:
                        pixelAtual = imagem.getpixel(coordDirecao((x,y),direcao))
                        if(pixelAtual[3]!=0):
                            lista.append(pixelAtual)
                    if(len(lista)>=3):
                        imagem.putpixel((x,y),pixelMedio(lista))
                    else:
                        verificaDepois.append((x,y))
            else:
                possoEncontrar = True
        if(possoEncontrar):
            for x in range(largura-2,0,-1):
                if(pixel[3]==0):
                    if((x,y) in verificaDepois):
                        verificaDepois.pop(verificaDepois.index((x,y)))
                else:
                    break
    corrigeAlguns(verificaDepois,imagem)
    for x in range(1,largura-1):
        possoEncontrar = False
        for y in range(1,altura-1):
            pixel = imagem.getpixel((x,y))
            if(pixel[3]==0):
                if(possoEncontrar):
                    lista = []
                    for direcao in [1,6]:
                        pixelAtual = imagem.getpixel(coordDirecao((x,y),direcao))
                        if(pixelAtual[3]!=0):
                            lista.append(pixelAtual)
                    if(len(lista)==2):
                        imagem.putpixel((x,y),pixelMedio(lista))
                        continue
                    for direcao in [3,4]:
                        pixelAtual = imagem.getpixel(coordDirecao((x,y),direcao))
                        if(pixelAtual[3]!=0):
                            lista.append(pixelAtual)
                    if(len(lista)>=3):
                        imagem.putpixel((x,y),pixelMedio(lista))
                    else:
                        verificaDepois.append((x,y))
            else:
                possoEncontrar = True
        if(possoEncontrar):
            for y in range(altura-2,0,-1):
                if(pixel[3]==0):
                    if((x,y) in verificaDepois):
                        verificaDepois.pop(verificaDepois.index((x,y)))
                else:
                    break
    corrigeAlguns(verificaDepois,imagem)
    imagem.save(nome)
    imagem.close()

if __name__ == "__main__":
    frames = ["C:\\pythonscript\\imagem\\morphManual\\frames\\"+a for a in os.listdir("C:\\pythonscript\\imagem\\morphManual\\frames")]
    frames.pop(0)
    frames.pop(-1)
    p = multiprocessing.Pool(os.cpu_count())
    p.map(corrigeFrame,frames)
