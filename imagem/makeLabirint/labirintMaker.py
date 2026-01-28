from PIL import Image
from random import randint
from numpy.random import permutation
from os import listdir

def makeALabirint(imagem,verticesAbertos):
    if verticesAbertos:
        largura,altura = imagem.size
        indice = randint(0,len(verticesAbertos)-1)
        doThePop = True
        x,y = verticesAbertos[indice]
        for direction in permutation(4).tolist():
            if direction==0:
                if y > 1:
                    if imagem.getpixel((x,y-2)) == PRETO:
                        imagem.putpixel((x,y-1),BRANCO)
                        imagem.putpixel((x,y-2),BRANCO)
                        verticesAbertos.append((x,y-2))
                        doThePop = False
                        break
            if direction==1:
                if x < largura-2:
                    if imagem.getpixel((x+2,y)) == PRETO:
                        imagem.putpixel((x+1,y),BRANCO)
                        imagem.putpixel((x+2,y),BRANCO)
                        verticesAbertos.append((x+2,y))
                        doThePop = False
                        break
            if direction==2:
                if y < altura-2:
                    if imagem.getpixel((x,y+2)) == PRETO:
                        imagem.putpixel((x,y+1),BRANCO)
                        imagem.putpixel((x,y+2),BRANCO)
                        verticesAbertos.append((x,y+2))
                        doThePop = False
                        break
            if direction==3:
                if x > 1:
                    if imagem.getpixel((x-2,y)) == PRETO:
                        imagem.putpixel((x-1,y),BRANCO)
                        imagem.putpixel((x-2,y),BRANCO)
                        verticesAbertos.append((x-2,y))
                        doThePop = False
                        break
        if doThePop:
            verticesAbertos.pop(indice)

BRANCO = (255,255,255,255)
PRETO = (0,0,0,255)
largura = 25
altura = 25
if not largura%2:
    largura += 1
if not altura%2:
    altura +=1
verticesAbertosInicio = [(1,1)]
imagem = Image.new('RGBA',(largura,altura),(0,0,0,255))
imagem.putpixel((1,1),(BRANCO))
while verticesAbertos:
    makeALabirint(imagem,verticesAbertosInicio)
name = f'pureLabirint//labirint{len(listdir("pureLabirint")):04d}.png'
print(name)
imagem.save(name)
imagem.close()
