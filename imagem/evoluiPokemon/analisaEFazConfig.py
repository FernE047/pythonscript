from PIL import Image
import os
import multiprocessing
from random import randint
from time import sleep

class Linha:
    def __init__(self,pontos = None,circular = False):
        if pontos is None:
            self.pontos = []
        else:
            self.pontos = pontos.copy()
        self.circular = circular
    
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
                for index in linhasQueTemOPonto[1:] :
                    superLinha += linhas[index]
                for index in reversed(sorted(linhasQueTemOPonto)):
                    linhas.pop(index)
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
            for self_ponto,other_ponto in zip(self,other):
                file.write(str(self_ponto[0])+','+str(self_ponto[1]))
                file.write(' '+str(other_ponto[0])+','+str(other_ponto[1])+'\n')
        elif(len(self)>len(other)):
            if(len(self)-1==0):
                multiplicador = 0
            else:
                multiplicador = (len(other)-1)/(len(self)-1)
            for n in range(len(self)):
                pontoInicial = self.pontos[n]
                pontoFinal = other.pontos[int(n*multiplicador)]
                file.write(str(pontoInicial[0])+','+str(pontoInicial[1]))
                file.write(' '+str(pontoFinal[0])+','+str(pontoFinal[1])+'\n')
        else:
            if(len(other)-1==0):
                multiplicador = 0
            else:
                multiplicador = (len(self)-1)/(len(other)-1)
            for n in range(len(other)):
                pontoInicial = self.pontos[int(n*multiplicador)]
                pontoFinal = other.pontos[n]
                file.write(str(pontoInicial[0])+','+str(pontoInicial[1]))
                file.write(' '+str(pontoFinal[0])+','+str(pontoFinal[1])+'\n')
                
    def copy(self,other = None):
        if other is None:
            return Linha(self.pontos,circular = self.circular)
        else:
            self.pontos = other.pontos
            self.circular = other.circular
        
    def append(self,elemento):
        if type(elemento) is Linha:
            for ponto in elemento.pontos:
                self.append(ponto)
        else:
            self.pontos.append(elemento)
        
    def __contains__(self,elemento):
        if elemento in self.pontos:
            return True
        return False
        
    def __add__(self,other):
        resultado = self.copy()
        if type(other) is list:
            resultado.pontos += other
        elif type(other) is Linha:
            resultado.pontos += other.pontos
        return resultado
        
    def __len__(self):
        return len(self.pontos)
        
    def __str__(self):
        return str(self.pontos)

class Area:
    def __init__(self,imagem):
        self.imagem = imagem
        self.regioes = []
        self.procuraContorno()
        self.procuraCamadas()

    def procuraContorno(self):
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
                for n in range(len(self.regioes[indice])):
                    linhaFinal = other.regioes[indice][int(n*multiplicador)]
                    self.regioes[indice][n].escreve(linhaFinal,file)
            else:
                if(len(other.regioes[indice])-1 == 0):
                    multiplicador = 0
                else:
                    multiplicador = (len(self.regioes[indice])-1)/(len(other.regioes[indice])-1)
                for n in range(len(other.regioes[indice])):
                    linhaInicial = self.regioes[indice][int(n*multiplicador)]
                    linhaInicial.escreve(other.regioes[indice][n],file)

    def __contains__(self,other): 
        for regiao in self.regioes:
            for linha in regiao:
                if other in linha:
                    return True
        return False
        
    def tamanhoMaiorRegiao(self):
        tamanho = float('-inf')
        for regiao in self.regioes:
            if len(regiao) > tamanho:
                tamanho = len(regiao)
        return tamanho

class ImagemParte:
    def __init__(self,nome):
        imagem = Image.open(nome)
        self.area = Area(imagem)
        imagem.close()
        
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
    for coord_a,coord_b in zip(pontoA,pontoB):
        soma += abs(coord_a-coord_b)**2
    return soma**(1/2)
        
if __name__ == '__main__':
    print("Fazendo Analise : " + str(0))
    parteInicial = Image.open("C:\\pythonscript\\imagem\\evoluiPokemon\\inicial.png")
    areaInicial = Area(parteInicial)
    parteInicial.close()
    parteFinal = Image.open("C:\\pythonscript\\imagem\\evoluiPokemon\\final.png")
    areaFinal = Area(parteFinal)
    parteFinal.close()
    fileConfig = open('C:\\pythonscript\\imagem\\evoluiPokemon\\config.txt','w')
    areaInicial.escreve(areaFinal,fileConfig)
    print("\Analise Terminada : " + str(0))
    fileConfig.close()
