from PIL import Image
import os
import pypdn

"""

SECÇÃO UTILITARIOS DO MAIN:

ferramentas utilizadas pelo main

"""

def hasColor(imagem):
    largura,altura = imagem.size
    hasBlack = False
    hasGreen = False
    hasRed = False
    hasBlue = False
    hasBlueIterative = False
    for x in range(largura):
        for y in range(altura):
            pixel = imagem.getpixel((x,y))
            if(pixel[3] == 0):
                continue
            if(pixel[0] != 0):
                hasRed = True
                continue
            if(pixel[1] != 0):
                hasGreen = True
                continue
            if(pixel[2] != 0):
                hasBlue = True
            if(pixel[2] == 200):
                hasBlueIterative = True
    return(hasRed,hasGreen,hasBlue,hasBlueIterative)

def limpaPasta(pasta):
    arquivos = [pasta+"\\"+a for a in os.listdir(pasta)]
    if("C:\\pythonscript\\imagem\\morphManual\\frames\\resized" in arquivos):
        arquivos.pop(arquivos.index("C:\\pythonscript\\imagem\\morphManual\\frames\\resized"))
    for arquivo in arquivos:
        os.remove(arquivo)

"""

SECÇÃO VERMELHA:

pontos únicos

"""

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

"""

SECÇÃO DE DIREÇÃO:

possui funções que funcionam com direções apontadas pela secção azul

"""

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

"""

SECÇÃO AZUL:

linhas que sejam direcionadas de acordo com direções de 1 a 8 com:

7 6 5
4 X 3
2 1 0

"""

def procuraInicioDaLinhaAzul(imagem):
    largura,altura = imagem.size
    for x in range(largura):
        inicioDaLinha = False
        for y in range(altura):
            pixel = imagem.getpixel((x,y))
            if(pixel[3] == 0):
                continue
            if(pixel[2] != 0):
                inicioDaLinha = True
                for direcao in range(8):
                    try:
                        pixelAoRedor = imagem.getpixel(coordDirecao((x,y),direcao))
                    except:
                        continue
                    if(pixelAoRedor[3] != 0):
                        if(pixelAoRedor[2] != 0):
                            if(pixelAoRedor[2]%8 == 7-direcao):
                                inicioDaLinha = False
                if(inicioDaLinha):
                    return(x,y)

def procuraLinhaAzul(imagem):
    inicioDaLinha = procuraInicioDaLinhaAzul(imagem)
    pontoAtual = inicioDaLinha
    linha = [pontoAtual]
    while True:
        pontoAtual = coordDirecao(pontoAtual,imagem.getpixel(pontoAtual)[2])
        try:
            pixel = imagem.getpixel(pontoAtual)
        except:
            return(linha)
        if (pixel[2] == 0) or (pixel[3] == 0):
            return(linha)
        else:
            linha.append(pontoAtual)

def procuraInicioDaLinhaAzulIterativa(imagem):
    largura,altura = imagem.size
    for x in range(largura):
        inicioDaLinha = False
        for y in range(altura):
            pixel = imagem.getpixel((x,y))
            if(pixel[3] == 0):
                continue
            if(pixel[2] == 200):
                return(x,y)

def procuraLinhaAzulIterativo(imagem, anteriores = None):
    if anteriores is None:
        anteriores = [procuraInicioDaLinhaAzulIterativa(imagem)]
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
            #print(pontoInicial)
            #sprint(pontos)
            linhaMaxima = linha.copy()
            for ponto in pontos:
                novaLinha = procuraLinhaAzulIterativo(imagem, anteriores = linha + [ponto])
                if len(novaLinha)> len(linhaMaxima):
                    linhaMaxima = novaLinha.copy()
            #print(len(linhaMaxima))
            return linhaMaxima
"""

SECÇÃO VERDE:

Regiões que sejam 2D, chamadas de blob
cada Blob possui camadas que são conjuntos de coordenadas

"""

def procuraContornoVerde(imagem,tom):
    contorno = []
    largura,altura = imagem.size
    for y in range(altura):
        ultimoElemento = False
        for x in range(largura):
            elementoAtual = imagem.getpixel((x,y))[1]==tom
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
            elementoAtual = imagem.getpixel((x,y))[1]==tom
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

def procuraBlob(linhaAtual,imagem,tom,blob,linhaAnterior = None):
    if(linhaAnterior is None):
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
                if pixel[1] == tom :
                    if coordenada not in linhaAtual:
                        if coordenada not in linhaAnterior:
                            if coordenada not in proximaLinha:
                                proximaLinha.append(coordenada)
    if(len(proximaLinha)>0):
        blob.append(proximaLinha)
        procuraBlob(proximaLinha,imagem,tom,blob,linhaAnterior = linhaAtual)
        
def procuraBlobs(imagem,linhaAtual = None):
    blobs = []
    largura,altura = imagem.size
    tons = []
    for y in range(altura):
        for x in range(largura):
            coordenada = (x,y)
            pixel = imagem.getpixel(coordenada)
            if(pixel[3]!=0):
                if(pixel[1]!=0):
                    if(pixel[1] not in tons):
                        tons.append(pixel[1])
    tons.sort()
    for tom in tons:
        if((tom == 255)and(linhaAtual is not None)):
            blob = []
        else:
            linhaAtual = procuraContornoVerde(imagem,tom)
            blob = [linhaAtual]
        procuraBlob(linhaAtual,imagem,tom,blob)
        if len(blob)>0:
            blobs.append(blob)
    return blobs
    
"""

SECÇÃO ESCRITA:

ferramentas para auxiliar a escrita de linhas e blob

"""

def escreveLinhas(linhaInicial,linhaFinal,file):
    pontosLinhaInicial = len(linhaInicial)
    pontosLinhaFinal = len(linhaFinal)
    if(pontosLinhaInicial == pontosLinhaFinal):
        for n in range(pontosLinhaInicial):
            file.write(str(linhaInicial[n][0])+","+str(linhaInicial[n][1]))
            file.write(" "+str(linhaFinal[n][0])+","+str(linhaFinal[n][1])+"\n")
    elif(pontosLinhaInicial>pontosLinhaFinal):
        if(pontosLinhaInicial-1==0):
            multiplicador = 0
        else:
            multiplicador = (pontosLinhaFinal-1)/(pontosLinhaInicial-1)
        for n in range(pontosLinhaInicial):
            pontoFinal = int(n*multiplicador)
            file.write(str(linhaInicial[n][0])+","+str(linhaInicial[n][1]))
            file.write(" "+str(linhaFinal[pontoFinal][0])+","+str(linhaFinal[pontoFinal][1])+"\n")
    else:
        if(pontosLinhaFinal-1==0):
            multiplicador = 0
        else:
            multiplicador = (pontosLinhaInicial-1)/(pontosLinhaFinal-1)
        for n in range(pontosLinhaFinal):
            pontoInicial = int(n*multiplicador)
            file.write(str(linhaInicial[pontoInicial][0])+","+str(linhaInicial[pontoInicial][1]))
            file.write(" "+str(linhaFinal[n][0])+","+str(linhaFinal[n][1])+"\n")

def escreveBlobs(blobsInicial,blobsFinal,file):
    """print("blob inicial")
    print(blobsInicial)
    print("blob final")
    print(blobsFinal)
    print("\n\n\n")"""
    for blobInicial, blobFinal in zip(blobsInicial, blobsFinal):
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

"""

SECÇÃO Fundo:

"""

def fazFundo(fileConfig,parteInicial,parteFinal):
    largura,altura = parteInicial.size
    for y in range(altura):
        for x in range(largura):
            pixel = parteInicial.getpixel((x,y))
            if pixel[3] != 0:
                if parteFinal.getpixel((x,y))[3]!=0:
                    fileConfig.write(str(x)+","+str(y)+" "+str(x)+","+str(y)+"\n")
                else:
                    fileConfig.write(str(x)+","+str(y)+" fundo\n")
    parteInicial.close()
    parteFinal.close()
                    
                

"""

SECÇÃO DEBUG:

"""

def imprimeBlob(blobs):
    for n,blob in enumerate(blobs):
        print("\nblob "+str(n)+" : \n")
        for m,camada in enumerate(blob):
            print("camada "+str(m)+" : \n")
            for coord in camada:
                print(coord)

"""

SECÇÃO MAIN:

"""

limpaPasta("C:\\pythonscript\\imagem\\morphManual\\partesConfig")
limpaPasta("C:\\pythonscript\\imagem\\morphManual\\frames")
limpaPasta("C:\\pythonscript\\imagem\\morphManual\\frames\\resized")
nomeConfig = "partesConfig\\parte{0:02d}Config.txt"
imagemInicial = pypdn.read("inicial.pdn")
imagemFinal = pypdn.read("final.pdn")
quantiaPartes = len(imagemInicial.layers)
with open("config.txt","w", encoding="utf-8") as file:
    partes = None
    for nParte in range(1,quantiaPartes):
        print(nParte)
        parteInicial = Image.fromarray(imagemInicial.layers[nParte].image)
        parteFinal = Image.fromarray(imagemFinal.layers[nParte].image)
        if nParte == 1:
            if(parteInicial.getpixel((0,0))==(255,255,255,255)):
                fazFundo(file,parteInicial,parteFinal)
                continue
        with open(nomeConfig.format(nParte),"w", encoding="utf-8") as fileConfig:
            hasRGB = hasColor(parteInicial)
            print(hasRGB)
            if(hasRGB[0]):
                coordVermelhosInicial = procuraCor(parteInicial,0)
                coordVermelhosFinal = procuraCor(parteFinal,0)
            if(hasRGB[2]):
                if(hasRGB[3]):
                    linhaAzulInicial = procuraLinhaAzulIterativo(parteInicial)
                    linhaAzulFinal = procuraLinhaAzulIterativo(parteFinal)
                else:
                    linhaAzulInicial = procuraLinhaAzul(parteInicial)
                    linhaAzulFinal = procuraLinhaAzul(parteFinal)
            if(hasRGB[1]):
                if(hasRGB[2]):
                    blobsInicial = procuraBlobs(parteInicial,linhaAtual = linhaAzulInicial)
                    blobsFinal = procuraBlobs(parteFinal,linhaAtual = linhaAzulFinal)
                elif(hasRGB[0]):
                    blobsInicial = procuraBlobs(parteInicial,linhaAtual = [a[0] for a in coordVermelhosInicial])
                    blobsFinal = procuraBlobs(parteFinal,linhaAtual = [a[0] for a in coordVermelhosFinal])
                else:
                    blobsInicial = procuraBlobs(parteInicial)
                    blobsFinal = procuraBlobs(parteFinal)
                escreveBlobs(blobsInicial,blobsFinal,fileConfig)
            fileConfig.write("azul\n")
            if(hasRGB[2]):
                escreveLinhas(linhaAzulInicial,linhaAzulFinal,fileConfig)
            fileConfig.write("vermelho\n")
            if(hasRGB[0]):
                for coordInicial, coordFinal in zip(coordVermelhosInicial, coordVermelhosFinal):
                    for coord_i, coord_f in zip(coordInicial, coordFinal):
                        fileConfig.write(str(coord_i[0])+","+str(coord_i[1]))
                        fileConfig.write(" "+str(coord_f[0])+","+str(coord_f[1])+"\n")
            print()
        parteInicial.close()
        parteFinal.close()
    for colorIndex in range(3):
        for nParte in range(1,quantiaPartes):
            with open(nomeConfig.format(nParte),"r") as fileConfig:
                linha = fileConfig.readline()
                if(colorIndex==1):
                    while(linha != "azul\n"):
                        linha = fileConfig.readline()
                    linha = fileConfig.readline()
                if(colorIndex==2):
                    while(linha != "vermelho\n"):
                        linha = fileConfig.readline()
                    linha = fileConfig.readline()
                while(linha):
                    if(linha[0] in ["a","v"]):
                        break
                    file.write(linha)
                    linha = fileConfig.readline()