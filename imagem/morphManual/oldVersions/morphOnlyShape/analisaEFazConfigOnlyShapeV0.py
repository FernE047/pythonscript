from PIL import Image
from textos import embelezeTempo
import os

'''

SECÇÃO DE DIREÇÃO:

possui funções que funcionam com direções apontadas

'''

def coordDirecao(coord,n):
    if(n>7):
        n = n%8
    x,y = coord
    if n == 0:
        return(x+1,y+1)
    if n == 1:
        return(x,y+1)
    if n == 2:
        return(x-1,y+1)
    if n == 3:
        return(x+1,y)
    if n == 4:
        return(x-1,y)
    if n == 5:
        return(x+1,y-1)
    if n == 6:
        return(x,y-1)
    if n == 7:
        return(x-1,y-1)
    return (x,y)

'''

SECÇÃO VERDE:

Regiões que sejam 2D, chamadas de blob
cada Blob possui camadas que são conjuntos de coordenadas

'''

def procuraContornoVerde(imagem):
    contorno = []
    largura,altura = imagem.size
    for y in range(altura):
        ultimoElemento = False
        for x in range(largura):
            elementoAtual = imagem.getpixel((x,y))[3] != 0
            if((not ultimoElemento) and elementoAtual):
                if((x,y) not in contorno):
                    contorno.append((x,y))
            if((not elementoAtual) and ultimoElemento):
                if((x-1,y) not in contorno):
                    contorno.append((x-1,y))
            ultimoElemento = elementoAtual
        if elementoAtual:
            if((x-1,y) not in contorno):
                contorno.append((x-1,y))
    for x in range(largura):
        ultimoElemento = False
        for y in range(altura):
            elementoAtual = imagem.getpixel((x,y))[3] != 0
            if((not ultimoElemento) and elementoAtual):
                if((x,y) not in contorno):
                    contorno.append((x,y))
            if((not elementoAtual) and ultimoElemento):
                if((x,y-1) not in contorno):
                    contorno.append((x,y-1))
            ultimoElemento = elementoAtual
        if elementoAtual:
            if((x,y-1) not in contorno):
                contorno.append((x,y-1))
    return contorno

def procuraBlob(linhaAtual,imagem,blob,linhaAnterior = None):
    if(linhaAnterior == None):
        linhaAnterior = []
    proximaLinha = []
    for coord in linhaAtual:
        for direcao in range(8):
            coordenada = coordDirecao(coord,direcao)
            try:
                pixel = imagem.getpixel(coordenada)
            except:
                continue
            if pixel[3] != 0 :
                if coordenada not in linhaAtual:
                    if coordenada not in linhaAnterior:
                        if coordenada not in proximaLinha:
                            proximaLinha.append(coordenada)
    if(len(proximaLinha)>0):
        blob.append(proximaLinha)
        procuraBlob(proximaLinha,imagem,blob,linhaAnterior = linhaAtual)
        
def procuraBlobs(imagem):
    linhaAtual = procuraContornoVerde(imagem)
    blob = [linhaAtual]
    procuraBlob(linhaAtual,imagem,blob)
    return blob
    
'''

SECÇÃO ESCRITA:

ferramentas para auxiliar a escrita de linhas e blob

'''

def escreveLinhas(linhaInicial,linhaFinal,file):
    pontosLinhaInicial = len(linhaInicial)
    pontosLinhaFinal = len(linhaFinal)
    if(pontosLinhaInicial == pontosLinhaFinal):
        for n in range(pontosLinhaInicial):
            file.write(str(linhaInicial[n][0])+','+str(linhaInicial[n][1]))
            file.write(' '+str(linhaFinal[n][0])+','+str(linhaFinal[n][1])+'\n')
    elif(pontosLinhaInicial>pontosLinhaFinal):
        if(pontosLinhaInicial-1==0):
            multiplicador = 0
        else:
            multiplicador = (pontosLinhaFinal-1)/(pontosLinhaInicial-1)
        for n in range(pontosLinhaInicial):
            pontoFinal = int(n*multiplicador)
            file.write(str(linhaInicial[n][0])+','+str(linhaInicial[n][1]))
            file.write(' '+str(linhaFinal[pontoFinal][0])+','+str(linhaFinal[pontoFinal][1])+'\n')
    else:
        if(pontosLinhaFinal-1==0):
            multiplicador = 0
        else:
            multiplicador = (pontosLinhaInicial-1)/(pontosLinhaFinal-1)
        for n in range(pontosLinhaFinal):
            pontoInicial = int(n*multiplicador)
            file.write(str(linhaInicial[pontoInicial][0])+','+str(linhaInicial[pontoInicial][1]))
            file.write(' '+str(linhaFinal[n][0])+','+str(linhaFinal[n][1])+'\n')

def escreveBlobs(blobInicial,blobFinal,file):
    pontosBlobInicial = len(blobInicial)
    pontosBlobFinal = len(blobFinal)
    if(pontosBlobInicial == pontosBlobFinal):
        for n in range(pontosBlobInicial):
            escreveLinhas(blobInicial[n],blobFinal[n],file)
    elif(pontosBlobInicial>pontosBlobFinal):
        if(pontosBlobInicial-1 == 0):
            multiplicador = 0
        else:
            multiplicador = (pontosBlobFinal-1)/(pontosBlobInicial-1)
        for n in range(pontosBlobInicial):
            camadaFinal = int(n*multiplicador)
            escreveLinhas(blobInicial[n],blobFinal[camadaFinal],file)
    else:
        if(pontosBlobFinal-1 == 0):
            multiplicador = 0
        else:
            multiplicador = (pontosBlobInicial-1)/(pontosBlobFinal-1)
        for n in range(pontosBlobFinal):
            camadaInicial = int(n*multiplicador)
            escreveLinhas(blobInicial[camadaInicial],blobFinal[n],file)

'''

SECÇÃO DEBUG:

'''

def imprimeBlob(blobs):
    for n,blob in enumerate(blobs):
        print('\nblob '+str(n)+' : \n')
        for m,camada in enumerate(blob):
            print('camada '+str(m)+' : \n')
            for coord in camada:
                print(coord)

'''

SECÇÃO Forma:

'''

def detectCorners(imagem):
    largura,altura = imagem.size
    xMenor = largura
    xMaior = 0
    yMenor = altura
    yMaior = 0
    for x in range(largura):
        for y in range(altura):
            pixel = imagem.getpixel((x,y))
            if pixel[3] == 255 :
                if x<xMenor:
                    xMenor = x
                if y<yMenor:
                    yMenor = y
                if x>xMaior:
                    xMaior = x
                if y>yMaior:
                    yMaior = y
    return(xMenor,xMaior,yMenor,yMaior)

def fazForma(imagem):
    forma = Image.new("RGBA",imagem.size,(0,0,0,0))
    xMenor,xMaior,yMenor,yMaior = detectCorners(imagem)
    for x in range(xMenor,xMaior):
        for y in range(yMenor,yMaior):
            forma.putpixel((x,y),(0,0,0,255))
    return forma

'''

SECÇÃO MAIN:

'''

parteInicial = Image.open('C:\\pythonscript\\imagem\\morphOnlyShape\\inicial.png')
fileConfig = open('C:\\pythonscript\\imagem\\morphOnlyShape\\config.txt','w')
blobInicial = procuraBlobs(parteInicial)
parteFinal = fazForma(parteInicial)
blobFinal = procuraBlobs(parteFinal)
parteInicial.close()
parteFinal.close()
escreveBlobs(blobInicial,blobFinal,fileConfig)
fileConfig.close()
