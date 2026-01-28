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

class Tabuleiro:
    def __init__(self, confInicial=0):
        self.matriz=[]
        self.espacosVazios=[]
        for y in range(9):
            self.matriz.append([0,0,0,0,0,0,0,0,0])
        if(confInicial):
            confLimpa = tEB(confInicial,tiraTudo=True)
            for a,valor in enumerate(list(confLimpa)):
                if(a>80):
                    break
                posY=a//9
                posX=a%9
                self.setElement(posY,posX,valor)
                if(valor=='0'):
                    self.espacosVazios=[(posY,posX)]+self.espacosVazios
        else:
            self.espacosVazios=[(y,x) for x in range(9,0,-1)]+self.espacosVazios

    def verificaValor(self,y,x,v):
        yQuad=y//3
        xQuad=x//3
        for a in range(3):
            for b in range(3):
                if(self.matriz[3*yQuad+a][3*xQuad+b]==v):
                    return False
        if(yQuad==0):
            for a in range(3,9):
                if(self.matriz[a][x]==v):
                    return False
        elif(yQuad==2):
            for a in range(0,6):
                if(self.matriz[a][x]==v):
                    return False
        else:
            for a in range(3):
                if(self.matriz[a][x]==v):
                    return False
            for a in range(6,9):
                if(self.matriz[a][x]==v):
                    return False
        if(xQuad==0):
            for b in range(3,9):
                if(self.matriz[y][b]==v):
                    return False
        elif(xQuad==2):
            for b in range(0,6):
                if(self.matriz[y][b]==v):
                    return False
        else:
            for b in range(3):
                if(self.matriz[y][b]==v):
                    return False
            for b in range(6,9):
                if(self.matriz[y][b]==v):
                    return False
        return True

    def viraConfig(self):
        chave=''
        for y in range(9):
            for x in range(9):
                chave += self.matriz[y][x]
        return chave

    def copia(self):
        return Tabuleiro(self.viraConfig())

    def setElement(self,y,x,v):
        self.matriz[y][x]='0'
        if v in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            if(v=='0'):
                return True
            else:
                if(self.verificaValor(y,x,v)):
                    self.matriz[y][x]=v
                    return True
        return False

    def imprime(self):
        for y in range(9):
            for x in range(9):
                print(self.matriz[y][x],end='')
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
                            print('numero '+tabuleiro.matriz[posY][posX]+' apagado')
                            tabuleiro.matriz[posY][posX]='0'
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
    if(tabuleiro.espacosVazios):
        espacoVazio = tabuleiro.espacosVazios.pop(-1)
        if(espacoVazio):
            global tries
            for value in range(1,10):
                if(tabuleiro.setElement(espacoVazio[0],espacoVazio[1],str(value))):
                    tries += 1
                    solucao = resolveTabuleiro(tabuleiro)
                    if(solucao):
                        return solucao
            tabuleiro.matriz[espacoVazio[0]][espacoVazio[1]]='0'
            tabuleiro.espacosVazios.append(espacoVazio)
    else:
        return tabuleiro

def resolveUmTabuleiro(tabuleiro):
    tabuleiro.imprime()
    print()
    global tries
    tries=0
    inicio = time()
    solucao = resolveTabuleiro(tabuleiro)
    fim = time()
    solucao.imprime()
    print('\ntentativas: '+str(tries))
    tempo = fim-inicio
    global tempoTotal
    tempoTotal += tempo
    print('\n'+embelezeTempo(tempo)+'\n\n\n')

while True:
    mode = choose_from_options('escolha uma opcao:',['sair','Input Manual','Import Sudoku Txt','Loop Import Folder'],'number')
    if(mode==0):
        break
    if(mode==3):
        global tempoTotal
        tempoTotal = 0
        files = os.listdir('sudokus')
        for name in files:
            print(name,end='\n\n')
            sudoku = open('sudokus//'+name)
            tabuleiro = Tabuleiro(sudoku.read())
            resolveUmTabuleiro(tabuleiro)
        print('\n'+embelezeTempo(tempoTotal)+'\n\n\n')
    else:
        tabuleiro = criaTabuleiro(mode)
        resolveUmTabuleiro(tabuleiro)
