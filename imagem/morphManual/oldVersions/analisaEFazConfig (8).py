from PIL import Image
import os
import pypdn
import multiprocessing
from random import randint

'''

SECÇÃO UTILITARIOS DO MAIN:

ferramentas utilizadas pelo main

'''

def hasColor(imagem):
    largura,altura = imagem.size
    hasGreen = False
    hasBlue = False
    for x in range(largura):
        for y in range(altura):
            pixel = imagem.getpixel((x,y))
            if(pixel[3] == 0):
                continue
            if(pixel[1] != 0):
                hasGreen = True
                if hasBlue:
                    return(hasGreen,hasBlue)
                else:
                    continue
            if(pixel[2] == 200):
                hasBlue = (x,y)
                if hasGreen:
                    return(hasGreen,hasBlue)
    return(hasGreen,hasBlue)

def limpaPasta(pasta):
    arquivos = [pasta+'\\'+a for a in os.listdir(pasta)]
    if('C:\\pythonscript\\imagem\\morphManual\\frames\\resized' in arquivos):
        arquivos.pop(arquivos.index('C:\\pythonscript\\imagem\\morphManual\\frames\\resized'))
    for arquivo in arquivos:
        os.remove(arquivo)

'''

SECÇÃO DE DIREÇÃO:

possui funções que funcionam com direções apontadas pela secção azul

'''

def coordDirecao(coord,n):
    x,y = coord
    if n == 0:
        return(x+1,y+1)
    if n == 1:
        return(x,y+1)
    if n == 2:
        return(x-1,y+1)
    if n == 3:
        return(x-1,y)
    if n == 4:
        return(x-1,y-1)
    if n == 5:
        return(x,y-1)
    if n == 6:
        return(x+1,y-1)
    if n == 7:
        return(x+1,y)
    return (x,y)

'''

SECÇÃO AZUL:

linhas que se iniciam no tom 200 e continuam no tom 255

'''

def procuraAzulInicial(imagem):
    largura,altura = imagem.size
    for x in range(largura):
        for y in range(altura):
            pixel = imagem.getpixel((x,y))
            if pixel[3] == 0:
                continue
            if pixel[2] == 200:
                return(x,y)

def procuraLinhaAzul(imagem, anteriores = None, inicio = None):
    if anteriores is None:
        if inicio is None:
            anteriores = [procuraAzulInicial(imagem)]
        else:
            anteriores = [inicio]
    linha = anteriores.copy()
    pontoInicial = anteriores[-1]
    anteriores = None
    while True:
        pontos = []
        for d in range(8):
            pontoAtual = coordDirecao(pontoInicial,d)
            if pontoAtual not in linha:
                try:
                    pixel = imagem.getpixel(pontoAtual)
                    if pixel[3] == 0:
                        continue
                    if pixel[2] == 255:
                        pontos.append(pontoAtual)
                except:
                    pass
        if len(pontos) == 0:
            return linha
        elif len(pontos) == 1:
            pontoInicial = pontos[0]
            linha.append(pontoInicial)
        else:
            linhaMaxima = linha.copy()
            for ponto in pontos:
                novaLinha = procuraLinhaAzul(imagem, anteriores = linha + [ponto])
                if len(novaLinha)> len(linhaMaxima):
                    linhaMaxima = novaLinha.copy()
            return linhaMaxima
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
            elementoAtual = imagem.getpixel((x,y))[3]==255
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
            elementoAtual = imagem.getpixel((x,y))[3]==255
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
    return ordenaLinha(contorno)

def isCoordInBlob(coordTeste,blob):
    for camada in blob:
        for coord in camada:
            if coordTeste == coord:
                return True
    return False

def procuraBlob(imagem,blob):
    linhaAtual = []
    linhaAnterior = blob[-1]
    for coord in linhaAnterior:
        for direcao in (1,3,5,7):
            coordenada = coordDirecao(coord,direcao)
            try:
                pixel = imagem.getpixel(coordenada)
            except:
                continue
            if pixel[3] != 0 :
                if pixel[1] == 255 :
                    if coordenada not in linhaAtual:
                        if not isCoordInBlob(coordenada,blob):
                            linhaAtual.append(coordenada)
    if(len(linhaAtual)>0):
        linhaAtual = ordenaLinha(linhaAtual)
        if linhaAtual not in blob:
            blob.append(linhaAtual)
            procuraBlob(imagem,blob)
    
def ordenaLinha(linhaOriginal):
    linhaTotal = []
    linhas = divideLinha(linhaOriginal)
    for linha in linhas:
        linhaTotal += ordenaLinhaInd(linha)
    return linhaTotal

def divideLinha(linha):
    linhas = []
    for ponto in linha:
        linhasAppend = []
        for n in range(len(linhas)):
            novaLinha = linhas[n]
            for novoPonto in novaLinha:
                if distancia(ponto,novoPonto) <= 2**(1/2)+0.01:
                    linhasAppend.append(n)
                    break
        if len(linhasAppend) == 0:
            linhas.append([ponto])
        elif len(linhasAppend) == 1:
            linhas[linhasAppend[0]].append(ponto)
        else:
            superLinha = []
            for n in linhasAppend:
                superLinha += linhas[n].copy()
            for n in reversed(sorted(linhasAppend)):
                linhas.pop(n)
            superLinha.append(ponto)
            linhas.append(superLinha)
    return linhas

def ordenaLinhaInd(linha):
    tamanho = len(linha)
    maiorLinha = []
    for n in range(tamanho):
        linhaTeste = linha.copy()
        primeiroPonto = linha[n]
        linhaTeste = ordenaLinhaIt(linhaTeste,inicio = primeiroPonto)
        if len(linhaTeste) == tamanho:
            return linhaTeste
        if len(linhaTeste) > len(maiorLinha):
            maiorLinha = linhaTeste.copy()
    return maiorLinha
    

def ordenaLinhaIt(linhaDesordenada, anteriores = None, inicio = None):
    if anteriores is None:
        anteriores = [inicio]
    linhaOrdenada = anteriores.copy()
    pontoInicial = anteriores[-1]
    anteriores = None
    while True:
        pontos = []
        for d in range(8):
            pontoAtual = coordDirecao(pontoInicial,d)
            if pontoAtual in linhaDesordenada:
                if pontoAtual not in linhaOrdenada:
                    pontos.append(pontoAtual)
        if len(pontos) == 0:
            return linhaOrdenada
        elif len(pontos) == 1:
            pontoInicial = pontos[0]
            linhaOrdenada.append(pontoInicial)
        else:
            linhaMaxima = linhaOrdenada.copy()
            for ponto in pontos:
                novaLinha = ordenaLinhaIt(linhaDesordenada, anteriores = linhaOrdenada + [ponto])
                if len(novaLinha) == len(linhaDesordenada):
                    return novaLinha
                if len(novaLinha) > len(linhaMaxima):
                    linhaMaxima = novaLinha.copy()
            return linhaMaxima

def distancia(pontoA,pontoB):
    soma = 0
    for n in range(len(pontoA)):
        soma += abs(pontoA[n]-pontoB[n])**2
    return soma**(1/2)
    
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

SECÇÃO Fundo:

'''

def fazFundo(fileConfig,parteInicial,parteFinal): #REMAKE
    pass

'''

SECÇÃO DEBUG:

'''

def imprimeBlob(blob,imagem):
    for camada in blob:
        linhas = [camada]#divideLinha(camada)
        for linha in linhas:
            cor = tuple([randint(0,255) for a in range(3)])
            for coord in linha:
                imagem.putpixel(coord,cor)
    imagem.save("C:\\pythonscript\\imagem\\morphManual\\partesConfig\\debugBlob{0:03d}.png".format(len(os.listdir('C:\\pythonscript\\imagem\\morphManual\\partesConfig'))))

'''

SECÇÃO MAIN:

'''

def configPart(data):
    n,imagemInicial,imagemFinal = data
    print("Fazendo Parte : " + str(n))
    parteInicial = Image.fromarray(imagemInicial)
    parteFinal = Image.fromarray(imagemFinal)
    fileConfig = open('partesConfig\\parte{0:02d}Config.txt'.format(n),'w')
    if n == 1:
        fazFundo(fileConfig,parteInicial,parteFinal)
    else:
        hasRGB = hasColor(parteInicial)
        if(hasRGB[1]):
            linhaAzulInicial = procuraLinhaAzul(parteInicial,inicio = hasRGB[1])
            linhaAzulFinal = procuraLinhaAzul(parteFinal)
        if(hasRGB[0]):
            if(hasRGB[1]):
                blobInicial = [linhaAzulInicial]
                blobFinal = [linhaAzulFinal]
            else:
                blobInicial = [procuraContornoVerde(parteInicial)]
                blobFinal = [procuraContornoVerde(parteFinal)]
            procuraBlob(parteInicial,blobInicial)
            procuraBlob(parteFinal,blobFinal)
            escreveBlobs(blobInicial,blobFinal,fileConfig)
        else:
            escreveLinhas(linhaAzulInicial,linhaAzulFinal,fileConfig)
    print("\tParte Terminada : " + str(n))
    fileConfig.close()
    parteInicial.close()
    parteFinal.close()

if __name__ == '__main__':
    limpaPasta('C:\\pythonscript\\imagem\\morphManual\\partesConfig')
    limpaPasta('C:\\pythonscript\\imagem\\morphManual\\frames')
    limpaPasta('C:\\pythonscript\\imagem\\morphManual\\frames\\resized')
    imagemInicial = pypdn.read("inicial.pdn")
    imagemFinal = pypdn.read("final.pdn")
    Image.fromarray(imagemInicial.layers[0].image).save("inicial.png")
    Image.fromarray(imagemFinal.layers[0].image).save("final.png")
    quantiaPartes = len(imagemInicial.layers)
    p = multiprocessing.Pool(os.cpu_count())
    p.map(configPart,[[a,imagemInicial.layers[a].image,imagemFinal.layers[a].image] for a in range(1,quantiaPartes)])
