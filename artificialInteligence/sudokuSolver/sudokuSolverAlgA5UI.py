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

def imprimeTabuleiro(tabuleiro):
    for y in range(9):
        if((y!=0)and(y%3==0)):
           print('---+---+---')
        tabuleiro[y]=tabuleiro[y][0:3]+['|']+tabuleiro[y][3:6]+['|']+tabuleiro[y][6:]
        print(''.join(tabuleiro[y]))

def criaTabuleiro(config):
    matriz = []
    espacosVazios = []
    tabuleiro = [matriz,espacosVazios]
    for y in range(9):
        tabuleiro[0].append(['0','0','0','0','0','0','0','0','0'])
    confLimpa = tiraEspaçoBranco(config)
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

while True:
    global tempoTotal
    tempoTotal = 0
    mode = choose_from_options('escolha uma opcao:',['sair','Input Manual','Import Sudoku Txt','Loop Import Folder'],'number')
    if(mode==0):
        break
    if(mode==3):
        files = os.listdir('sudokus')
        for name in files:
            print(name,end='\n\n')
            sudoku = open('sudokus//'+name)
            tabuleiro = criaTabuleiro(sudoku.read())
            sudoku.close()
            resolveUmTabuleiro(tabuleiro)
            print('\n'+embelezeTempo(tempoTotal)+'\n\n\n')
    elif(mode==2):
        name = pS('qual o nome do arquivo?')
        sudoku = open(name+'.txt')
        tabuleiro = criaTabuleiro(sudoku.read())
        sudoku.close()
        resolveUmTabuleiro(tabuleiro)
    else:
        sudoku = ''.join(['0' for a in range(81)])
        quantia = 0
        while quantia<81:
            inputConfig = pS('')
            for v in inputConfig:
                if v in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                    sudoku = list(sudoku)
                    sudoku[quantia] = v
                    sudoku = ''.join(sudoku)
                    print('elemento '+v+' adicionado')
                    quantia += 1
                else:
                    if(v=='p'):
                        if(quantia>0):
                            quantia -= 1
                            print('numero '+sudoku[-1]+' apagado')
                            sudoku = list(sudoku)
                            sudoku[quantia] = '0'
                            sudoku = ''.join(sudoku)
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
                        sudoku = ''
                        quantia = 0
                    elif(v=='s'):
                        for a in range(81):
                            print(sudoku[a],end='')
                            if(a%9==8):
                                print()
                    elif(v=='e'):
                        quantia=81
                    else:
                        print('digite um numero entre 0 e 9 ou opcoes adicionais')
                        sudoku[quantia] = '0'
                        quantia += 1
            for a in range(81):
                print(sudoku[a],end='')
                if(a%9==8):
                    print()
        tabuleiro = criaTabuleiro(sudoku)
        resolveUmTabuleiro(tabuleiro)
        imprimeTabuleiro(tabuleiro)
