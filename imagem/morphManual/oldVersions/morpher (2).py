from PIL import Image
from userUtil import pegaInteiro
from textos import embelezeTempo
from time import time
from os import cpu_count
import multiprocessing

def funcaoAfim(inicio,fim,total,n):
    elemento = []
    for elementoInicial, elementoFinal in zip(inicio, fim):
        B = elementoInicial
        A = (elementoFinal-elementoInicial)/(total+1)
        elemento.append(int(A*n+B))
    return tuple(elemento)

def makeFrame(n):
    imagemInicial = Image.open('C:\\pythonscript\\imagem\\morphManual\\inicial.png')
    imagemFinal = Image.open('C:\\pythonscript\\imagem\\morphManual\\final.png')
    print(n)
    frame = Image.new("RGBA",imagemFinal.size,(255,255,255,0))
    file = open('C:\\pythonscript\\imagem\\morphManual\\config.txt')
    linha = file.readline()
    while(linha):
        if(linha.find('fundo')!=-1):
            coord = tuple([int(b) for b in linha[:-6].split(',')])
            frame.putpixel(coord,imagemInicial.getpixel(coord))
        else:
            coords = [tuple([int(b) for b in coord.split(',')]) for coord in linha.split(' ')]
            coordFinal = coords[1]
            pixelFinal = imagemFinal.getpixel(coordFinal)
            coordInicial = coords[0]
            pixelInicial = imagemInicial.getpixel(coordInicial)
            novaCoord = funcaoAfim(coordInicial,coordFinal,30,n+1)
            novaCor = funcaoAfim(pixelInicial,pixelFinal,30,n+1)
            frame.putpixel(novaCoord,novaCor)
        linha = file.readline()
    frame.save('C:\\pythonscript\\imagem\\morphManual\\frames\\frame{0:03d}.png'.format(n+1))
    imagemInicial.close()
    imagemFinal.close()
    frame.close()
    file.close()

if __name__ == '__main__':
    nomeFrame = 'C:\\pythonscript\\imagem\\morphManual\\frames\\frame{0:03d}.png'
    quantiaFrames = 30#pegaInteiro('quantos frames?')
    imagemInicial = Image.open('C:\\pythonscript\\imagem\\morphManual\\inicial.png')
    imagemFinal = Image.open('C:\\pythonscript\\imagem\\morphManual\\final.png')
    imagemInicial.save(nomeFrame.format(0))
    imagemFinal.save(nomeFrame.format(quantiaFrames+1))
    print('\n tamanho: '+str(imagemInicial.size),end='\n\n')
    p = multiprocessing.Pool(cpu_count())
    p.map(makeFrame,range(quantiaFrames))
