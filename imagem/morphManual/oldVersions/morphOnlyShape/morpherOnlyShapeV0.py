from PIL import Image
from userUtil import pegaInteiro
from textos import embelezeTempo
from time import time

def funcaoAfim(inicio,fim,total,n):
    elemento = []
    for elementoInicial, elementoFinal in zip(inicio, fim):
        B = elementoInicial
        A = (elementoFinal-elementoInicial)/(total+1)
        elemento.append(int(A*n+B))
    return tuple(elemento)

imagemInicial = Image.open('C:\\pythonscript\\imagem\\morphOnlyShape\\inicial.png')
imagemFinal = Image.new('RGBA',imagemInicial.size,(0,0,0,0))
file = open('C:\\pythonscript\\imagem\\morphOnlyShape\\config.txt')
linha = file.readline()
while(linha):
    coords = [tuple([int(b) for b in coord.split(',')]) for coord in linha.split(' ')]
    coordInicial = coords[0]
    coordFinal = coords[1]
    cor = imagemInicial.getpixel(coordInicial)
    imagemFinal.putpixel(coordFinal,cor)
    linha = file.readline()
imagemFinal.save('C:\\pythonscript\\imagem\\morphOnlyShape\\final.png')
file.close()
imagemInicial.close()
imagemFinal.close()
