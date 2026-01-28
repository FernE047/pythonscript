from PIL import Image
from textos import embelezeTempo
import os
import pypdn
from analisaEFazConfig import configPart
from morpher import funcaoCor
from morpher import funcaoCoord

def makeFrame(n,total,initial,final):
    imagemInicial = Image.open('C:\\pythonscript\\imagem\\morphManual\\inicial.png')
    imagemFinal = Image.open('C:\\pythonscript\\imagem\\morphManual\\final.png')
    print(n)
    frame = Image.open(f'C:\\pythonscript\\imagem\\morphManual\\frames\\frame{n+1:03d}.png')
    for nParte in range(initial,final):
        file = open(f'C:\\pythonscript\\imagem\\morphManual\\partesConfig\\parte{nParte:02d}Config.txt','r')
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
    frame.save(f'C:\\pythonscript\\imagem\\morphManual\\frames\\frame{n+1:03d}.png')
    imagemInicial.close()
    imagemFinal.close()
    frame.close()

if __name__ == '__main__':
    ultimaCamadaFeita = len(os.listdir('C:\\pythonscript\\imagem\\morphManual\\partesConfig'))
    imagemInicial = pypdn.read("inicial.pdn")
    imagemFinal = pypdn.read("final.pdn")
    quantiaPartes = len(imagemInicial.layers)
    for a in range(ultimaCamadaFeita+1,quantiaPartes):
        configPart([a,imagemInicial.layers[a].image,imagemFinal.layers[a].image])
        
    nomeFrame = 'C:\\pythonscript\\imagem\\morphManual\\frames\\frame{0:03d}.png'
    quantiaFrames = len(os.listdir('C:\\pythonscript\\imagem\\morphManual\\frames'))-2
    for a in range(quantiaFrames):
        makeFrame(a,quantiaFrames,ultimaCamadaFeita+1,quantiaPartes)
