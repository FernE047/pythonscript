from typing import Literal, overload
from userUtil import pegaString as pS
from textos import tiraEspacoBranco as tEB
from time import time
from textos import embelezeTempo
import os




@overload
def choose_from_options(
    prompt: str, options: list[str], mode: Literal["text"]
) -> str: ...


@overload
def choose_from_options(
    prompt: str, options: list[str], mode: Literal["number"]
) -> int: ...


def choose_from_options(
    prompt: str, options: list[str], mode: Literal["text", "number"] = "text"
) -> str | int:
    while True:
        for i, option in enumerate(options):
            print(f"{i} - {option}")
        user_choice = input(prompt)
        try:
            if mode == "number":
                return int(user_choice)
            else:
                return options[int(user_choice)]
        except (ValueError, IndexError):
            user_choice = input("not valid, try again: ")

class Quadrante:
    def __init__(self,confInicial='0'):
        self.matrizQuad=[]
        for a in range(3):
            self.matrizQuad.append(['0','0','0'])
        if(confInicial!='0'):
            for a,b in enumerate(list(confInicial)):
                self.matrizQuad[a//3][a%3]=b                   
    def delElement(self,y,x):
        self.matrizQuad[y][x]='0'

    def getElement(self,y,x):
        return self.matrizQuad[y][x]

    def verificaValor(self,v):
        for a in range(3):
            for b in range(3):
                if(self.matrizQuad[a][b]==v):
                    return False
        return True

    def setElement(self,y,x,valor):
        if valor in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            if(valor=='0'):
                self.matrizQuad[y][x]='0'
                return True
            else:
                if(self.verificaValor(valor)):
                    self.matrizQuad[y][x]=valor
                    return True
        return False

    def viraConfig(self):
        chave=''
        for a in range(3):
            for b in range(3):
                chave+=self.getElement(a,b)
        return chave

    def copia(self):
        return Quadrante(self.viraConfig)

    def verificaQuadrante(self):
        quadrante=self.copia
        for a in range(3):
            for b in range(3):
                v=quadrante.getElement(a,b)
                quadrante.setElement(a,b,'0')
                if(not(quadrante.setElement(a,b,v))):
                    return False
        return True
        
class Tabuleiro:
    def __init__(self, confInicial=0):
        self.matrizTab=[]
        for a in range(3):
            self.matrizTab.append([Quadrante(),Quadrante(),Quadrante()])
        if(confInicial):
            confLimpa = tEB(confInicial,tiraTudo=True)
            for a,valor in enumerate(list(confLimpa)):
                if(a>80):
                    break
                posY=a//9
                posX=a%9
                self.setElement(posY,posX,valor)

    def transformaPos(self,y=0,x=0):
        posYTab=y//3
        posXTab=x//3
        posYQuad=y%3
        posXQuad=x%3
        return [posYTab,posXTab,posYQuad,posXQuad]

    def getQuadrante(self,y,x):
        return(self.matrizTab[y][x])

    def delElement(self,y,x):
        posYTab,posXTab,posYQuad,posXQuad = self.transformaPos(y,x)
        self.getQuadrante(posYTab,posXTab).delElement(posYQuad,posXQuad)

    def getElement(self,y,x):
        posYTab,posXTab,posYQuad,posXQuad = self.transformaPos(y,x)
        return self.getQuadrante(posYTab,posXTab).getElement(posYQuad,posXQuad)

    def verificaValorQuadrante(self,y,x,v):
        posYTab,posXTab,posYQuad,posXQuad = self.transformaPos(y,x)
        return self.getQuadrante(posYTab,posXTab).verificaValor(v)

    def verificaValorLinha(self,y,v):
        posYTab,posXTab,posYQuad,posXQuad = self.transformaPos(y=y)
        for a in range(3):
            quadrante=self.getQuadrante(posYTab,a)
            for b in range(3):
                if(quadrante.matrizQuad[posYQuad][b]==v):
                    return False
        return True

    def verificaValorColuna(self,x,v):
        posYTab,posXTab,posYQuad,posXQuad = self.transformaPos(x=x)
        for a in range(3):
            quadrante=self.getQuadrante(a,posXTab)
            for b in range(3):
                if(quadrante.matrizQuad[b][posXQuad]==v):
                    return False
        return True

    def verificaQuadrante(self,y,x):
        posYTab,posXTab,posYQuad,posXQuad = self.transformaPos(y,x)
        return self.getQuadrante(posYTab,posXTab).verificaQuadrante()

    def viraConfig(self):
        chave=''
        for a in range(9):
            for b in range(9):
                chave += self.getElement(a,b)
        return chave

    def copia(self):
        return Tabuleiro(self.viraConfig())

    def verificaColuna(self,x):
        tabuleiro=self.copia()
        for a in range(9):
            v=tabuleiro.getElement(a,x)
            tabuleiro.setElement(a,x,'0')
            if(not(tabuleiro.setElement(a,x,v))):
                return False
        return True

    def verificaLinha(self,y):
        tabuleiro=self.copia()
        for a in range(9):
            v=tabuleiro.getElement(y,a)
            tabuleiro.setElement(y,a,'0')
            if(not(tabuleiro.setElement(y,a,v))):
                return False
        return True

    def verificaTabuleiro(self):
        tabuleiro = self.copia()
        for a in range(9):
            for b in range(9):
                v = tabuleiro.getElement(a,b)
                if(v=='0'):
                    return False
                tabuleiro.setElement(a,b,'0')
                if(not(tabuleiro.setElement(a,b,v))):
                    return False
        return True

    def verificaValor(self,y,x,v):
        if(not(self.verificaValorQuadrante(y,x,v))):
            return False
        if(not(self.verificaValorColuna(x,v))):
            return False
        if(not(self.verificaValorLinha(y,v))):
            return False
        return True

    def setElement(self,y,x,v):
        posYTab,posXTab,posYQuad,posXQuad = self.transformaPos(y,x)
        quadrante=self.getQuadrante(posYTab,posXTab)
        if v in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            if(v=='0'):
                quadrante.setElement(posYQuad,posXQuad,'0')
                return True
            else:
                if(self.verificaValor(y,x,v)):
                    quadrante.setElement(posYQuad,posXQuad,v)
                    return True
        return False

    def proximoEspaco(self):
        for y in range(9):
            for x in range(9):
                if(self.getElement(y,x)=='0'):
                    return((y,x))

    def possibilidadesEspaco(self,pos):
        possibilidades = []
        for value in range(1,10):
            if(self.verificaValor(pos[0],pos[1],str(value))):
                possibilidades.append(str(value))
        return possibilidades

    def imprime(self):
        for y in range(9):
            for x in range(9):
                print(self.getElement(y,x),end='')
            print()

def criaTabuleiro(mode):
    if(mode==2):
        nome = pS('qual o nome do arquivo?')
        sudokuFile = open(nome+'.txt')
        tabuleiro = Tabuleiro(sudokuFile.read())
        return tabuleiro
    else:
        tabuleiro = Tabuleiro()
        quantia = 0
        while quantia<81:
            inputConfig=pS('')
            for v in inputConfig:
                posY=quantia//9
                posX=quantia%9
                if v in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                    if(tabuleiro.setElement(posY,posX,v)):
                        print('elemento '+v+' adicionado')
                        quantia+=1
                    else:
                        print('elemento '+v+' não adicionado')
                        break
                else:
                    if(v=='p'):
                        if(quantia>0):
                            quantia-=1
                            posY=quantia//9
                            posX=quantia%9
                            print('numero '+tabuleiro.getElement(posY,posX)+' apagado')
                            tabuleiro.delElement(posY,posX)
                    elif(v=='l'):
                        pass #apagar linha atual
                    elif(v=='L'):
                        pass #apagar uma linha
                    elif(v=='c'):
                        pass #apagar coluna atual
                    elif(v=='C'):
                        pass #apagar uma coluna
                    elif(v=='q'):
                        pass #apagar quadrante atual
                    elif(v=='Q'):
                        pass #apagar um quadrante
                    elif(v=='o'):
                        print('entrada completamente apagada')
                        tabuleiro = Tabuleiro()
                        quantia=0
                    elif(v=='s'):
                        tabuleiro.imprime()
                    elif(v=='e'):
                        return tabuleiro
                    else:
                        print('digite um numero entre 0 e 9 ou opcoes adicionais')
                        config +='0'
            print()
            tabuleiro.imprime()
        return tabuleiro

def resolveTabuleiro(tabuleiro):
    #tabuleiro.imprime()
    global tries
    if(tabuleiro.verificaTabuleiro()):
        return tabuleiro
    else:
        espacoVazio=tabuleiro.proximoEspaco()
        #print(espacoVazio)
        if(espacoVazio):
            possibilidades=tabuleiro.possibilidadesEspaco(espacoVazio)
            #print(possibilidades)
            for possibilidade in possibilidades:
                filho = tabuleiro.copia()
                filho.setElement(espacoVazio[0],espacoVazio[1],possibilidade)
                tries += 1
                solucao = resolveTabuleiro(filho)
                if(solucao):
                    return solucao

def resolveUmTabuleiro(tabuleiro):
    tabuleiro.imprime()
    print()
    global tries
    tries=0
    inicio = time()
    solucao = resolveTabuleiro(tabuleiro)
    solucao.imprime()
    fim = time()
    print('\ntentativas: '+str(tries))
    print('\n'+embelezeTempo(fim-inicio)+'\n\n\n')

while True:
    mode = choose_from_options('escolha uma opcao:',['sair','Input Manual','Import Sudoku Txt','Loop Import Folder'],'number')
    if(mode==0):
        break
    if(mode==3):
        files = os.listdir('sudokus')
        for name in files:
            print(name,end='\n\n')
            sudoku = open('sudokus//'+name)
            tabuleiro = Tabuleiro(sudoku.read())
            resolveUmTabuleiro(tabuleiro)
    else:
        tabuleiro = criaTabuleiro(mode)
        resolveUmTabuleiro(tabuleiro)
