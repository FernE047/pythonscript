'''
PIECES:

walkers = 0 (rook)
jumpers = 1 (horses)
summers = 2 (queen)
custom = 3 (pawn)
multiDimensionalSteper = 4 (king)
square = 5 (king)
jumpWalker = 6 (none)

VICTORY:

check-mate = 0
check = 1
capture = 2
capture-All = 3

'''
from itertools import permutations as perm

def imprimeTabuleiro(tabuleiro,posicao=None):
    if posicao == None:
        posicao = []
    if len(posicao) == 0:
        if type(tabuleiro[0]) == type(list()):
            for tab in tabuleiro:
                imprimeTabuleiro(tab)
            print()
        else:
            print(tabuleiro[0]+(tabuleiro[0] if tabuleiro[1] == 0 else str(tabuleiro[1])),end="")
    else:
        imprimeTabuleiro(tabuleiro[posicao[0]],posicao[1:])

def montaTabuleiro(dimensao = 2, tamanho = 8, posicao = None):
    if posicao == None:
        posicao = []
    if dimensao == 0:
        if sum(posicao)%2:
            return ['█',0]
        else:
            return [' ',0]
    else:
        tabuleiro = []
        for t in range(tamanho):
            posicao.append(t)
            tabuleiro.append(montaTabuleiro(dimensao-1,tamanho,posicao))
            posicao.pop(-1)
    return tabuleiro

def verificaTabuleiro(tabuleiro,posicao):
    if len(posicao) == 0:
        return tabuleiro
    else:
        return verificaTabuleiro(tabuleiro[posicao[0]],posicao[1:])

def horizontalSymmetry(tabuleiro,dimensaoAtual = -1):
    global tamanho
    global dimensao
    if dimensaoAtual == -1:
        dimensaoAtual = dimensao
    if dimensaoAtual == 1:
        for n,peca in enumerate(tabuleiro):
            if peca[1] != 0:
                tabuleiro[tamanho-n-1][0] = peca[0]
                tabuleiro[tamanho-n-1][1] = peca[1]
    else:
        for a in range(tamanho):
            horizontalSymmetry(tabuleiro[a],dimensaoAtual - 1)

def verticalSymmetry(tabuleiro,tab=None,dimensaoAtual = None,posicao = None):
    global tamanho
    if posicao == None:
        posicao = []
    if tab == None:
        tab = tabuleiro
    if dimensaoAtual == None:
        global dimensao
        dimensaoAtual = dimensao
    if dimensaoAtual == 1:
        for n,peca in enumerate(tab):
            if peca[1]!=0:
                posicaoAlt = []
                posicaoAlt.append(tamanho-posicao[0]-1)
                posicao.append(n)
                colocaPeca(tabuleiro,peca[0],1 if peca[1]==2 else 2,posicaoAlt+posicao[1:])
                posicao.pop(-1)
    else:
        for a in range(tamanho):
            posicao.append(a)
            verticalSymmetry(tabuleiro,tab[a],dimensaoAtual - 1,posicao)
            posicao.pop(-1)

def rotateTabuleiro(tabuleiro,novoTabuleiro=None,tab=None,dimensaoAtual=None,posicao = None):
    global tamanho
    if posicao == None:
        posicao = []
    if tab == None:
        tab = tabuleiro
    if dimensaoAtual == None:
        global dimensao
        dimensaoAtual = dimensao
    if novoTabuleiro == None:
        novoTabuleiro = montaTabuleiro(dimensao,tamanho)
    if dimensaoAtual == 1:
        for n,peca in enumerate(tab):
            if peca[1]!=0:
                posicaoAlt = []
                posicao.append(n)
                for n,number in enumerate(posicao):
                    if n in (0,len(posicao)-1):
                        posicaoAlt.append(tamanho-number-1)
                    else:
                        posicaoAlt.append(number)
                colocaPeca(novoTabuleiro,peca[0],peca[1],posicaoAlt)
                posicao.pop(-1)
    else:
        for a in range(tamanho):
            posicao.append(a)
            rotateTabuleiro(tabuleiro,novoTabuleiro,tab[a],dimensaoAtual - 1,posicao)
            posicao.pop(-1)
    if dimensaoAtual == dimensao:
        return novoTabuleiro

def colocaPeca(tabuleiro,peca,jogador,posicao = None):
    if posicao != None:
        if len(posicao) == 1:
            colocaPeca(tabuleiro[posicao[0]],peca,jogador)
        else:
            colocaPeca(tabuleiro[posicao[0]],peca,jogador,posicao[1:])
    else:
        if type(tabuleiro[0])==type(str()):
            tabuleiro[0] = peca
            tabuleiro[1] = jogador
        else:
            for tab in tabuleiro:
                colocaPeca(tab,peca,jogador)

def movePeca(tabuleiro,posicaoInicio,posicaoFinal):
    peca = verificaTabuleiro(tabuleiro,posicaoInicio)
    colocaPeca(tabuleiro,peca[0],peca[1],posicaoFinal)
    limpo = '█' if sum(posicaoInicio)%2 else ' '
    colocaPeca(tabuleiro,limpo,0,posicaoInicio)

def encontraPecas(tabuleiro,jogador1Lista,jogador2Lista,posicao = None):
    if posicao == None:
        posicao = []
    if type(tabuleiro[0]) == type(list()):
        for n,tab in enumerate(tabuleiro):
            posicao.append(n)
            encontraPecas(tab,jogador1Lista,jogador2Lista,posicao)
            posicao.pop(-1)
    else:
        if tabuleiro[1] == 1:
            jogador1Lista.append([tabuleiro[0],posicao.copy()])
        if tabuleiro[1] == 2:
            jogador2Lista.append([tabuleiro[0],posicao.copy()])
    return [jogador1Lista,jogador2Lista]

def jogadasPossiveisIndividuais(tabuleiro, peca, jogador):
    global comportamentos
    global dimensao
    global tamanho
    comportamento = comportamentos[peca[0]]
    posicaoAtual = peca[1]
    if len(comportamento) == 5:
        tipo,estatico,movimento,captura,value = comportamento
    else:
        tipo,estatico,movimento,value = comportamento
        captura = movimento
    while len(movimento) < dimensao:
        movimento.append(0)
    while len(captura) < dimensao:
        captura.append(0)
    if tipo == 0 :
        for movimentoNovo in set(perm(movimento)):
            

def encontraJogadasPossiveis(tabuleiro, pecasJogador, jogador):
    jogadas = []
    for peca in pecasJogador:
        jogadas.append()

dimensao = 2
tamanho = 8
tabuleiro = montaTabuleiro(dimensao,tamanho)
comportamentos = {"P":[3,False,[1],[[1,1],[1,-1]],1],  #pawn
                  "R":[0,True,[1],5],                  #rook
                  "N":[1,True,[1,2],3],                #knight
                  "B":[0,True,[1,1],3],                #bishop
                  "Q":[2,True,[1,3],9],                  #queen
                  "K":[5,True,1,2]}                      #king
victory = [0,"K"]
colocaPeca(tabuleiro,"R",1,[0,0])
colocaPeca(tabuleiro,"N",1,[0,1])
colocaPeca(tabuleiro,"B",1,[0,2])
colocaPeca(tabuleiro,"P",1,[1])
horizontalSymmetry(tabuleiro)
colocaPeca(tabuleiro,"Q",1,[0,3])
colocaPeca(tabuleiro,"K",1,[0,4])
verticalSymmetry(tabuleiro)
pecasJogador = [[],[]]
encontraPecas(tabuleiro,pecasJogador[0],pecasJogador[1])
tabuleiro = rotateTabuleiro(tabuleiro)
imprimeTabuleiro(tabuleiro)
vezDeJogar = 0
rodada = 0
while True:
    jogadasPossiveis = encontraJogadasPossiveis(tabuleiro,pecasJogador[vezDeJogar],vezDeJogar+1)
