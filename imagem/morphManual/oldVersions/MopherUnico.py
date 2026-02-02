from PIL import Image
import pypdn
import os


def pegaInteiro(
    mensagem: str, minimo: int | None = None, maximo: int | None = None
) -> int:
    while True:
        entrada = input(f"{mensagem} : ")
        try:
            valor = int(entrada)
            if (minimo is not None) and (valor < minimo):
                print(f"valor deve ser maior ou igual a {minimo}")
                continue
            if (maximo is not None) and (valor > maximo):
                print(f"valor deve ser menor ou igual a {maximo}")
                continue
            return valor
        except Exception as _:
            print("valor inválido, tente novamente")

"""

SECÇÃO UTILITARIOS DO MAIN:

ferramentas utilizadas pelo main

"""

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
"""

SECÇÃO VERDE:

Regiões que sejam 2D, chamadas de blob
cada Blob possui camadas que são conjuntos de coordenadas

"""

def procuraContornoVerde(imagem):
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
        for direcao in range(8):
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
        blob.append(proximaLinha)
        procuraBlob(imagem,proximaLinha,blob,linhaAnterior = linhaAtual)
    
"""

SECÇÃO ESCRITA:

ferramentas para auxiliar a escrita de linhas e blob

"""

def escreveLinhas(imagemInicialPNG,imagemFinalPNG,linhaInicial,linhaFinal,file,total):
    pontosLinhaInicial = len(linhaInicial)
    pontosLinhaFinal = len(linhaFinal)
    if(pontosLinhaInicial == pontosLinhaFinal):
        for n in range(pontosLinhaInicial):
            linha = [] #linha de texto
            for m in range(2):
                B = linhaInicial[n][m]
                A = (linhaFinal[n][m]-B)
                linha.append(str(A)+","+str(B))
            pixelInicial = imagemInicialPNG.getpixel(linhaInicial[n])
            pixelFinal = imagemFinalPNG.getpixel(linhaFinal[n])
            for m in range(3):
                B = pixelInicial[m]
                A = (pixelFinal[m]-B)
                linha.append(str(A)+","+str(B))
            file.write(" ".join(linha)+"\n")
    elif(pontosLinhaInicial>pontosLinhaFinal):
        if(pontosLinhaInicial-1==0):
            multiplicador = 0
        else:
            multiplicador = (pontosLinhaFinal-1)/(pontosLinhaInicial-1)
        for n in range(pontosLinhaInicial):
            linha = [] #linha de texto
            pontoFinal = int(n*multiplicador)
            for m in range(2):
                B = linhaInicial[n][m]
                A = (linhaFinal[pontoFinal][m]-B)
                linha.append(str(A)+","+str(B))
            pixelInicial = imagemInicialPNG.getpixel(linhaInicial[n])
            pixelFinal = imagemFinalPNG.getpixel(linhaFinal[pontoFinal])
            for m in range(3):
                B = pixelInicial[m]
                A = pixelFinal[m]-B
                linha.append(str(A)+","+str(B))
            file.write(" ".join(linha)+"\n")
    else:
        if(pontosLinhaFinal-1==0):
            multiplicador = 0
        else:
            multiplicador = (pontosLinhaInicial-1)/(pontosLinhaFinal-1)
        for n in range(pontosLinhaFinal):
            linha = [] #linha de texto
            pontoInicial = int(n*multiplicador)
            for m in range(2):
                B = linhaInicial[pontoInicial][m]
                A = linhaFinal[n][m]-B
                linha.append(str(A)+","+str(B))
            pixelInicial = imagemInicialPNG.getpixel(linhaInicial[pontoInicial])
            pixelFinal = imagemFinalPNG.getpixel(linhaFinal[n])
            for m in range(3):
                B = pixelInicial[m]
                A = pixelFinal[m]-B
                linha.append(str(A)+","+str(B))
            file.write(" ".join(linha)+"\n")

def escreveBlobs(imagemInicialPNG,imagemFinalPNG,blobInicial,blobFinal,file,quantiaFrames):
    """print("blob inicial")
    print(blobsInicial)
    print("blob final")
    print(blobsFinal)
    print("\n\n\n")"""
    pontosBlobInicial = len(blobInicial)
    pontosBlobFinal = len(blobFinal)
    if(pontosBlobInicial == pontosBlobFinal):
        for n in range(pontosBlobInicial):
            escreveLinhas(imagemInicialPNG,imagemFinalPNG,blobInicial[n],blobFinal[n],file,quantiaFrames)
    elif(pontosBlobInicial>pontosBlobFinal):
        if(pontosBlobInicial-1 == 0):
            multiplicador = 0
        else:
            multiplicador = (pontosBlobFinal-1)/(pontosBlobInicial-1)
        for n in range(pontosBlobInicial):
            camadaFinal = int(n*multiplicador)
            escreveLinhas(imagemInicialPNG,imagemFinalPNG,blobInicial[n],blobFinal[camadaFinal],file,quantiaFrames)
    else:
        if(pontosBlobFinal-1 == 0):
            multiplicador = 0
        else:
            multiplicador = (pontosBlobInicial-1)/(pontosBlobFinal-1)
        for n in range(pontosBlobFinal):
            camadaInicial = int(n*multiplicador)
            escreveLinhas(imagemInicialPNG,imagemFinalPNG,blobInicial[camadaInicial],blobFinal[n],file,quantiaFrames)

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

def fazConfig(quantiaFrames):
    nomeConfig = "partesConfig\\parte{0:02d}Config.txt"
    imagemInicialPDN = pypdn.read("inicial.pdn")
    imagemFinalPDN = pypdn.read("final.pdn")
    imagemInicialPNG = Image.fromarray(imagemInicialPDN.layers[0].image)
    imagemFinalPNG = Image.fromarray(imagemFinalPDN.layers[0].image)
    quantiaPartes = len(imagemInicialPDN.layers)
    with open("config.txt","w", encoding = "utf-8") as file:
        partes = None
        for nParte in range(1,quantiaPartes):
            print(nParte)
            parteInicial = Image.fromarray(imagemInicialPDN.layers[nParte].image)
            parteFinal = Image.fromarray(imagemFinalPDN.layers[nParte].image)
            if nParte == 1:
                if(parteInicial.getpixel((0,0))==(255,255,255,255)):
                    fazFundo(file,parteInicial,parteFinal)
                    continue
            with open(nomeConfig.format(nParte),"w", encoding = "utf-8") as fileConfig:
                hasRGB = hasColor(parteInicial)
                print(hasRGB)
                if(hasRGB[0]):
                    coordVermelhosInicial = procuraCor(parteInicial,0)
                    coordVermelhosFinal = procuraCor(parteFinal,0)
                if(hasRGB[2]):
                    linhaAzulInicial = procuraLinhaAzul(parteInicial,primeiro = hasRGB[2])
                    linhaAzulFinal = procuraLinhaAzul(parteFinal)
                    escreveLinhas(imagemInicialPNG,imagemFinalPNG,linhaAzulInicial,linhaAzulFinal,fileConfig,quantiaFrames)
                if(hasRGB[3]):
                    linhaAzulInicial = procuraLinhaAzulIterativo(parteInicial,inicio = hasRGB[3])
                    linhaAzulFinal = procuraLinhaAzulIterativo(parteFinal)
                    escreveLinhas(imagemInicialPNG,imagemFinalPNG,linhaAzulInicial,linhaAzulFinal,fileConfig,quantiaFrames)
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
                        blobsInicial = []
                        procuraBlob(parteInicial,[],blobsInicial)
                        blobsFinal = []
                        procuraBlob(parteFinal,[],blobsFinal)
                    escreveBlobs(imagemInicialPNG,imagemFinalPNG,blobsInicial,blobsFinal,fileConfig,quantiaFrames)
                if(hasRGB[0]):
                    for coordInicial, coordFinal in zip(coordVermelhosInicial, coordVermelhosFinal):
                        for coord_i, coord_f in zip(coordInicial, coordFinal):
                            fileConfig.write(str(coord_i[0])+","+str(coord_i[1]))
                            fileConfig.write(" "+str(coord_f[0])+","+str(coord_f[1])+"\n")
                print()
            parteInicial.close()
            parteFinal.close()
        for nParte in range(1,quantiaPartes):
            with open(nomeConfig.format(nParte),"r", encoding = "utf-8") as fileConfig:
                linha = fileConfig.readline()
                while(linha):
                    file.write(linha)
                    linha = fileConfig.readline()
    return [imagemInicialPNG,imagemFinalPNG]

def funcaoAfim(inicio,fim,total,n):
    elemento = []
    for elementoInicial, elementoFinal in zip(inicio, fim):
        B = elementoInicial
        A = (elementoFinal-elementoInicial)/(total+1)
        elemento.append(int(A*n+B))
    return tuple(elemento)

quantiaFrames = 30#pegaInteiro("quantos frames?")
limpaPasta("C:\\pythonscript\\imagem\\morphManual\\partesConfig")
limpaPasta("C:\\pythonscript\\imagem\\morphManual\\frames")
limpaPasta("C:\\pythonscript\\imagem\\morphManual\\frames\\resized")
nomeFrame = "frames\\frame{0:03d}.png"
imagemInicial,imagemFinal = fazConfig(quantiaFrames)
imagemInicial.save(nomeFrame.format(0))
imagemFinal.save(nomeFrame.format(quantiaFrames+1))
print("\n tamanho: "+str(imagemInicial.size),end="\n\n")
for n in range(quantiaFrames):
    print(n)
    frame = Image.new("RGBA",imagemFinal.size,(255,255,255,0))
    with open("config.txt", "r", encoding="utf-8") as file:
        linha = file.readline()
        while(linha):
            if(linha.find("fundo")!=-1):
                coord = tuple([int(b) for b in linha[:-6].split(",")])
                frame.putpixel(coord,imagemInicial.getpixel(coord))
            else:
                dados = [tuple([int(b) for b in coord.split(",")]) for coord in linha.split(" ")]
                novaCoord = []
                for m in range(2):
                    A = dados[m][0]
                    B = dados[m][1]
                    novaCoord.append(int((n+1)*A/(quantiaFrames+1)+B))
                novaCoord = tuple(novaCoord)
                novaCor = []
                for m in range(3):
                    A = dados[m+2][0]
                    B = dados[m+2][1]
                    novaCor.append(int((n+1)*A/(quantiaFrames+1)+B))
                novaCor.append(255)
                novaCor = tuple(novaCor)
                frame.putpixel(novaCoord,novaCor)
            linha = file.readline()
        frame.save(nomeFrame.format(n+1))
        frame.close()
imagemInicial.close()
imagemFinal.close()
