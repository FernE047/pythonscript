import random
import time

from textos import embelezeTempo

def ehLimpo(board):
    for elemento in board:
        if(elemento!=-1):
            return(False)
    return(True)

def ehValido(jogada):
    global board
    if(isinstance(jogada)=list):
        for a in jogada:
            if board[a]==-1:
                return(False)
    else:
        if board[jogada]==-1:
            return(False)
    return(True)

def fazJogada(quant):
    jogada=0
    while True:
        jogada=random.randint(0,quant)
        while(not(ehValido(jogada))):
            jogada=random.randint(0,quant)
        return(jogada)

while True:
    print('quantia de jogos')
    #quantJogo=int(input())
    quantJogo=1000
    print('quantia de pares')
    #quantPar=int(input())
    quantPar=4
    dados=[]
    inicio=time.time()
    for jogo in range(quantJogo):
        #print('jogo:'+str(jogo+1))
        board=[]
        memoria=[]
        for a in range(quantPar):
            board+=[a,a]
            memoria+=[-1,-1]
        random.shuffle(board)
        #print(board)
        jogada=[0,0]
        pecasVistas=[]
        total=0
        while(not(ehLimpo(board))):
            jogada[0]=fazJogada(len(board)-1)
            while True:
                jogada[0]=random.randint(0,len(board)-1)
                jogada[1]=random.randint(0,len(board)-1)
                while(not(ehValido(jogada))):
                    jogada[0]=random.randint(0,len(board)-1)
                    jogada[1]=random.randint(0,len(board)-1)
                if(jogada[0]!=jogada[1]):
                    break
            if(board[jogada[0]]==board[jogada[1]]):
                board[jogada[0]]=-1
                board[jogada[1]]=-1
            total+=1
            #print('jogada:'+str(jogada))
            #print('')
            #print(board)
        dados.append(total)
        #print(total)
    soma=0
    for elemento in dados:
        soma+=elemento
    fim=time.time()
    print('quantia de jogos:'+str(quantJogo))
    print('\n\nmedia:'+str(soma/quantJogo))
    print('maximo:'+str(max(dados)))
    print('minimo:'+str(min(dados)))
    print(embelezeTempo(fim-inicio))
    print('\ncontinuar')
    if(input()):
        break
