from time import time
from textos import embelezeTempo
import os


def tiraEspaçoBranco(texto: str) -> str:
    for espaco in [" ", "\n", "\t"]:
        if espaco in texto:
            texto = texto.replace(espaco, "")
    return texto


def criaTabuleiro(config):
    matriz = []
    espacosVazios = []
    tabuleiro = {'matriz':matriz,'espacos':espacosVazios}
    for y in range(9):
        tabuleiro['matriz'].append([0,0,0,0,0,0,0,0,0])
    confLimpa = tiraEspaçoBranco(config)
    for a,valor in enumerate(list(confLimpa)):
        if(a>80):
            break
        posY = a//9
        posX = a%9
        tabuleiro['matriz'][posY][posX] = valor
        if(valor == '0'):
            tabuleiro['espacos']=[(posY,posX)]+tabuleiro['espacos']
    return tabuleiro

def verificaValor(tabuleiro,y,x,v):
        yQuad=y//3
        xQuad=x//3
        for a in range(3):
            for b in range(3):
                if(tabuleiro['matriz'][3*yQuad+a][3*xQuad+b]==v):
                    return False
        if(yQuad==0):
            for a in range(3,9):
                if(tabuleiro['matriz'][a][x]==v):
                    return False
        elif(yQuad==2):
            for a in range(0,6):
                if(tabuleiro['matriz'][a][x]==v):
                    return False
        else:
            for a in range(3):
                if(tabuleiro['matriz'][a][x]==v):
                    return False
            for a in range(6,9):
                if(tabuleiro['matriz'][a][x]==v):
                    return False
        if(xQuad==0):
            for b in range(3,9):
                if(tabuleiro['matriz'][y][b]==v):
                    return False
        elif(xQuad==2):
            for b in range(0,6):
                if(tabuleiro['matriz'][y][b]==v):
                    return False
        else:
            for b in range(3):
                if(tabuleiro['matriz'][y][b]==v):
                    return False
            for b in range(6,9):
                if(tabuleiro['matriz'][y][b]==v):
                    return False
        return True

def setElement(tabuleiro,y,x,v):
    tabuleiro['matriz'][y][x]='0'
    if v in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
        if(v=='0'):
            return True
        else:
            if(verificaValor(tabuleiro,y,x,v)):
                tabuleiro['matriz'][y][x]=v
                return True
    return False

def imprime(tabuleiro):
    for y in range(9):
        for x in range(9):
            print(tabuleiro['matriz'][y][x],end='')
        print()

def resolveTabuleiro(tabuleiro):
    if(tabuleiro['espacos']):
        espacoVazio = tabuleiro['espacos'].pop(-1)
        if(espacoVazio):
            global tries
            for value in range(1,10):
                if(setElement(tabuleiro,espacoVazio[0],espacoVazio[1],str(value))):
                    tries += 1
                    solucao = resolveTabuleiro(tabuleiro)
                    if(solucao):
                        return solucao
            tabuleiro['matriz'][espacoVazio[0]][espacoVazio[1]]='0'
            tabuleiro['espacos'].append(espacoVazio)
    else:
        return tabuleiro

def resolveUmTabuleiro(tabuleiro):
    imprime(tabuleiro)
    print()
    global tries
    tries=0
    inicio = time()
    solucao = resolveTabuleiro(tabuleiro)
    fim = time()
    imprime(solucao)
    print('\ntentativas: '+str(tries))
    tempo = fim-inicio
    global tempoTotal
    tempoTotal += tempo
    print('\n'+embelezeTempo(tempo)+'\n\n\n')

while True:
    global tempoTotal
    tempoTotal = 0
    files = os.listdir('sudokus')
    for name in files:
        print(name,end='\n\n')
        sudoku = open('sudokus//'+name)
        tabuleiro = criaTabuleiro(sudoku.read())
        sudoku.close()
        resolveUmTabuleiro(tabuleiro)
    print('\n'+embelezeTempo(tempoTotal)+'\n\n\n')
