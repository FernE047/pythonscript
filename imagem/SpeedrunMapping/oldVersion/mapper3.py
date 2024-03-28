import subprocess
import numpy as np
import matplotlib.image as im
import matplotlib.pyplot as plt
from PIL import Image
from os import listdir
from time import time
from textos import embelezeTempo as eT

def openFrame(frame):
    return im.imread(frame)[42:1039,78:479,:]

def comparaPixel(pixelA,pixelB):
    total = 1
    for i in range(3):
        total *= 1-abs(pixelA[i]-pixelB[i])/255
    return total

def comparaFrames(mapa,frameB,posicao):
    inicio = time()
    tamanho = frameB.shape
    aprovados = np.zeros(DT,DT)
    totais = np.zeros(DT,DT)
    for y in range(0,tamanho[1],DT):#PY):
        for x in range(0,tamanho[0],DT):#PX):
            pixelA = mapa[posicao[0]+x,posicao[1]+y]
            if pixelA[2] == max(pixelA):
                continue
            for yAdd in range(-DDP,DDP+1):
                for xAdd in range(-DDP,DDP+1):
                    if x+xAdd < 0:
                        continue
                    if x+xAdd >= tamanho[0]:
                        break
                    if y+yAdd < 0:
                        continue
                    if y+yAdd >= tamanho[1]:
                        break
                    pixelB = frameB[x+xAdd,y+yAdd]
                    if pixelB[2] == max(pixelB):
                        continue
                    aprovados[xAdd+DDP][yAdd+DDP] += comparaPixel(pixelA,pixelB)
                    totais[xAdd+DDP][yAdd+DDP] += 1
                if y+yAdd >= tamanho[1]:
                    break
    fim = time()
    probabilidades = [[aprovados[x][y]/totais[x][y] for y in range(DT)] for x in range(DT)]
    firstIndice = [max(probabilidades[x]) for x in range(DT)]
    maximo = max(firstIndice)
    teste = sum([probabilidades[x].count(maximo) for x in range(DT)])
    if teste >= 2:
        print("aconteceu" + str(teste))
    indiceX = firstIndice.index(maximo)
    yAdd = probabilidades[indiceX].index(maximo)-DDP
    xAdd = indiceX - DDP
    duracao = fim-inicio
    print(str(posicao) + " : " + eT(duracao))
    return [-xAdd,-yAdd]

def ampliaMapa(mapa,ampliacao,posicao,adds):
    tamanhoMapa = mapa.shape[:-1]
    tamanhoAmpliacao = ampliacao.shape[:-1]
    novaPosicao = [posicao[a]+adds[a] for a in range(2)]
    if min(novaPosicao) < 0:
        novoTamanho = np.copy(tamanhoMapa)
        for a in range(2):
            if novaPosicao[a] < 0:
                novoTamanho[a] = tamanhoMapa[a] - novaPosicao[a]
            else:
                novoTamanho[a] = novaPosicao[a] + tamanhoAmpliacao[a]
        novoMapa = np.zeros(novoTamanho)
        for a in range(2):
            if novaPosicao[a] < 0:
                novaPosicao[a] = 0
        novissimaPosicao = np.copy(novaPosicao)
        for a in range(2):
            if novissimaPosicao[a] > 0:
                novissimaPosicao[a] = 0
            else:
                novissimaPosicao[a] -= adds[a]
        novoMapa = np.insert(novoMapa,novissimaPosicao,mapa)
        novoMapa = np.insert(novoMapa,novaPosicao,ampliacao)
    else:
        novoTamanho = np.copy(tamanhoMapa)
        for a in range(2):
            if novaPosicao[a] + tamanhoAmpliacao[a] > tamanhoMapa[a]:
                novoTamanho[a] = novaPosicao[a] + tamanhoAmpliacao[a]
        novoMapa = np.zeros(novoTamanho)
        novoMapa = np.insert(novoMapa,(0,0),mapa)
        novoMapa = np.insert(novoMapa,novaPosicao,ampliacao)
    return novoMapa,novaPosicao
            
DDP = 20 #DISTANCIADEPROCURA  maior = mais lento e melhor
DT = DDP*2+1 #DISTANCIATOTAL
#PY = DT #PASSOSY             menor = mais lento e melhor
#PX = DT #PASSOSX             menor = mais lento e melhor

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
tamanho = mapa.shape[:-1]
posicao = [0,0]
framesTotais = len(listdir(diretorioVideo))
inicio = time()
inicioTotal = time()
for n in range(90,framesTotais):
    frameAtual = openFrame(diretorioFrames.format(n))
    adds = comparaFrames(mapa,frameAtual,posicao)
    while max([abs(a) for a in adds]) == DDP:
        DDP = max([abs(a) for a in adds]) + 1
        DT = DDP*2+1
        adds = comparaFrames(mapa,frameAtual,posicao)
    mapa,posicao = ampliaMapa(mapa,frameAtual,posicao,adds)
    '''fim = time()
    duracao = fim-inicio
    inicio = time()
    print()
    print(str(n) + " : " + eT(duracao))
    print(eT(duracao*(framesTotais-n)))
    print(adds)'''
    mapa.savefig("mapa.png")
#except:
#    print("deu erro")
#    pass
fimTotal = time()
duracao = fimTotal-inicioTotal
print(eT(duracao))
mapa.savefig("mapa.png")
