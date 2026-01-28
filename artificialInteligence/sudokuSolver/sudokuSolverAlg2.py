from typing import Literal, overload
from userUtil import pegaString as pS
from time import time
from textos import embelezeTempo
import os


def tiraEspaçoBranco(texto: str) -> str:
    for espaco in [" ", "\n", "\t"]:
        if espaco in texto:
            texto = texto.replace(espaco, "")
    return texto


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

class Tabuleiro:
    def __init__(self, confInicial=0):
        self.matrizTab=[]
        for a in range(9):
            self.matrizTab.append([0,0,0,0,0,0,0,0,0])
        if(confInicial):
            confLimpa = tiraEspaçoBranco(confInicial)
            for a,valor in enumerate(list(confLimpa)):
                if(a>80):
                    break
                posY=a//9
                posX=a%9
                self.setElement(posY,posX,valor)

    def delElement(self,y,x):
        self.matrizTab[y][x]='0'

    def getElement(self,y,x):
        return self.matrizTab[y][x]

    def verificaValorQuadrante(self,y,x,v):
        yQuad=y//3
        xQuad=x//3
        for y in range(3):
            for x in range(3):
                if(self.getElement(3*yQuad+y,3*xQuad+x)==v):
                    return False
        return True

    def verificaValorLinha(self,y,v):
        for x in range(9):
            if(self.getElement(y,x)==v):
                return False
        return True

    def verificaValorColuna(self,x,v):
        for y in range(9):
            if(self.getElement(y,x)==v):
                return False
        return True

    def verificaQuadrante(self,y,x):
        yQuad=y//3
        xQuad=x//3
        tabuleiro=self.copia()
        for y in range(3):
            for x in range(3):
                v=tabuleiro.getElement(a,b)
                tabuleiro.setElement(3*yQuad+y,3*xQuad+x,'0')
                if(not(tabuleiro.setElement(a,b,v))):
                    return False
        return True

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
        for y in range(9):
            v = tabuleiro.getElement(y,x)
            tabuleiro.setElement(y,x,'0')
            if(not(tabuleiro.setElement(y,x,v))):
                return False
        return True

    def verificaLinha(self,y):
        tabuleiro=self.copia()
        for x in range(9):
            v=tabuleiro.getElement(y,x)
            tabuleiro.setElement(y,x,'0')
            if(not(tabuleiro.setElement(y,x,v))):
                return False
        return True

    def verificaTabuleiro(self):
        tabuleiro = self.copia()
        for y in range(9):
            for x in range(9):
                v = tabuleiro.getElement(y,x)
                if(v=='0'):
                    return False
                tabuleiro.setElement(y,x,'0')
                if(not(tabuleiro.setElement(y,x,v))):
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
        self.delElement(y,x)
        if v in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            if(v=='0'):
                return True
            else:
                if(self.verificaValor(y,x,v)):
                    self.matrizTab[y][x]=v
                    return True
        return False

    def proximoEspaco(self):
        for y in range(9):
            for x in range(9):
                if(self.getElement(y,x)=='0'):
                    return((y,x))

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
    global tries
    if(tabuleiro.verificaTabuleiro()):
        return tabuleiro
    else:
        espacoVazio=tabuleiro.proximoEspaco()
        if(espacoVazio):
            for value in range(1,10):
                if(tabuleiro.setElement(espacoVazio[0],espacoVazio[1],str(value))):
                    tries += 1
                    solucao = resolveTabuleiro(tabuleiro)
                    if(solucao):
                        return solucao
            tabuleiro.delElement(espacoVazio[0],espacoVazio[1])

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
        inicioTotal = time()
        files = os.listdir('sudokus')
        for name in files:
            print(name,end='\n\n')
            sudoku = open('sudokus//'+name)
            tabuleiro = Tabuleiro(sudoku.read())
            resolveUmTabuleiro(tabuleiro)
        fimTotal = time()
        print('\n'+embelezeTempo(fimTotal-inicioTotal)+'\n\n\n')
    else:
        tabuleiro = criaTabuleiro(mode)
        resolveUmTabuleiro(tabuleiro)
