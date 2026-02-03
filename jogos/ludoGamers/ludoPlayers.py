#importações

from string import ascii_uppercase
import numpy.random as npr
import math

#funções de DEBUG

def imprimirLista(lista,titulo):
    print(titulo,end="\n\n")
    for num,ele in enumerate(lista):
        print(str(num)+" : "+str(ele))
    print()

def imprimirDict(dictionary,titulo):
    print(titulo,end="\n\n")
    for num,ele in enumerate(dictionary):
        print(" : ".join([str(num),str(ele),str(dictionary[ele])]))
    print()

#funções de inicialização

def fazNome(numero):
    global ALFABETO
    global QUANTIA_JOGANDO
    idNome="{0:0"+str(int((math.log(numero,10) if numero>0 else 0)+1))+"d}"
    nome=ALFABETO[a%26]+idNome.format(int(a/26))
    return(nome)

def fazNomePecas(numero):
    global QUANTIA_PECAS_LUDO
    nome=fazNome(numero)
    idPeca="-{0:0"+str(int((math.log(QUANTIA_PECAS_LUDO,10) if numero>0 else 0)+1))+"d}"
    nomes=[nome+idPeca.format(int(b)) for b in range(QUANTIA_PECAS_LUDO)]
    return(nomes)

#funções booleanas

def todosGanharam(posicoes):
    for posicao in posicoes:
        if(posicao!="win"):
            return(False)
    return(True)

#informações pela ordem dos jogadores

def jogadorPorOrdem(n):
    global jogadoresOrdem
    jogadorAtual=jogadoresOrdem[n]
    return(jogadorAtual)

def achaCorPorOrdem(n):
    global corUsada
    cor=corUsada[jogadorPorOrdem(n)]
    return(cor)

def posicaoPecasPorOrdem(n):
    global pecaLocalizacao
    global playerPecas
    pecaPosicao={}
    for peca in playerPecas[jogadorPorOrdem(n)]:
        pecaPosicao[peca]=pecaLocalizacao[peca]
    return(pecaPosicao)

def estrategiaPorOrdem(n):
    global estrategia
    estrategiaAtual=estrategia[jogadorPorOrdem(n)]
    return(estrategiaAtual)

#funções básicas para Jogar    

def rolarDados():
    global QUANTIA_DADOS
    global FACES_DADOS
    resultados=[]
    for a in range(QUANTIA_DADOS):
        resultados.append(npr.randint(FACES_DADOS))
    return(resultados)

def jogadorPlay(tabuleiro,ordem):
    dados=rolarDados()
    cor=achaCorPorOrdem(ordem)
    estrategia=estrategiaPorOrdem(ordem)
    pecasPosicao=posicaoPecasPorOrdem(ordem)
    jogadorInfo={"dados":dados,"pecasPosicao":pecasPosicao,"cor":cor,"ordem":ordem}
    print("jogador "+cor+" rolou: "+",".join([str(dado) for dado in dados]))
    if(estrategia=="random"):
        tabuleiro=jogadaRandom(tabuleiro,jogadorInfo)
    return(tabuleiro)

def atualizaLocalizacoes(tabuleiro,pecaLocalizacao):
    for numeroCasa,casa in enumerate(tabuleiro):
        if(tabuleiro[numeroCasa]):
            for peca in casa:
                if(numeroCasa==len(tabuleiro)-1):
                    pecaLocalizacao[peca]="win"
                else:
                    pecaLocalizacao[peca]=numeroCasa
    return(pecaLocalizacao)

def movePecaXtoY(peca,x,y,tabuleiro):
    global pecaLocalizacao
    global tamanhoTabuleiro
    tabuleiro[x].pop(peca)
    jogadorId=peca[:peca.find("-")]
    if(y<tamanhoTabuleiro):
        casa=tabuleiro[y]
        if(casa):
            for pecaRival in casa:
                idRival=pecaRival[:peca.find("-")]
                if(idRival!=jogadorId):
                    pecaLocalizacao[pecaRival]="sleep"
        tabuleiro[y]=[peca]
        pecaLocalizacao[peca]=y
    else:
        tabuleiro[y]+=[peca]
        pecaLocalizacao[peca]="fila"

def movimentosPossiveis(tabuleiro,pecas,dados): #movimento={dados,peças,inicio,destino}
    for peca in pecas:
        
#funções estratégias

def jogadaRandom(tabuleiro,jogador):    #info={"dados":dados,"pecasPosicao":pecasPosicao,"cor":cor,"ordem":ordem}
    movimentos=movimentoPossiveis(tabuleiro,jogador["pecasPosicao"],jogador["dados"])
    return(tabuleiro)

#Inicialização das constantes e variaveis importantes

CAMINHADA_FINAL=5       #tamanho da fila colorida no meio do tabuleiro que todo player percorre no fim do jogo
QUANTIA_PECAS_LUDO=4    #quantas peças cada jogador irá ter
QUANTIA_DADOS=6         #quantos dados serão rodados numa jogada, 1 dado apenas diminui as estratégias que podem ser usadas
FACES_DADOS=6           #quantas faces tem os dados
QUANTIA_JOGADORES=4     #quantia de jogadores que o tabuleiro pode ter no total
QUANTIA_JOGANDO=4       #quantia de jogadores que estarão jogando, caso seja menor que a quantia de jogadores a ordem no tabuleiro é escolhida randomicamente
NUMEROS_SAIDA=(1)       #qual numero do dado permite retirar uma peça de seu estado dormente
if(QUANTIA_JOGANDO>QUANTIA_JOGADORES):
    QUANTIA_JOGANDO=QUANTIA_JOGADORES
JOGADORES_CORES=["vermelho","amarelo","azul","verde","roxo","rosa","laranja","marrom","cinza","ciano","lima","agua","verde-claro","preto"]
ALFABETO=list(ascii_uppercase)


def main() -> None:
    tamanhoTabuleiro=2*QUANTIA_JOGADORES*(CAMINHADA_FINAL+2)
    tabuleiro=(tamanhoTabuleiro+CAMINHADA_FINAL+1)*[[]]

    #Inicialização das variaveis dos jogadores

    jogador=[]
    corUsada={}
    jogadoresOrdem={}
    playerPecas={}
    pecaLocalizacao={}
    estrategia={}
    ordemSorteio=npr.choice([a for a in range(QUANTIA_JOGADORES)],QUANTIA_JOGANDO,replace=False)
    ordemSorteio=sorted(ordemSorteio)
    for a in range(QUANTIA_JOGANDO):
        nome=fazNome(a)
        jogador.append(nome)
        jogadoresOrdem[ordemSorteio[a]]=nome
        if(QUANTIA_JOGANDO<=14):
            corUsada[nome]=JOGADORES_CORES[a]
        playerPecas[nome]=fazNomePecas(a)
        for umaPeca in playerPecas[nome]:
            pecaLocalizacao[umaPeca]="sleep"
        estrategia[nome]="random"
        
    #deletar variaveis não reutilizaveis

    del ordemSorteio

    #DEBUG

    print("tamanho : "+str(tamanhoTabuleiro))
    imprimirLista(tabuleiro,"tabuleiro : ")
    imprimirLista(jogador,"jogadores : ")
    imprimirLista(estrategia,"estrategias : ")
    imprimirDict(playerPecas,"peças : ")
    imprimirDict(pecaLocalizacao,"peças Localização : ")
    imprimirDict(corUsada,"cores : ")
    imprimirDict(jogadoresOrdem,"ordem : ")

    #Jogo

    while(not(todosGanharam(pecaLocalizacao))):
        for n in range(QUANTIA_JOGADORES):
            if(n in jogadoresOrdem.keys()):
                tabuleiro=jogadorPlay(tabuleiro,n)
                pecaLocalizacao=atualizaLocalizacoes(tabuleiro,pecaLocalizacao)

if __name__ == "__main__":
    main()