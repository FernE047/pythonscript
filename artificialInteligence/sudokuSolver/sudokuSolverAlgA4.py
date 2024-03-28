from textos import tiraEspacoBranco as tEB
from time import time
from textos import embelezeTempo
import os

def criaTabuleiro(config):
    matriz = []
    espacosVazios = []
    tabuleiro = [matriz,espacosVazios]
    for y in range(9):
        tabuleiro[0].append(['0','0','0','0','0','0','0','0','0'])
    confLimpa = tEB(config,tiraTudo = True)
    for a,valor in enumerate(list(confLimpa)):
        if(a>80):
            break
        posY = a//9
        posX = a%9
        tabuleiro[0][posY][posX] = valor
        if(valor == '0'):
            tabuleiro[1]=[(posY,posX)]+tabuleiro[1]
    return tabuleiro

def possibilidades(tabuleiro,y,x):
        yQuad=(y//3)*3
        xQuad=(x//3)*3
        lista=['1','2','3','4','5','6','7','8','9']
        tabuleiro[0][y][x]='0'
        for a in range(3):
            for b in range(3):
                v = tabuleiro[0][yQuad+a][xQuad+b]
                if(v in lista):
                    lista.remove(v)
        if(yQuad==0):
            for a in range(3,9):
                v = tabuleiro[0][a][x]
                if(v in lista):
                    lista.remove(v)
        elif(yQuad==6):
            for a in range(0,6):
                v = tabuleiro[0][a][x]
                if(v in lista):
                    lista.remove(v)
        else:
            for a in range(3):
                v = tabuleiro[0][a][x]
                if(v in lista):
                    lista.remove(v)
            for a in range(6,9):
                v = tabuleiro[0][a][x]
                if(v in lista):
                    lista.remove(v)
        if(not(lista)):
            return lista
        if(xQuad==0):
            for b in range(3,9):
                v = tabuleiro[0][y][b]
                if(v in lista):
                    lista.remove(v)
        elif(xQuad==6):
            for b in range(0,6):
                v = tabuleiro[0][y][b]
                if(v in lista):
                    lista.remove(v)
        else:
            for b in range(3):
                v = tabuleiro[0][y][b]
                if(v in lista):
                    lista.remove(v)
            for b in range(6,9):
                v = tabuleiro[0][y][b]
                if(v in lista):
                    lista.remove(v)
        return lista

def resolveTabuleiro(tabuleiro):
    if(tabuleiro[1]):
        espacoVazio = tabuleiro[1].pop(-1)
        global tries
        for value in possibilidades(tabuleiro,espacoVazio[0],espacoVazio[1]):
            tabuleiro[0][espacoVazio[0]][espacoVazio[1]]=value
            tries += 1
            solucao = resolveTabuleiro(tabuleiro)
            if(solucao):
                return solucao
        tabuleiro[0][espacoVazio[0]][espacoVazio[1]]='0'
        tabuleiro[1].append(espacoVazio)
    else:
        return tabuleiro

def resolveUmTabuleiro(tabuleiro):
    print()
    global tries
    tries=0
    inicio = time()
    solucao = resolveTabuleiro(tabuleiro)
    fim = time()
    print('\ntentativas: '+str(tries))
    tempo = fim-inicio
    global tempoTotal
    tempoTotal += tempo
    print('\n'+embelezeTempo(tempo)+'\n\n\n')

global tempoTotal
tempoTotal = 0
files = os.listdir('C:\\pythonscript\\artificialInteligence\\sudokuSolver\\sudokus')
for name in files:
    print(name,end='\n\n')
    sudoku = open('C:\\pythonscript\\artificialInteligence\\sudokuSolver\\sudokus\\'+name)
    tabuleiro = criaTabuleiro(sudoku.read())
    sudoku.close()
    resolveUmTabuleiro(tabuleiro)
print('\n'+embelezeTempo(tempoTotal)+'\n\n\n')
