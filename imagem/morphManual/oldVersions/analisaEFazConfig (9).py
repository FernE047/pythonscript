from PIL import Image
import os
import pypdn
import multiprocessing
from random import randint

class Linha:
    def __init__(self,pontos = None):
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
            for n in range(len(linhas)):
                novaLinha = linhas[n]
                for novoPonto in novaLinha.pontos:
                    if distancia(ponto,novoPonto) <= 2**(1/2)+0.01:
                        linhasQueTemOPonto.append(n)
                        break
            if len(linhasQueTemOPonto) == 0:
                linhas.append(Linha([ponto]))
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
        maiorLinha = Linha()
        for n in range(tamanho):
            linhaTeste = self.copy()
            primeiroPonto = self.pontos[n]
            linhaTeste.sortIt(Linha([primeiroPonto]))
            if len(linhaTeste) == tamanho:
                maiorLinha = linhaTeste.copy()
                break
            if len(linhaTeste) > len(maiorLinha):
                maiorLinha = linhaTeste.copy()
        self.copy(maiorLinha)

    def sortIt(self, linhaOrdenada):
        while True:
            pontoInicial = linhaOrdenada.fim
            pontos = []
            for d in range(8):
                pontoAtual = coordDirecao(pontoInicial,d)
                if pontoAtual in self:
                    if pontoAtual not in linhaOrdenada:
                        pontos.append(pontoAtual)
            if len(pontos) == 1:
                linhaOrdenada.append(pontos[0])
            else:
                for ponto in pontos:
                    novaLinha = self.copy()
                    novaLinha.sortIt(linhaOrdenada + [ponto])
                    if len(novaLinha) == len(self):
                        linhaOrdenada = novaLinha.copy()
                        break
                    if len(novaLinha) > len(linhaOrdenada):
                        linhaOrdenada = novaLinha.copy()
                break
        self.copy(linhaOrdenada)
        
    def divide(self,divisor,inicio):
        particoes = [0] * divisor
        for n in range(len(self)):
            particoes[n%divisor] += 1
        linhas = []
        for n in range(divisor):
            linha = Linha()
            inicioParticao = inicio + sum(particoes[:n])
            fimParticao = inicioParticao + particoes[n]
            for ponto in self.pontos[inicioParticao:fimParticao]:
                linha.append(ponto)
            if n == divisor-1:
                for ponto in self.pontos[:inicio]:
                    linha.append(ponto)
            linhas.append(linha)
        return linhas

    def escreve(self,other,file):
        if(len(self) == len(other)):
            for n in range(len(self)):
                file.write(str(self.pontos[n][0])+','+str(self.pontos[n][1]))
                file.write(' '+str(other.pontos[n][0])+','+str(other.pontos[n][1])+'\n')
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
            return Linha(self.pontos)
        else:
            self.pontos = other.pontos
            self.inicio = other.inicio
            self.fim = other.fim
        
    def append(self,elemento):
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
            self.procuraContornoVerde()
        else:
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
                    if pixel[1] == 255 :
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
        imagem.save("C:\\pythonscript\\imagem\\morphManual\\partesConfig\\debugArea{0:03d}.png".format(len(os.listdir('C:\\pythonscript\\imagem\\morphManual\\partesConfig'))))
        
    def escreve(self,other,file):
        if(len(self) == len(other)):
            for n in range(len(self)):
                self.linhas[n].escreve(other.linhas[n],file)
        elif(len(self)>len(other)):
            if(len(self)-1 == 0):
                multiplicador = 0
            else:
                multiplicador = (len(other)-1)/(len(self)-1)
            for n in range(len(self)):
                linhaFinal = other.linhas[int(n*multiplicador)]
                self.linhas[n].escreve(linhaFinal,file)
        else:
            if(len(other)-1 == 0):
                multiplicador = 0
            else:
                multiplicador = (len(self)-1)/(len(other)-1)
            for n in range(len(other)):
                linhaInicial = self.linhas[int(n*multiplicador)]
                linhaInicial.escreve(other.linhas[n],file)

    def __contains__(self,other):
        for linha in self.linhas:
            if other in linha:
                return True
        return False
        
    def __len__(self):
        return len(self.linhas)

class ImagemParte:
    def __init__(self,indice,nome):
        image = convertePypdnToPil(nome)
        azul = self.azulInicial(imagem)
        if azul:
            linha = Linha([azul])
            linha.procuraLinhaAzul(imagem)
            self.area = Area(imagem,linhaInicial = linha)
        else:
            self.area = Area(imagem,nome[-9:-4])
        imagem.close()
        
    def azulInicial(self,imagem):
        largura,altura = imagem.size
        for x in range(largura):
            for y in range(altura):
                pixel = imagem.getpixel((x,y))
                if(pixel[3] == 0):
                    continue
                if(pixel[2] == 200):
                    return (x,y)
        return False
        
    def escreveArea(self,other,file):
        self.area.escreve(other.area,file)

def limpaPasta(pasta):
    arquivos = [pasta+'\\'+a for a in os.listdir(pasta)]
    if('C:\\pythonscript\\imagem\\morphManual\\frames\\resized' in arquivos):
        arquivos.pop(arquivos.index('C:\\pythonscript\\imagem\\morphManual\\frames\\resized'))
    for arquivo in arquivos:
        os.remove(arquivo)

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
    for n in range(len(pontoA)):
        soma += abs(pontoA[n]-pontoB[n])**2
    return soma**(1/2)
    
def convertePypdnToPil(nome):
    layeredImage = pypdn.read(nome)
    imageLayer = layeredImage.layers[indice]
    imageArray = imageLayer.image
    imagem = Image.fromarray(imageArray)
    layeredImage = imageLayer = imageArray = None
    return imagem
    
def configPart(indice):
    print("Fazendo Parte : " + str(indice))
    parteInicial = ImagemParte(indice,"C:\\pythonscript\\imagem\\morphManual\\inicial.pdn")
    print("a")
    parteFinal = ImagemParte(indice,"C:\\pythonscript\\imagem\\morphManual\\final.pdn")
    print("b")
    fileConfig = open('C:\\pythonscript\\imagem\\morphManual\\partesConfig\\parte{0:02d}Config.txt'.format(indice),'w')
    print("c")
    parteInicial.escreveArea(parteFinal,fileConfig)
    print("\tParte Terminada : " + str(indice))
    fileConfig.close()
        
if __name__ == '__main__':
    limpaPasta('C:\\pythonscript\\imagem\\morphManual\\partesConfig')
    limpaPasta('C:\\pythonscript\\imagem\\morphManual\\frames')
    limpaPasta('C:\\pythonscript\\imagem\\morphManual\\frames\\resized')
    limpaPasta('C:\\pythonscript\\imagem\\morphManual\\debug')
    imagemInicial = pypdn.read("C:\\pythonscript\\imagem\\morphManual\\inicial.pdn")
    imagemFinal = pypdn.read("C:\\pythonscript\\imagem\\morphManual\\final.pdn")
    Image.fromarray(imagemInicial.layers[0].image).save("inicial.png")
    Image.fromarray(imagemFinal.layers[0].image).save("final.png")
    quantiaPartes = len(imagemInicial.layers)
    imagemInicial = None
    imagemFinal = None
    for a in range(2,quantiaPartes):
        configPart(a)
    #p = multiprocessing.Pool(os.cpu_count())
    #p.map(configPart,range(2,quantiaPartes))