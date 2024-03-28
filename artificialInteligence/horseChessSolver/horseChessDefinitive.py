from time import time
from textos import embelezeTempo

class Tabuleiro:
    def __init__(self,dimensoes,tamanho=8,pos=[]):
        self.dimensoes = dimensoes
        self.tamanho = tamanho
        self.pos = pos
        if(self.dimensoes == 1):
            self.matriz = [False for a in range(tamanho)]
        else:
            self.matriz = Tabuleiro(self.dimensoes-1,self.tamanho)

    def setPos(self,pos):

    def setPosValue(self,value):
        if()

def criaMatrizSquare(dimensoes,tamanho):
    if(dimensoes==0):
        return False
    else:
        return [criaMatrizSquare(dimensoes-1,tamanho) for a in range(tamanho)]

def resolveUmTabuleiro(tabuleiro):
    print()
    global tries
    tries=0
    inicio = time()
    solucao = resolveTabuleiro(tabuleiro)
    fim = time()
    print('\ntentativas: '+str(tries))
    tempo = fim-inicio
    print('\n'+embelezeTempo(tempo)+'\n\n\n')

tabuleiro = criaTabuleiroSquare(3,5)
print(tabuleiro)
resolveUmTabuleiro(tabuleiro)
