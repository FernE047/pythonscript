from PIL import Image
import os
import multiprocessing
from random import randint
from time import sleep

class Linha:
    def __init__(self,pontos = None,circular = False):
        if pontos is None:
            self.pontos = []
            self.inicio = None
            self.fim = None
        else:
            self.pontos = pontos.copy()
            if self.pontos:
                self.inicio = self.pontos[0]
                self.fim = self.pontos[-1]
            else:
                self.inicio = None
                self.fim = None
        self.circular = circular
                    
    def procuraLinhaAzul(self,imagem):
        while True:
            pontoInicial = self.fim
            pontos = []
            for d in range(8):
                pontoAtual = coordDirecao(pontoInicial,d)
                if pontoAtual not in self:
                    try:
                        pixel = imagem.getpixel(pontoAtual)
                        if pixel[3] == 0:
                            continue
                        if pixel[2] == 255:
                            pontos.append(pontoAtual)
                    except:
                        pass
            if len(pontos) == 1:
                self.append(pontos[0])
            else:
                for ponto in pontos:
                    novaLinha = self.copy()
                    novaLinha.append(ponto)
                    novaLinha.procuraLinhaAzul(imagem)
                    if len(novaLinha)> len(self):
                        self.copy(novaLinha)
                break
    
    def sortAll(self):
        linhas = self.separa()
        self.pontos = []
        for linha in linhas:
            linha.sort()
            self.copy(self + linha)

    def separa(self):
        linhas = []
        for ponto in self.pontos:
            linhasQueTemOPonto = []
            for index,linha in enumerate(linhas):
                for novoPonto in linha.pontos:
                    if distancia(ponto,novoPonto) <= 2**(1/2)+0.01:
                        linhasQueTemOPonto.append(index)
                        break
            if len(linhasQueTemOPonto) == 0:
                linhas.append(Linha([ponto],circular = self.circular))
            elif len(linhasQueTemOPonto) == 1:
                linhas[linhasQueTemOPonto[0]].append(ponto)
            else:
                superLinha = linhas[linhasQueTemOPonto[0]].copy()
                for n in linhasQueTemOPonto[1:] :
                    superLinha += linhas[n]
                for n in reversed(sorted(linhasQueTemOPonto)):
                    linhas.pop(n)
                superLinha.append(ponto)
                linhas.append(superLinha)
        return linhas

    def sort(self):
        tamanho = len(self)
        maiorLinha = Linha(circular = self.circular)
        for n in range(min(4,tamanho)):
            linhaTeste = self.copy()
            primeiroPonto = self.pontos[n]
            linhaTeste.sortIt(Linha([primeiroPonto],circular = self.circular))
            if len(linhaTeste) == tamanho:
                maiorLinha = linhaTeste.copy()
                break
            if len(linhaTeste) > len(maiorLinha):
                maiorLinha = linhaTeste.copy()
        self.copy(maiorLinha)

    def sortIt(self, linhaOrdenada):
        while True:
            pontoInicial = linhaOrdenada.pontos[-1]
            pontos = self.pontosProximos(pontoInicial, exceptions = linhaOrdenada)
            if len(pontos) == 1:
                linhaOrdenada.append(pontos[0])
            else:
                if len(pontos) == 0:
                    if self.circular:
                        indice = self.pontos.index(pontoInicial)
                        if indice < len(self)-1:
                            linhaOrdenada.append(self.pontos[indice+1])
                            continue
                    maiorLinha = linhaOrdenada.copy()
                else:
                    antes = len(linhaOrdenada)
                    for ponto in pontos:
                        pontosProximosDele = self.pontosProximos(ponto, exceptions = linhaOrdenada)
                        if len(pontosProximosDele) == 1:
                            if pontosProximosDele[0] in pontos:
                                linhaOrdenada.append(ponto)
                                linhaOrdenada.append(pontosProximosDele[0])
                                break
                    if len(linhaOrdenada)!=antes:
                        continue
                    maiorLinha = linhaOrdenada.copy()
                    for ponto in pontos:
                        novaLinha = self.copy()
                        novaLinha.sortIt(linhaOrdenada + [ponto])
                        if len(novaLinha) == len(self):
                            maiorLinha = novaLinha.copy()
                            break
                        if len(novaLinha) > len(maiorLinha):
                            maiorLinha = novaLinha.copy()
                break
        self.copy(maiorLinha)
        
    def pontosProximos(self,ponto,exceptions = None):
        if exceptions is None:
            exceptions = []
        pontos = []
        for d in range(8):
            pontoAtual = coordDirecao(ponto,d)
            if pontoAtual in self:
                if pontoAtual not in exceptions:
                    if self.circular:
                        if abs(self.pontos.index(pontoAtual)-self.pontos.index(ponto)) < 5:
                            pontos.append(pontoAtual)
                    else:
                        pontos.append(pontoAtual)
        return pontos
        
    def divide(self,divisor,inicio):
        particoes = [0] * divisor
        for index in range(len(self)):
            particoes[index%divisor] += 1
        linhas = []
        for index in range(divisor):
            linha = Linha(circular = self.circular)
            inicioParticao = inicio + sum(particoes[:index])
            fimParticao = inicioParticao + particoes[index]
            for ponto in self.pontos[inicioParticao:fimParticao]:
                linha.append(ponto)
            if index == divisor-1:
                for ponto in self.pontos[:inicio]:
                    linha.append(ponto)
            linhas.append(linha)
        return linhas
        
    def melhorPonto(self):
        melhor = (float('inf'),float('inf'))
        for ponto in self.pontos:
            if ponto[1] < melhor[1]:
                melhor = ponto
            elif ponto[1] == melhor[1]:
                if ponto[0] < melhor[0]:
                    melhor = ponto
        return melhor

    def gira(self,novoInicio):
        if novoInicio in self:
            while self.pontos[0] != novoInicio:
                self.append(self.pontos[0])
                self.pontos.pop(0)
                self.inicio = self.pontos[0]
        
    def makeCamada(self):
        perimetro = len(self)
        tamanhoSeccao = int((perimetro-0.1)//4+1)
        if perimetro <= 4:
            camada = []
            for a in range(perimetro):
                camada.append(Linha([self.pontos[a]],circular = self.circular))
            while len(camada) != 4:
                camada.append(Linha([self.pontos[-1]],circular = self.circular))
            return camada
        camada = []
        melhorPontuacao = float('inf')
        for inicioSeccao in range(tamanhoSeccao):
            novaCamada = self.divide(4,inicioSeccao)
            maiorY = novaCamada[0].pontoMedio()[1]
            linhaDeBaixo = novaCamada[0]
            for n in range(1,4):
                if novaCamada[n].pontoMedio()[1] > maiorY:
                    maiorY = novaCamada[n].pontoMedio()[1]
                    linhaDeBaixo = novaCamada[n]
            while novaCamada[0] != linhaDeBaixo:
                novaCamada = [novaCamada[-1]] + novaCamada
                novaCamada.pop(-1)
            pontuacao = 0
            for a in range(4):
                if a%2==0:
                    pontuacao += abs(novaCamada[a].pontos[-1][1]-novaCamada[a].pontos[0][1])
                else:
                    pontuacao += abs(novaCamada[a].pontos[-1][0]-novaCamada[a].pontos[0][0])
            if pontuacao < melhorPontuacao:
                camada = novaCamada.copy()
                melhorPontuacao = pontuacao
        if camada[1].pontoMedio()[0] > camada[3].pontoMedio()[0]:
            novaCamada = [camada[a] for a in (0,3,2,1)]
            for linha in camada:
                linha.pontos = list(reversed(linha.pontos))
                linha.inicio = linha.pontos[0]
                linha.fim = linha.pontos[-1]
        else:
            novaCamada = camada
        return novaCamada
    
    def pontoMedio(self):
        x = 0
        y = 0
        for ponto in self.pontos:
            x += ponto[0]
            y += ponto[1]
        xmedio = x/len(self)
        ymedio = y/len(self)
        return (xmedio,ymedio)

    def escreve(self,other,file):
        if(len(self) == len(other)):
            for index in range(len(self)):
                file.write(str(self.pontos[index][0])+','+str(self.pontos[index][1]))
                file.write(' '+str(other.pontos[index][0])+','+str(other.pontos[index][1])+'\n')
        elif(len(self)>len(other)):
            if(len(self)-1==0):
                multiplicador = 0
            else:
                multiplicador = (len(other)-1)/(len(self)-1)
            for index in range(len(self)):
                pontoInicial = self.pontos[index]
                pontoFinal = other.pontos[int(index*multiplicador)]
                file.write(str(pontoInicial[0])+','+str(pontoInicial[1]))
                file.write(' '+str(pontoFinal[0])+','+str(pontoFinal[1])+'\n')
        else:
            if(len(other)-1==0):
                multiplicador = 0
            else:
                multiplicador = (len(self)-1)/(len(other)-1)
            for index in range(len(other)):
                pontoInicial = self.pontos[int(index*multiplicador)]
                pontoFinal = other.pontos[index]
                file.write(str(pontoInicial[0])+','+str(pontoInicial[1]))
                file.write(' '+str(pontoFinal[0])+','+str(pontoFinal[1])+'\n')
                
    def imprime(self,imagem): 
        transparencia = 255
        for ponto in self.pontos:
            imagem.putpixel(ponto,tuple([0,0,0,transparencia]))
            if transparencia > 80:
                transparencia -= 1
            else:
                transparencia = 255
        directory = "C:\\pythonscript\\imagem\\morphManual\\debug"
        name = f"{directory}\\{len(os.listdir(directory)):03d}.png"
        imagem.save(name)
                
    def copy(self,other = None):
        if other is None:
            return Linha(self.pontos,circular = self.circular)
        else:
            self.pontos = other.pontos
            self.inicio = other.inicio
            self.fim = other.fim
            self.circular = other.circular
        
    def append(self,elemento):
        if type(elemento) is Linha:
            for ponto in elemento.pontos:
                self.append(ponto)
        else:
            self.pontos.append(elemento)
            self.fim = elemento
            if self.inicio is None:
                self.inicio = elemento
        
    def __contains__(self,elemento):
        if elemento in self.pontos:
            return True
        return False
        
    def __add__(self,other):
        resultado = self.copy()
        if type(other) is list:
            resultado.pontos += other
            resultado.fim = other[-1]
        elif type(other) is Linha:
            resultado.pontos += other.pontos
            resultado.fim = other.fim
        return resultado
        
    def __len__(self):
        return len(self.pontos)
        
    def __str__(self):
        return str(self.pontos)
            
class Area:
    def __init__(self,imagem,linhaInicial = None):
        self.imagem = imagem
        self.linhas = []
        if linhaInicial is None:
            self.circular = True
            self.procuraContornoVerde()
        else:
            self.circular = False
            self.linhas.append(linhaInicial)
        self.procuraLinhas()

    def procuraContornoVerde(self):
        contorno = []
        largura,altura = self.imagem.size
        for y in range(altura):
            isUltimoPixelSolid = False
            for x in range(largura):
                isPixelAtualSolid = self.imagem.getpixel((x,y))[3]==255
                if((not isUltimoPixelSolid) and isPixelAtualSolid):
                    if((x,y) not in contorno):
                        contorno.append((x,y))
                if((not isPixelAtualSolid) and isUltimoPixelSolid):
                    if((x-1,y) not in contorno):
                        contorno.append((x-1,y))
                isUltimoPixelSolid = isPixelAtualSolid
            if isUltimoPixelSolid:
                if((x-1,y) not in contorno):
                    contorno.append((x-1,y))
        for x in range(largura):
            isUltimoPixelSolid = False
            for y in range(altura):
                isPixelAtualSolid = self.imagem.getpixel((x,y))[3]==255
                if((not isUltimoPixelSolid) and isPixelAtualSolid):
                    if((x,y) not in contorno):
                        contorno.append((x,y))
                if((not isPixelAtualSolid) and isUltimoPixelSolid):
                    if((x,y-1) not in contorno):
                        contorno.append((x,y-1))
                isUltimoPixelSolid = isPixelAtualSolid
            if isUltimoPixelSolid:
                if((x,y-1) not in contorno):
                    contorno.append((x,y-1))
        linhaInicial = Linha(contorno)
        linhaInicial.sortAll()
        camada = linhaInicial.makeCamada()
        linhaInicial = camada[0]
        for indice in range(1,4):
            linhaInicial.append(camada[indice])
        self.linhas.append(linhaInicial)

    def procuraLinhas(self):
        linhaAtual = Linha()
        linhaAnterior = self.linhas[-1]
        for coord in linhaAnterior.pontos:
            for direcao in (1,3,5,7):
                coordenada = coordDirecao(coord,direcao)
                try:
                    pixel = self.imagem.getpixel(coordenada)
                except:
                    continue
                if pixel[3] != 0 :
                    if coordenada not in linhaAtual:
                        if coordenada not in self:
                            linhaAtual.append(coordenada)
        if(len(linhaAtual)>0):
            linhaAtual.sortAll()
            self.linhas.append(linhaAtual)
            self.procuraLinhas()

    def imprimeArea(self,imagem):
        for linha in self:
            linhas = [linha]#separaLinha(linha)
            for linha in linhas:
                cor = tuple([randint(0,255) for a in range(3)])
                for coord in linha.pontos:
                    imagem.putpixel(coord,cor)
        path = "C:\\pythonscript\\imagem\\morphManual\\partesConfig"
        imagem.save(f"{path}\\debugArea{len(os.listdir(path)):03d}.png")
        
    def escreve(self,other,file):
        if(len(self) == len(other)):
            for self_linha,other_linha in zip(self.linhas, other.linhas):
                self_linha.escreve(other_linha,file)
        elif(len(self)>len(other)):
            if(len(self)-1 == 0):
                multiplicador = 0
            else:
                multiplicador = (len(other)-1)/(len(self)-1)
            for index in range(len(self)):
                linhaFinal = other.linhas[int(index*multiplicador)]
                self.linhas[index].escreve(linhaFinal,file)
        else:
            if(len(other)-1 == 0):
                multiplicador = 0
            else:
                multiplicador = (len(self)-1)/(len(other)-1)
            for index in range(len(other)):
                linhaInicial = self.linhas[int(index*multiplicador)]
                linhaInicial.escreve(other.linhas[index],file)

    def __contains__(self,other):
        for linha in self.linhas:
            if other in linha:
                return True
        return False
        
    def __len__(self):
        return len(self.linhas)

class AreaVermelha: #maybe add a separation for larger areas
    def __init__(self,imagem):
        self.imagem = imagem
        self.regioes = []
        self.procuraContornoVermelho()
        self.procuraCamadas()

    def procuraContornoVermelho(self):
        contorno = []
        largura,altura = self.imagem.size
        for y in range(altura):
            isUltimoPixelSolid = False
            for x in range(largura):
                isPixelAtualSolid = self.imagem.getpixel((x,y))[3]==255
                if((not isUltimoPixelSolid) and isPixelAtualSolid):
                    if((x,y) not in contorno):
                        contorno.append((x,y))
                if((not isPixelAtualSolid) and isUltimoPixelSolid):
                    if((x-1,y) not in contorno):
                        contorno.append((x-1,y))
                isUltimoPixelSolid = isPixelAtualSolid
            if isUltimoPixelSolid:
                if((x-1,y) not in contorno):
                    contorno.append((x-1,y))
        for x in range(largura):
            isUltimoPixelSolid = False
            for y in range(altura):
                isPixelAtualSolid = self.imagem.getpixel((x,y))[3]==255
                if((not isUltimoPixelSolid) and isPixelAtualSolid):
                    if((x,y) not in contorno):
                        contorno.append((x,y))
                if((not isPixelAtualSolid) and isUltimoPixelSolid):
                    if((x,y-1) not in contorno):
                        contorno.append((x,y-1))
                isUltimoPixelSolid = isPixelAtualSolid
            if isUltimoPixelSolid:
                if((x,y-1) not in contorno):
                    contorno.append((x,y-1))
        linhaInicial = Linha(contorno)
        linhaInicial.sort()
        camada = linhaInicial.makeCamada()
        for linha in camada:
            self.regioes.append([linha])

    def procuraCamadas(self):
        self.imprimeCamadas('nome')
        alterationDone = False
        for indice in [0,2,1,3]:
            linhaAtual = Linha(circular = True)
            linhaAnterior = self.regioes[indice][-1]
            for coord in linhaAnterior.pontos:
                for direcao in (1,3,5,7):
                    coordenada = coordDirecao(coord,direcao)
                    try:
                        pixel = self.imagem.getpixel(coordenada)
                    except:
                        continue
                    if pixel[3] != 0 :
                        if coordenada not in linhaAtual:
                            if coordenada not in self:
                                linhaAtual.append(coordenada)
            if(len(linhaAtual)>0):
                linhaAtual.sortAll()
                self.regioes[indice].append(linhaAtual)
                alterationDone = True
        if alterationDone:
            self.procuraCamadas()
            
    def imprimeRegioes(self,nome,indice): 
        for regiao in self.regioes:
            for linha in regiao:
                cor = [randint(0,255) for a in range(3)]
                transparencia = 255
                for coord in linha.pontos:
                    self.imagem.putpixel(coord,tuple(cor+[transparencia]))
                    if transparencia:
                        transparencia -= 1
        self.imagem.save(f"C:\\pythonscript\\imagem\\morphManual\\debug\\{indice:03d}" + nome + ".png")

    def imprimeCamadas(self,nome): 
        maximoLinhas = self.tamanhoMaiorRegiao()
        for indice in range(maximoLinhas):
            transparencia = 255
            for regiao in self.regioes:
                if indice < len(regiao):
                    linha = regiao[indice]
                    cor = [randint(0,255) for a in range(3)]
                    for coord in linha.pontos:
                        self.imagem.putpixel(coord,tuple(cor+[transparencia]))
                        if transparencia > 80:
                            transparencia -= 1
                        else:
                            transparencia = 255
        directory = "C:\\pythonscript\\imagem\\morphManual\\debug"
        name = directory 
        index = sum([1 if file.find(nome)!=-1 else 0 for file in os.listdir(directory)])
        name += f"\\{index:03d}"
        name += nome + ".png"
        self.imagem.save(name)
        
    def escreve(self,other,file): 
        for indice in range(4):
            if(len(self.regioes[indice]) == len(other.regioes[indice])):
                for self_regiao,other_regiao in zip(self.regioes[indice], other.regioes[indice]):
                    self_regiao.escreve(other_regiao,file)
            elif(len(self.regioes[indice])>len(other.regioes[indice])):
                if(len(self.regioes[indice])-1 == 0):
                    multiplicador = 0
                else:
                    multiplicador = (len(other.regioes[indice])-1)/(len(self.regioes[indice])-1)
                for index in range(len(self.regioes[indice])):
                    linhaFinal = other.regioes[indice][int(index*multiplicador)]
                    self.regioes[indice][index].escreve(linhaFinal,file)
            else:
                if(len(other.regioes[indice])-1 == 0):
                    multiplicador = 0
                else:
                    multiplicador = (len(self.regioes[indice])-1)/(len(other.regioes[indice])-1)
                for index in range(len(other.regioes[indice])):
                    linhaInicial = self.regioes[indice][int(index*multiplicador)]
                    linhaInicial.escreve(other.regioes[indice][index],file)

    def __contains__(self,other): 
        for regiao in self.regioes:
            for linha in regiao:
                if other in linha:
                    return True
        return False
        
    def __len__(self):
        return len(self.camadas)
        
    def tamanhoMaiorRegiao(self):
        tamanho = float('-inf')
        for regiao in self.regioes:
            if len(regiao) > tamanho:
                tamanho = len(regiao)
        return tamanho

class ImagemParte:
    def __init__(self,nome):
        imagem = Image.open(nome)
        self.hasColor(imagem)
        if self.hasRed:
            self.area = AreaVermelha(imagem)
        elif self.hasBlue:
            linha = Linha([self.hasBlue])
            linha.procuraLinhaAzul(imagem)
            self.area = Area(imagem,linhaInicial = linha)
        else:
            self.area = Area(imagem)
        imagem.close()
        
    
    def hasColor(self,imagem):
        largura,altura = imagem.size
        self.hasRed = False
        self.hasBlue = False
        for x in range(largura):
            for y in range(altura):
                pixel = imagem.getpixel((x,y))
                if(pixel[3] == 0):
                    continue
                if(pixel[0] == 255):
                    self.hasRed = True
                    break
                if(pixel[2] == 200):
                    self.hasBlue = (x,y)
                    break
            if self.hasBlue or self.hasRed:
                break
        
    def escreveArea(self,other,file):
        self.area.escreve(other.area,file)

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

def distancia(pontoA,pontoB):
    soma = 0
    for coord_a,coord_b in zip(pontoA, pontoB):
        soma += abs(coord_a - coord_b)**2
    return soma**(1/2)

def configPart(indice):
    print("Fazendo Parte : " + str(indice))
    parteInicial = ImagemParte(f"C:\\pythonscript\\imagem\\morphManual\\partes\\iniciais\\{indice:03d}.png")
    parteFinal = ImagemParte(f"C:\\pythonscript\\imagem\\morphManual\\partes\\finais\\{indice:03d}.png")
    fileConfig = open(f'C:\\pythonscript\\imagem\\morphManual\\partes\\config\\{indice:03d}.txt','w')
    parteInicial.escreveArea(parteFinal,fileConfig)
    print("\tParte Terminada : " + str(indice))
    fileConfig.close()
        
if __name__ == '__main__':
    quantiaPartes = len(os.listdir("C:\\pythonscript\\imagem\\morphManual\\partes\\finais"))
    p = multiprocessing.Pool(os.cpu_count())
    p.map(configPart,range(quantiaPartes))
