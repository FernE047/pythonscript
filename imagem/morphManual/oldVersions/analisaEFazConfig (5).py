from PIL import Image
from textos import embelezeTempo
import os
import pypdn

'''

SECÇÃO UTILITARIOS DO MAIN:

ferramentas utilizadas pelo main

'''

def hasColor(imagem):
    largura,altura = imagem.size
    hasGreen = False
    hasRed = False
    hasBlue = False
    hasBlueIterative = False
    for x in range(largura):
        for y in range(altura):
            pixel = imagem.getpixel((x,y))
            if(pixel[3] == 0):
                continue
            if(pixel[1] != 0):
                if(pixel[2] == 255):
                    continue
                hasGreen = True
                if hasBlueIterative or hasBlue or hasRed:
                    return(hasRed,hasGreen,hasBlue,hasBlueIterative)
                else:
                    continue
            if(pixel[2] != 0):
                if(pixel[2] == 200):
                    hasBlueIterative = (x,y)
                    if hasGreen:
                        return(hasRed,hasGreen,hasBlue,hasBlueIterative)
                else:
                    hasBlue = (x,y)
                    if hasGreen:
                        return(hasRed,hasGreen,hasBlue,hasBlueIterative)
                continue
            if(pixel[0] != 0):
                hasRed = True
                if hasGreen:
                    return(hasRed,hasGreen,hasBlue,hasBlueIterative)
    return(hasRed,hasGreen,hasBlue,hasBlueIterative)

def limpaPasta(pasta):
    arquivos = [pasta+'\\'+a for a in os.listdir(pasta)]
    if('C:\\pythonscript\\imagem\\morphManual\\frames\\resized' in arquivos):
        arquivos.pop(arquivos.index('C:\\pythonscript\\imagem\\morphManual\\frames\\resized'))
    for arquivo in arquivos:
        os.remove(arquivo)

'''

SECÇÃO VERMELHA:

pontos únicos

'''

def procuraCor(imagem,indexColor):
    largura,altura = imagem.size
    listaDeCores = []
    coordenadasDasCores = []
    for x in range(largura):
        for y in range(altura):
            pixel = imagem.getpixel((x,y))
            if(pixel[3]==0):
                continue
            cor = pixel[indexColor]
            if(cor != 0):
                if(cor not in listaDeCores):
                    listaDeCores.append(cor)
                    coordenadasDasCores.append([(x,y)])
                else:
                    corIndex = listaDeCores.index(cor)
                    coordenadasDasCores[corIndex].append((x,y))
    return coordenadasDasCores

'''

SECÇÃO DE DIREÇÃO:

possui funções que funcionam com direções apontadas pela secção azul

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

linhas que sejam direcionadas de acordo com direções de 1 a 8 com:

7 6 5
4 X 3
2 1 0

'''

def procuraLinhaAzul(imagem,primeiro = None):
    largura,altura = imagem.size
    if primeiro is None:
        primeiro = procuraUmAzul(imagem, range(248,256))
    linha = [primeiro]
    pontoAtual = primeiro
    while True:
        pontoAtual = coordDirecao(pontoAtual,imagem.getpixel(pontoAtual)[2])
        try:
            pixel = imagem.getpixel(pontoAtual)
        except:
            break
        if (pixel[2] == 0) or (pixel[3] == 0):
            break
        else:
            linha.append(pontoAtual)
    inicioDaLinha = True
    while True:
        for direcao in range(8):
            try:
                coord = coordDirecao(primeiro,direcao)
                pixelAoRedor = imagem.getpixel(coord)
            except:
                continue
            if(pixelAoRedor[3] != 0):
                if pixelAoRedor not in linha:
                    if(pixelAoRedor[2] != 0):
                        if(pixelAoRedor[2]%8 == 7-direcao):
                            primeiro = coord
                            linha = [primeiro] + linha
                            inicioDaLinha = False
                            break
        if inicioDaLinha:
            return linha
        else:
            inicioDaLinha = True

def procuraUmAzul(imagem, tons):
    largura,altura = imagem.size
    for x in range(largura):
        inicioDaLinha = False
        for y in range(altura):
            pixel = imagem.getpixel((x,y))
            if(pixel[3] == 0):
                continue
            if pixel[2] in tons:
                return(x,y)

def procuraLinhaAzulIterativo(imagem, anteriores = None, inicio = None):
    if anteriores is None:
        if inicio is None:
            anteriores = [procuraUmAzul(imagem, [200])]
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
                    if(pixel[3] == 0):
                        continue
                    if pixel[:3] == (0,255,255):
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
                novaLinha = procuraLinhaAzulIterativo(imagem, anteriores = linha + [ponto])
                if len(novaLinha)> len(linhaMaxima):
                    linhaMaxima = novaLinha.copy()
            return linhaMaxima
'''

SECÇÃO VERDE:

Regiões que sejam 2D, chamadas de blob
cada Blob possui camadas que são conjuntos de coordenadas

'''

def procuraContornoVerde(imagem): #obsolete
    contorno = []
    largura,altura = imagem.size
    for y in range(altura):
        ultimoElemento = False
        for x in range(largura):
            elementoAtual = imagem.getpixel((x,y))[1]==255
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
            elementoAtual = imagem.getpixel((x,y))[1]==255
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

def procuraBlob(imagem,linhaAtual,blob,linhaAnterior = None):
    if(linhaAnterior == None):
        linhaAnterior = []
    proximaLinha = []
    for coord in linhaAtual:
        for direcao in range(1,8,2):
            coordenada = coordDirecao(coord,direcao)
            try:
                pixel = imagem.getpixel(coordenada)
            except:
                continue
            if pixel[3] != 0 :
                if pixel[1] == 255 :
                    if coordenada not in linhaAtual:
                        if coordenada not in linhaAnterior:
                            if coordenada not in proximaLinha:
                                proximaLinha.append(coordenada)
    if(len(proximaLinha)>0):
        proximaLinha = ordenaLinha(proximaLinha)
        blob.append(proximaLinha)
        procuraBlob(imagem,proximaLinha,blob,linhaAnterior = linhaAtual)

def divideLinha(linha):
    linhas = []
    for ponto in linha:
        pontoAppend = False
        for n in range(len(linhas)):
            novaLinha = linhas[n]
            for novoPonto in novaLinha:
                if distancia(ponto,novoPonto) <= 2**(1/2)+0.01:
                    #print("a")
                    pontoAppend = True
                    break
            if pontoAppend:
                novaLinha.append(ponto)
                break
        if not pontoAppend:
            linhas.append([ponto])
    return linhas
    
def ordenaLinha(linhaOriginal):
    linhaTotal = []
    linhas = divideLinha(linhaOriginal)
    for linha in linhas:
        linhaTotal += ordenaLinhaInd(linha)
    return linhaTotal

def ordenaLinhaInd(linha):
    tamanho = len(linha)
    for n in range(min((4,tamanho))):
        linhaTeste = linha.copy()
        primeiroPonto = linha[n]
        linhaTeste = ordenaLinhaIt(linhaTeste,inicio = primeiroPonto)
        if len(linhaTeste) == tamanho:
            return linhaTeste

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
        if len(pontos) == 1:
            pontoInicial = pontos[0]
            linhaOrdenada.append(pontoInicial)
        else:
            linhaMaxima = linhaOrdenada.copy()
            for ponto in pontos:
                novaLinha = ordenaLinhaIt(linhaDesordenada, anteriores = linhaOrdenada + [ponto])
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
    '''print('blob inicial')
    print(blobsInicial)
    print('blob final')
    print(blobsFinal)
    print('\n\n\n')'''
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

def fazFundo(fileConfig,parteInicial,parteFinal):
    largura,altura = parteInicial.size
    for y in range(altura):
        for x in range(largura):
            pixel = parteInicial.getpixel((x,y))
            if pixel[3] != 0:
                if parteFinal.getpixel((x,y))[3]!=0:
                    fileConfig.write(str(x)+','+str(y)+' '+str(x)+','+str(y)+'\n')
                else:
                    fileConfig.write(str(x)+','+str(y)+' fundo\n')
    parteInicial.close()
    parteFinal.close()
                    
                

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

SECÇÃO MAIN:

'''

limpaPasta('C:\\pythonscript\\imagem\\morphManual\\partesConfig')
limpaPasta('C:\\pythonscript\\imagem\\morphManual\\frames')
limpaPasta('C:\\pythonscript\\imagem\\morphManual\\frames\\resized')
nomeConfig = 'partesConfig\\parte{0:02d}Config.txt'
imagemInicial = pypdn.read("inicial.pdn")
imagemFinal = pypdn.read("final.pdn")
Image.fromarray(imagemInicial.layers[0].image).save("inicial.png")
Image.fromarray(imagemFinal.layers[0].image).save("final.png")
quantiaPartes = len(imagemInicial.layers)
file = open('config.txt','w')
partes = None
for nParte in range(1,quantiaPartes):
    print(nParte)
    parteInicial = Image.fromarray(imagemInicial.layers[nParte].image)
    parteFinal = Image.fromarray(imagemFinal.layers[nParte].image)
    if nParte == 1:
        fileConfig = open(nomeConfig.format(nParte),'w')
        fazFundo(file,parteInicial,parteFinal)
        fileConfig.close()
        continue
    fileConfig = open(nomeConfig.format(nParte),'w')
    hasRGB = hasColor(parteInicial)
    print(hasRGB)
    if(hasRGB[0]):
        coordVermelhosInicial = procuraCor(parteInicial,0)
        coordVermelhosFinal = procuraCor(parteFinal,0)
    if(hasRGB[2]):
        linhaAzulInicial = procuraLinhaAzul(parteInicial,primeiro = hasRGB[2])
        linhaAzulFinal = procuraLinhaAzul(parteFinal)
        escreveLinhas(linhaAzulInicial,linhaAzulFinal,fileConfig)
    if(hasRGB[3]):
        linhaAzulInicial = procuraLinhaAzulIterativo(parteInicial,inicio = hasRGB[3])
        linhaAzulFinal = procuraLinhaAzulIterativo(parteFinal)
        escreveLinhas(linhaAzulInicial,linhaAzulFinal,fileConfig)
    if(hasRGB[1]):
        if(hasRGB[2])or(hasRGB[3]):
            blobsInicial = [linhaAzulInicial]
            procuraBlob(parteInicial,linhaAzulInicial,blobsInicial)
            blobsFinal = [linhaAzulFinal]
            procuraBlob(parteFinal,linhaAzulFinal,blobsFinal)
        elif(hasRGB[0]):
            blobsInicial = [[a[0] for a in coordVermelhosInicial]]
            procuraBlob(parteInicial,blobsInicial[0],blobsInicial)
            blobsFinal = [[a[0] for a in coordVermelhosFinal]]
            procuraBlob(parteFinal,blobsFinal[0],blobsFinal)
        else:
            blobsInicial = [procuraContornoVerde(parteInicial)]
            procuraBlob(parteInicial,blobsInicial[0],blobsInicial)
            blobsFinal = [procuraContornoVerde(parteFinal)]
            procuraBlob(parteFinal,blobsFinal[0],blobsFinal)
        escreveBlobs(blobsInicial,blobsFinal,fileConfig)
    if(hasRGB[0]):
        for n in range(len(coordVermelhosInicial)):
            for m in range(len(coordVermelhosInicial[n])):
                fileConfig.write(str(coordVermelhosInicial[n][m][0])+','+str(coordVermelhosInicial[n][m][1]))
                fileConfig.write(' '+str(coordVermelhosFinal[n][m][0])+','+str(coordVermelhosFinal[n][m][1])+'\n')
    print()
    fileConfig.close()
    parteInicial.close()
    parteFinal.close()
for nParte in range(1,quantiaPartes):
    fileConfig = open(nomeConfig.format(nParte),'r')
    linha = fileConfig.readline()
    while(linha):
        file.write(linha)
        linha = fileConfig.readline()
    fileConfig.close()
file.close()
