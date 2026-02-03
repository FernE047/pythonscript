from numpy.random import randint
from string import ascii_uppercase
from typing import Literal, overload


def pegaInteiro(
    mensagem: str, minimo: int | None = None, maximo: int | None = None
) -> int:
    while True:
        entrada = input(f"{mensagem} : ")
        try:
            valor = int(entrada)
            if (minimo is not None) and (valor < minimo):
                print(f"valor deve ser maior ou igual a {minimo}")
                continue
            if (maximo is not None) and (valor > maximo):
                print(f"valor deve ser menor ou igual a {maximo}")
                continue
            return valor
        except Exception as _:
            print("valor inválido, tente novamente")


@overload
def choose_from_options(
    prompt: str, options: list[str], mode: Literal["text"]
) -> str: ...


@overload
def choose_from_options(
    prompt: str, options: list[str], mode: Literal["number"]
) -> int: ...

@overload
def choose_from_options(
    prompt: str, options: list[str]
) -> str: ...


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

def imprime(board):
    global IMPRESSAO
    if(not(IMPRESSAO)):
        return
    tamanho=len(board)
    lista=[str(a) for a in range(tamanho)]
    print(" "+" ".join(lista))
    entreLinha=" "+"+".join(["-" for a in range(tamanho)])
    for n,linhaValores in enumerate(board):
        linha=str(n)
        for m,valor in enumerate(linhaValores):
            if(valor==0):
                linha+=" "
            else:
                linha+=str(valor)
            if(m!=tamanho-1):
                linha+="|"
        print(linha)
        if(n!=tamanho-1):
            print(entreLinha)
    print()

def ganhou(board):
    tamanho=len(board)
    simbolo=board[0][0]
    win=True
    for x in range(tamanho):
        casa=board[x][x]
        if(casa==0):
            win=False
            break
        if(casa!=simbolo):
            win=False
            break
    if(win):
        return(True)
    simbolo=board[0][-1]
    win=True
    for x in range(tamanho):
        casa=board[x][tamanho-x-1]
        if(casa==0):
            win=False
            break
        if(casa!=simbolo):
            win=False
            break
    if(win):
        return(True)
    for y in range(tamanho):
        simbolo=board[y][0]
        win=True
        for x in range(tamanho):
            casa=board[y][x]
            if(casa==0):
                win=False
                break
            if(casa!=simbolo):
                win=False
                break
        if(win):
            return(True)
    for x in range(tamanho):
        simbolo=board[0][x]
        win=True
        for y in range(tamanho):
            casa=board[y][x]
            if(casa==0):
                win=False
                break
            if(casa!=simbolo):
                win=False
                break
        if(win):
            return(True)
    return(False)

def velha(board):
    if(len(possibilidadesDeJogadas(board))==0):
        return True
    return False

def final(tabuleiro,texto):
    global IMPRESSAO
    if(ganhou(tabuleiro)):
        if(IMPRESSAO):print(texto,end=" Ganhou\n\n\n")
        return "win"
    if(velha(tabuleiro)):
        if(IMPRESSAO):print("Deu velha",end="\n\n\n")
        return "draw"
    return False

def randomNumber(number):
    SEEDLEN=7
    while(number==0):
        number=randint(10**(SEEDLEN-1)+1,10**SEEDLEN)
    newNumber=number**2
    newNumber=list(str(newNumber))
    while(len(newNumber)>4):
        newNumber.pop(0)
        if(newNumber==SEEDLEN):
            break
        newNumber.pop()
    newNumber=int("".join(newNumber))
    return newNumber

def possibilidadesDeJogadas(board):
    tamanho=len(board)
    jogadaPossivel=[]
    for y in range(tamanho):
        for x in range(tamanho):
            if(board[y][x]==0):
                jogadaPossivel.append((y,x))
    return(jogadaPossivel)

def jogadaHumana(board):
    tamanho=len(board)
    while True:
        while True:
            y=pegaInteiro("digite Y")
            if((y<0)or(y>tamanho-1)):
                print("numero invalido")
            else:
                break
        while True:
            x=pegaInteiro("digite X")
            if((x<0)or(x>tamanho-1)):
                print("numero invalido")
            else:
                break
        if(board[y][x]!=0):
            print("coordenada já utilizada")
        else:
            break
    return(((y,x)))

#cada jogada algo deverá apenas pegar as possibilidades, caso não tenha, joga random

def jogadaMirrorX(board):
    tamanho=len(board)
    possibilidades=[]
    for y in range(tamanho):
        for x in range(tamanho):
            if(board[y][x]):
                if(not(board[y][tamanho-1-x])):
                    possibilidades.append((y,tamanho-1-x))
    return(possibilidades)

def jogadaMirrorY(board):
    tamanho=len(board)
    possibilidades=[]
    for y in range(tamanho):
        for x in range(tamanho):
            if(board[y][x]):
                if(not(board[tamanho-1-y][x])):
                    possibilidades.append((tamanho-1-y,x))
    return(possibilidades)

def jogada180(board):
    tamanho=len(board)
    possibilidades=[]
    for y in range(tamanho):
        for x in range(tamanho):
            if(board[y][x]):
                if(not(board[tamanho-1-y][tamanho-1-x])):
                    possibilidades.append((tamanho-1-y,tamanho-1-x))
    return(possibilidades)

def jogadaMirrorDiagonal(board):
    tamanho=len(board)
    possibilidades=[]
    for y in range(tamanho):
        for x in range(tamanho):
            if(board[y][x]):
                if(not(board[x][y])):
                    possibilidades.append((x,y))
    return(possibilidades)

def jogadaMirrorDiagonalX(board):
    tamanho=len(board)
    possibilidades=[]
    for y in range(tamanho):
        for x in range(tamanho):
            if(board[y][x]):
                if(not(board[tamanho-1-x][tamanho-1-y])):
                    possibilidades.append((tamanho-1-x,tamanho-1-y))
    return(possibilidades)

def jogadaNormal(board,jogador,number):
    global IMPRESSAO
    simbolo=jogador["simbolo"]
    if(IMPRESSAO):print("simbolo "+simbolo+" : \n")
    possibilidades=fazJogada(tabuleiro,jogador["estrategia"])
    total=len(possibilidades)
    if(total==0):
        possibilidades=fazJogada(tabuleiro,"random")
        total=len(possibilidades)
    coordenadas=possibilidades[number%total]
    tabuleiro[coordenadas[0]][coordenadas[1]]=simbolo
    imprime(tabuleiro)
    return final(board,"simbolo "+simbolo)

def fazJogada(tabuleiro,estrategia):
    if(estrategia=="random"):
        return possibilidadesDeJogadas(tabuleiro)
    elif(estrategia=="mirrorx"):
        return jogadaMirrorX(tabuleiro)
    elif(estrategia=="mirrory"):
        return jogadaMirrorY(tabuleiro)
    elif(estrategia=="mirrordiag"):
        return jogadaMirrorDiagonal(tabuleiro)
    elif(estrategia=="mirrordiagx"):
        return jogadaMirrorDiagonalX(tabuleiro)
    elif(estrategia=="spin180clock"):
        return jogada180(tabuleiro)
    else:
        return jogadaHumana(tabuleiro)

IMPRESSAO=("sim"==choose_from_options("impressao na tela?",["sim","não"]))
ESTRATEGIAS=["random","mirrorx","mirrory","mirrordiag","mirrordiagx","spin180clock"]
if(IMPRESSAO):
    ESTRATEGIAS+=["humano"]
while True:
    ESTRATEGIAS=["aleatorios"]+list(ESTRATEGIAS)
    partidasTotal=pegaInteiro("digite quantas partidas serão jogadas")
    tamanho=pegaInteiro("digite o tamanho do tabuleiro", maximo = 10)
    seed=0
    estrategia1=choose_from_options("digite a estrategia do player 1",ESTRATEGIAS)
    ESTRATEGIAS.pop(0)
    if(estrategia1=="aleatorios"):
        ESTRATEGIAS.pop()
        estrategia1=ESTRATEGIAS[randint(len(ESTRATEGIAS))-1]
        estrategia2=ESTRATEGIAS[randint(len(ESTRATEGIAS))-1]
        ESTRATEGIAS+=["humano"]
    else:
        estrategia2=choose_from_options("digite a estrategia do player 2",ESTRATEGIAS)
    jogador=[{"simbolo":"X","estrategia":estrategia1,"vitorias":0},{"simbolo":"O","estrategia":estrategia2,"vitorias":0}]
    for partida in range(partidasTotal):
        seed=randomNumber(seed)
        tabuleiro=[[0 for b in range(tamanho)] for a in range(tamanho)]
        vitoria=lambda jog,number:jogadaNormal(tabuleiro,jog,number)
        imprime(tabuleiro)
        for vez in range(tamanho**2):
            resultado=vitoria(jogador[vez%2],seed)
            if(resultado):
                if(resultado=="win"):
                    jogador[vez%2]["vitorias"]+=1
                break
    print("tamanho do tabuleiro : "+str(tamanho))
    print("partidas no total : "+str(partidasTotal))
    vitoria1=jogador[0]["vitorias"]
    vitoria2=jogador[1]["vitorias"]
    print("jogador "+jogador[0]["simbolo"]+" ganhou "+str(vitoria1)+" vezes, "+str(vitoria1*100/partidasTotal)+"%, com a estrategia "+jogador[0]["estrategia"])
    print("jogador "+jogador[1]["simbolo"]+" ganhou "+str(vitoria2)+" vezes, "+str(vitoria2*100/partidasTotal)+"%, com a estrategia "+jogador[1]["estrategia"])
    print("Empatou "+str(partidasTotal-vitoria1-vitoria2)+" vezes, "+str(100-(vitoria1+vitoria2)*100/partidasTotal)+"%")
    if("não"==choose_from_options("continuar?",("sim","não"))):
        break
