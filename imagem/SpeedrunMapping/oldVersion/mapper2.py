import subprocess
import numpy as np
from PIL import Image
from os import listdir
from time import time
from textos import embelezeTempo as eT

def openFrame(frame):
    return Image.open(frame).crop((42,78,1039,479))

def comparaPixel(pixelA,pixelB):
    total = 1
    for i in range(3):
        total *= 1-abs(pixelA[i]-pixelB[i])/255
    return total

def encontraIndice(aprovados,totais):
    maxValue = 0
    maxIndice = [DDP,DDP]
    for x in range(DT):
        for y in range(DT):
            value = aprovados[x][y]/totais[x][y]
            if value >= maxValue:
                maxValue = value
                maxIndice = [x,y]
    return [DDP-a for a in maxIndice]

def comparaFrames(mapa,frameB,posicao):
    inicio = time()
    tamanho = frameB.size
    aprovados = [[0 for a in range(DT)] for b in range(DT)]
    totais = [[0 for a in range(DT)] for b in range(DT)]
    for y in range(0,tamanho[1],PY):
        for x in range(0,tamanho[0],PX):
            pixelA = mapa.getpixel((posicao[0]+x,posicao[1]+y))
            if pixelA[2] == max(pixelA):
                continue
            for yAdd in range(-DDP,DDP+1):
                if y+yAdd < 0:
                    continue
                if y+yAdd >= tamanho[1]:
                    break
                for xAdd in range(-DDP,DDP+1):
                    if x+xAdd < 0:
                        continue
                    if x+xAdd >= tamanho[0]:
                        break
                    pixelB = frameB.getpixel((x+xAdd,y+yAdd))
                    if pixelB[2] != max(pixelB):
                        aprovados[xAdd+DDP][yAdd+DDP] += comparaPixel(pixelA,pixelB)
                        totais[xAdd+DDP][yAdd+DDP] += 1
    inicio = time()
    indice = encontraIndice(aprovados,totais)
    return indice

def ampliaMapa(mapa,ampliacao,posicao,adds):
    tamanhoMapa = mapa.size
    tamanhoAmpliacao = ampliacao.size
    novaPosicao = [posicao[a]+adds[a] for a in range(2)]
    if min(novaPosicao) < 0:
        novoTamanho = list(tamanhoMapa).copy()
        for a in range(2):
            if novaPosicao[a] < 0:
                novoTamanho[a] = tamanhoMapa[a] - novaPosicao[a]
            else:
                novoTamanho[a] = novaPosicao[a] + tamanhoAmpliacao[a]
        novoMapa = Image.new("RGBA",tuple(novoTamanho),(255,255,255,0))
        for a in range(2):
            if novaPosicao[a] < 0:
                novaPosicao[a] = 0
        novissimaPosicao = novaPosicao.copy()
        for a in range(2):
            if novissimaPosicao[a] > 0:
                novissimaPosicao[a] = 0
            else:
                novissimaPosicao[a] -= adds[a]
        novoMapa.paste(mapa,tuple(novissimaPosicao))
        ampliacaoTransparent = Image.new("RGBA",novoMapa.size,(255,255,255,0))
        ampliacaoTransparent.paste(ampliacao,tuple(novaPosicao))
        novoMapa = Image.alpha_composite(ampliacaoTransparent, novoMapa)
        #novoMapa.paste(ampliacao,tuple(novaPosicao))
    else:
        novoTamanho = list(tamanhoMapa).copy()
        for a in range(2):
            if novaPosicao[a] + tamanhoAmpliacao[a] > tamanhoMapa[a]:
                novoTamanho[a] = novaPosicao[a] + tamanhoAmpliacao[a]
        novoMapa = Image.new("RGBA",tuple(novoTamanho),(255,255,255,0))
        novoMapa.paste(mapa,(0,0))
        ampliacaoTransparent = Image.new("RGBA",novoMapa.size,(255,255,255,0))
        ampliacaoTransparent.paste(ampliacao,tuple(novaPosicao))
        novoMapa = Image.alpha_composite(ampliacaoTransparent, novoMapa)
        #novoMapa.paste(ampliacao,novaPosicao)
    return novoMapa,novaPosicao
            
DDP = 20 #DISTANCIADEPROCURA  maior = mais lento e melhor
DT = DDP*2+1 #DISTANCIATOTAL
PY = DT #PASSOSY             menor = mais lento e melhor, tem que ser maior que DT
PX = DT #PASSOSX             menor = mais lento e melhor, tem que ser maior que DT

#Argumentos do FFMPEG
diretorioVideo = 'C:\\pythonscript\\imagem\\SpeedrunMapping\\video'
origemVideo = '-i C:\pythonscript\\imagem\\SpeedrunMapping\\level.mp4'#'-i C:\\pythonscript\\videos\\videos\\video0002.mp4'
destinoTemp = diretorioVideo + '\\frame%04d.png'
extraArguments = '-r {0:02d}/1'
processoArgs = ['ffmpeg',origemVideo,extraArguments,destinoTemp]

fps = 30

processoArgs[2] = extraArguments.format(fps)
#subprocess.call (' '.join(processoArgs))

diretorioFrames = diretorioVideo+"\\frame{0:04d}.png"

mapa = openFrame(diretorioFrames.format(1))
tamanho = mapa.size
posicao = [0,0]
framesTotais = len(listdir(diretorioVideo))
inicio = time()
inicioTotal = time()
try:
    for n in range(90,framesTotais):
        frameAtual = openFrame(diretorioFrames.format(n))
        adds = comparaFrames(mapa,frameAtual,posicao)
        while max([abs(a) for a in adds]) == DDP:
            DDP = max([abs(a) for a in adds]) + 1
            DT = DDP*2+1
            PY = DT
            PX = DT
            adds = comparaFrames(mapa,frameAtual,posicao)
        mapa,posicao = ampliaMapa(mapa,frameAtual,posicao,adds)
        fim = time()
        duracao = fim-inicio
        inicio = time()
        print()
        print(str(n) + " : " + eT(duracao))
        print(eT(duracao*(framesTotais-n)))
        print(adds)
except:
    print(n)
    print("deu erro")
    pass
frameAtual.close()
fimTotal = time()
duracao = fimTotal-inicioTotal
print(eT(duracao))
mapa.save("mapa.png")
mapa.close()