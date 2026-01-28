from PIL import Image
from userUtil import pegaInteiro
from textos import embelezeTempo
from time import time
import os
import subprocess

def funcaoAfim(inicio,fim,total,n):
    elemento = []
    for elementoInicial, elementoFinal in zip(inicio, fim):
        B = elementoInicial
        A = (elementoFinal-elementoInicial)/(total+1)
        elemento.append(int(A*n+B))
    return tuple(elemento)

nomeFrame = 'frames\\frame{0:03d}.png'
quantiaFrames = 30#pegaInteiro('quantos frames?')
imagemInicial = Image.open('inicial.png')
imagemFinal = Image.open('final.png')
nomeFile = 'partesConfig\\parte{0:02d}Config.txt'
imagemInicial.save(nomeFrame.format(0))
imagemFinal.save(nomeFrame.format(quantiaFrames+1))
print('\n tamanho: '+str(imagemInicial.size),end='\n\n')
partes = os.listdir('partesIniciais')
quantiaPartes = len(partes)
partes = None
for a in range(quantiaFrames):
    frame = Image.new("RGBA",imagemFinal.size,(255,255,255,0))
    frame.save(nomeFrame.format(a+1))
firstTime = True
for nParte in range(quantiaPartes):
    for n in range(quantiaFrames):
        if(firstTime):
            inicio = time()
        frame = Image.open(nomeFrame.format(n+1))
        file = open(nomeFile.format(nParte))
        linha = file.readline()
        while(linha):
            if(linha[0] in ['a','v']):
                linha = file.readline()
                continue
            coords = [tuple([int(b) for b in coord.split(',')]) for coord in linha.split(' ')]
            coordFinal = coords[1]
            pixelFinal = imagemFinal.getpixel(coordFinal)
            coordInicial = coords[0]
            pixelInicial = imagemInicial.getpixel(coordInicial)
            novaCoord = funcaoAfim(coordInicial,coordFinal,quantiaFrames,n+1)
            novaCor = funcaoAfim(pixelInicial,pixelFinal,quantiaFrames,n+1)
            frame.putpixel(novaCoord,novaCor)
            linha = file.readline()
        frame.save(nomeFrame.format(n+1))
        frame.close()
        if(firstTime):
            fim = time()
            duracao = fim-inicio
            print('são '+str(quantiaFrames)+' frames')
            print('uma execução demorou : '+embelezeTempo(duracao))
            print('execução Total demorará : '+embelezeTempo(duracao*quantiaFrames))
            fim,inicio,duracao,tamanhoFile = [None,None,None,None]
            firstTime = False
        file.close()
    subprocess.call ('python C:\\pythonscript\\imagem\\morphManual\\fazGif.py ')
imagemInicial.close()
imagemFinal.close()
