from time import time
from textos import embelezeTempo

def resolveUmTabuleiro(tabuleiro):
    print()
    global tries
    tries = 0
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
for pos in ((0,0),(0,1),(0,2),(0,3),(1,1),(1,2),(1,3),(2,2),(2,3),(3,3)):
    matriz = [[False for a in range(8)] for b in range(8)]
    matriz[pos[0]][pos[1]] = True
    tabuleiro = (matriz,pos)
    resolveUmTabuleiro(tabuleiro)
print('\n'+embelezeTempo(tempoTotal)+'\n\n\n')
