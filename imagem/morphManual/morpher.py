from PIL import Image
from userUtil import pegaInteiro
from time import time
import os
import multiprocessing

def funcaoCor(inicio,fim,total,n):
    elemento = []
    for elementoInicial, elementoFinal in zip(inicio, fim):
        B = elementoInicial
        A = (elementoFinal-elementoInicial)/(total+1)
        elemento.append(int(A*n+B))
    return tuple(elemento)

def funcaoCoord(inicio,fim,total,n):
    elemento = []
    for elementoInicial, elementoFinal in zip(inicio, fim):
        B = elementoInicial
        A = (elementoFinal-elementoInicial)/(total+1)
        elemento.append(int(A*n+B))
    return tuple(elemento)

def makeFrame(args):
    n,total = args
    imagemInicial = Image.open('C:\\pythonscript\\imagem\\morphManual\\inicial.png')
    imagemFinal = Image.open('C:\\pythonscript\\imagem\\morphManual\\final.png')
    print("Fazendo Frame : " + str(n))
    frame = Image.new("RGBA",imagemFinal.size,(255,255,255,0))
    for fileName in os.listdir('C:\\pythonscript\\imagem\\morphManual\\partes\\config'):
        file = open('C:\\pythonscript\\imagem\\morphManual\\partes\\config\\' + fileName,'r')
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
                novaCoord = funcaoCoord(coordInicial,coordFinal,total,n+1)
                novaCor = funcaoCor(pixelInicial,pixelFinal,total,n+1)
                frame.putpixel(novaCoord,novaCor)
            linha = file.readline()
        file.close()
    print("\tFrame Terminado : " + str(n))
    frame.save(f'C:\\pythonscript\\imagem\\morphManual\\frames\\frame{n+1:03d}.png')
    imagemInicial.close()
    imagemFinal.close()
    frame.close()

if __name__ == '__main__':
    quantiaFrames = 30#pegaInteiro('quantos frames?')
    nomeFrame = 'C:\\pythonscript\\imagem\\morphManual\\frames\\frame{0:03d}.png'
    
    imagemInicial = Image.open('C:\\pythonscript\\imagem\\morphManual\\inicial.png')
    imagemFinal = Image.open('C:\\pythonscript\\imagem\\morphManual\\final.png')
    imagemInicial.save(nomeFrame.format(0))
    imagemFinal.save(nomeFrame.format(quantiaFrames+1))
    imagemInicial.close()
    imagemFinal.close()
    
    print('\n tamanho: '+str(imagemInicial.size),end='\n\n')
    p = multiprocessing.Pool(os.cpu_count())
    p.map(makeFrame,[[a,quantiaFrames] for a in range(quantiaFrames)])
