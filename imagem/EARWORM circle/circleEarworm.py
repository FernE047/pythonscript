from colorsys import hsv_to_rgb as hTr
from userUtil import cadaMusicaFaca
from textos import separaPalavras
from PIL import Image
import math

def criaPaleta(N): #cria paleta, ainda não personalizado
    HSV_tuples = [(x*1.0/N,0.5,0.5) for x in range(N)]
    print(HSV_tuples)
    RGB_tuples = [hTr(*color) for color in HSV_tuples]
    print(RGB_tuples)
    RGB_tuples = [tuple([int(a*256-1) for a in hTr(*color)]) for color in HSV_tuples]
    print(RGB_tuples)

def coordenadasPrego(pregoNumber,quantia,tamanho):
    raio = (tamanho-10)//2
    pregosAngulo = 360/quantia
    radiano = pregosAngulo*pregoNumber*math.pi/180
    coord = (int(raio*math.cos(radiano))+raio+5 , int(raio*math.sin(radiano)+raio+5))
    return(coord)
              
def fazLinha(pontoInicial,pontoFinal,imagem,cor):
    if(pontoInicial[0]!=pontoFinal[0]):
        auxA=(pontoInicial[1]-pontoFinal[1])/(pontoInicial[0]-pontoFinal[0])
        auxB=pontoFinal[1]-pontoFinal[0]*auxA
    else:
        auxA=2
    if((auxA<=1)and(auxA>=-1)):
        if(pontoInicial[0]>pontoFinal[0]):
            flow=-1
        else:
            flow=1
        for x in range(pontoInicial[0],pontoFinal[0],flow):
            imagem.putpixel((x,int(auxA*x+auxB)),cor)
    else:
        auxA=(pontoInicial[0]-pontoFinal[0])/(pontoInicial[1]-pontoFinal[1])
        auxB=pontoFinal[0]-pontoFinal[1]*auxA
        if(pontoInicial[1]>pontoFinal[1]):
            flow=-1
        else:
            flow=1
        for y in range(pontoInicial[1],pontoFinal[1],flow):
            imagem.putpixel((int(auxA*y+auxB),y),cor)
    return(imagem)

def fazImagem(info):
    titulo,musica = info
    musicaSeparada = separaPalavras(musica)
    prego = []
    for palavra in musicaSeparada:
        if palavra not in prego:
            prego.append(palavra)
    totalPregos=len(prego)
    if(totalPregos<25):
        tamanho = (100,100)
    else:
        tamanho = (4*totalPregos,4*totalPregos)
    imagem = Image.new('RGBA',tamanho,(255,255,255,255))
    cor = (0,0,0,255)
    for indice in range(len(musicaSeparada)-1):
        pregoInicial = prego.index(musicaSeparada[indice])
        pregoFinal = prego.index(musicaSeparada[indice+1])
        if(pregoInicial!=pregoFinal):
            pontoInicial = coordenadasPrego(pregoInicial,totalPregos,tamanho[0])
            pontoFinal = coordenadasPrego(pregoFinal,totalPregos,tamanho[0])
            fazLinha(pontoInicial,pontoFinal,imagem,cor)
    for n in range(totalPregos):
        coord = coordenadasPrego(n,totalPregos,tamanho[0])
        imagem.putpixel(coord,(255,0,0,255))
    return(imagem.rotate(90))

cadaMusicaFaca(fazImagem,pastaDir='EarwormCircle')#,debug=True)
    
