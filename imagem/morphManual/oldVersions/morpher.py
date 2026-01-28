from PIL import Image
from userUtil import pegaInteiro
from time import time

def funcaoAfim(inicio,fim,total,n):
    elemento = []
    for elementoInicial, elementoFinal in zip(inicio, fim):
        B = elementoInicial
        A = (elementoFinal-elementoInicial)/(total+1)
        elemento.append(int(A*n+B))
    return tuple(elemento)

nomeFrame = 'frames\\frame{0:03d}.png'
quantiaFrames = 3#pegaInteiro('quantos frames?')
imagemInicial = Image.open('inicial.png')
imagemFinal = Image.open('final.png')
imagemInicial.save(nomeFrame.format(0))
imagemFinal.save(nomeFrame.format(quantiaFrames+1))
print('\n tamanho: '+str(imagemInicial.size),end='\n\n')
for n in range(quantiaFrames):
    print(n)
    frame = Image.new("RGBA",imagemFinal.size,(255,255,255,0))
    file = open('config.txt')
    linha = file.readline()
    while(linha):
        if(linha.find('fundo')!=-1):
            pass
            #coord = tuple([int(b) for b in linha[:-6].split(',')])
            #frame.putpixel(coord,imagemInicial.getpixel(coord))
        else:
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
    file.close()
imagemInicial.close()
imagemFinal.close()
