from PIL import Image
from userUtil import pegaInteiro
import imageio
from textos import embelezeTempo
from time import time

def funcaoAfim(inicio,fim,total,n):
    elemento = []
    for elementoInicial, elementoFinal in zip(inicio, fim):
        B = elementoInicial
        A = (elementoFinal-elementoInicial)/(total+1)
        elemento.append(int(A*n+B))
    return tuple(elemento)

def verificaTamanho():
    file = open('config.txt')
    linha = file.readline()
    quantia = 0
    while(linha):
        quantia+=1
        linha = file.readline()
    file.close()
    return quantia

nomeFrame = 'pokemon002{0:02d}.png'
quantiaFrames = 30#pegaInteiro('quantos frames?')
imagemInicial = Image.open('pokemon000.png')
imagemFinal = Image.open('pokemon001.png')
nomeFile = 'partesConfig\\parte{0:02d}Config.txt'
imagemInicial.save(nomeFrame.format(0))
imagemFinal.save(nomeFrame.format(quantiaFrames+1))
print('\n tamanho: '+str(imagemInicial.size),end='\n\n')
for a in range(quantiaFrames):
    frame = Image.new("RGBA",imagemFinal.size,(255,255,255,0))
    frame.save(nomeFrame.format(a+1))
altura,largura = imagemFinal.size
tamanhoFile = verificaTamanho()
file = open('config.txt')
linha = file.readline()
firstTime = True
inicioDef = time()
while(linha):
    if(firstTime):
        inicio = time()
    coords = [tuple([int(b) for b in coord.split(',')]) for coord in linha.split(' ')]
    coordFinal = coords[1]
    pixelFinal = imagemFinal.getpixel(coordFinal)
    coordInicial = coords[0]
    pixelInicial = imagemInicial.getpixel(coordInicial)
    for n in range(quantiaFrames):
        frame = Image.open(nomeFrame.format(n+1))
        novaCoord = funcaoAfim(coordInicial,coordFinal,quantiaFrames,n+1)
        novaCor = funcaoAfim(pixelInicial,pixelFinal,quantiaFrames,n+1)
        frame.putpixel(novaCoord,novaCor)
        frame.save(nomeFrame.format(n+1))
        frame.close()
    linha = file.readline()
    if(firstTime):
        fim = time()
        duracao = fim-inicio
        print('são '+str(tamanhoFile)+' transformações')
        print('uma execução demorou : '+embelezeTempo(duracao))
        print('execução Total demorará : '+embelezeTempo(duracao*tamanhoFile))
        fim,inicio,duracao,tamanhoFile = [None,None,None,None]
        firstTime = False
file.close()
with imageio.get_writer('bulbasaurEvolve.gif', mode='I') as writer:
    for n in range(quantiaFrames):
        imagem = imageio.imread(nomeFrame.format(n))
        writer.append_data(imagem)
fimDef = time()
imagemInicial.close()
imagemFinal.close()
print('\nfinalizado')
print('execução : '+embelezeTempo(fimDef-inicioDef))
