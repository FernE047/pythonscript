from time import time
from textos import embelezeTempo
from PIL import Image

def salva(tabuleiro,nome):
    imagem = Image.new('RGBA',(len(tabuleiro[0]),len(tabuleiro)),(255,255,255,255))
    for y in range(len(tabuleiro)):
        for x in range(len(tabuleiro[0])):
            if tabuleiro[y][x]:
                imagem.putpixel((x,y),(0,0,0,255))
    imagem.save(nome+".png")
    imagem.close()

def situacaoCompara(situacao,dica,ultimaCelula,limite,tamanho):
    if(dica[0]==0):
        if situacao:
            return False
        else:
            return True
    if(len(situacao)>len(dica)):
        return False
    if(situacao):
        if(len(situacao)>1):
            for n in range(len(situacao)-1):
                if(situacao[n]!=dica[n]):
                    return False
        else:
            n=-1
        if not ultimaCelula:
            if(situacao[n+1]!=dica[n+1]):
                return False
            if(len(situacao)<len(dica)):
                if(tamanho-(limite+1)<len(dica[len(situacao):])+sum(dica[len(situacao):])-1):
                    return False
        else:
            if(situacao[n+1]>dica[n+1]):
                return False
            if(situacao[n+1] == dica[n+1]):
                if(tamanho-(limite+1)<len(dica[len(situacao):])+sum(dica[len(situacao):])-2):
                    return False
            else:
                if(tamanho-(limite+1)<len(dica[len(situacao):])+sum(dica[len(situacao):])+dica[n+1]-situacao[n+1]-1):
                    return False
    else:
        if(tamanho-(limite+1)<len(dica)+sum(dica)-1):
            return False
    return True

def verificaColunasParcial(jogo,limiteY,minimoX,limiteX):
    if(minimoX != 0):
        minimoX -= 1
    for x in range(minimoX,limiteX):
        dica = jogo[1][0][x]
        situacao = []
        ultimaCelula = False
        for y in range(limiteY+1):
            celula = jogo[0][y][x]
            if ultimaCelula:
                if celula:
                    contagem += 1
                else:
                    situacao.append(contagem)
            else:
                if celula:
                    contagem = 1
            ultimaCelula = celula
        if ultimaCelula:
            situacao.append(contagem)
        if(not situacaoCompara(situacao,dica,ultimaCelula,limiteY,len(jogo[0]))):
            return False
    return True

def resolveTabuleiro(jogo):
    if(not(jogo[1][1])):
        return jogo[0]
    else:
        dicaAtual = jogo[1][1].pop(0)
        if(dicaAtual[1]==0):
            solucao = resolveTabuleiro(jogo)
            if(solucao):
                return solucao
        else:
            y = dicaAtual[0]
            primeiroEspacoLivre = -1
            tamanhoX = len(jogo[1][0])
            for x in range(tamanhoX):
                if jogo[0][y][x]:
                    primeiroEspacoLivre = x
            if primeiroEspacoLivre!=-1:
                primeiroEspacoLivre += 2
            else:
                primeiroEspacoLivre = 0
            dicasY = []
            if(jogo[1][1]):
                for dica in jogo[1][1]:
                    if(dica[0]==y):
                        dicasY.append(dica)
                    else:
                        break
                tamanhoDicasAdicionais = (len(dicasY)+sum([dica[1] for dica in dicasY]))
            else:
                tamanhoDicasAdicionais = 0
            espacoLivreTotal = len(jogo[1][0])-primeiroEspacoLivre-tamanhoDicasAdicionais
            if(dicaAtual[1]<=espacoLivreTotal):
                if((dicaAtual[1]==espacoLivreTotal)and(dicasY)):
                    for x in range(primeiroEspacoLivre,primeiroEspacoLivre+dicaAtual[1]):
                        jogo[0][y][x] = True
                    for dica in dicasY:
                        jogo[1][1].pop(0)
                        for x in range(x+2,x+dica[1]+2):
                            jogo[0][y][x] = True
                        if(verificaColunasParcial(jogo,y,primeiroEspacoLivre,len(jogo[0][0]))):
                            global triesA
                            triesA += 1
                            solucao = resolveTabuleiro(jogo)
                            if(solucao):
                                return solucao
                    for x in range(primeiroEspacoLivre,len(jogo[0][0])):
                        jogo[0][y][x] = False
                    jogo[1][1]=dicasY+jogo[1][1]
                else:
                    for inicial in range(primeiroEspacoLivre,tamanhoX-dicaAtual[1]+1-tamanhoDicasAdicionais):
                        for x in range(inicial,inicial+dicaAtual[1]):
                            jogo[0][y][x] = True
                        if(verificaColunasParcial(jogo,y,primeiroEspacoLivre,inicial+dicaAtual[1])):
                            global tries
                            tries += 1
                            solucao = resolveTabuleiro(jogo)
                            if(solucao):
                                return solucao
                        for x in range(inicial,inicial+dicaAtual[1]):
                            jogo[0][y][x] = False
        jogo[1][1]=[dicaAtual]+jogo[1][1]

def resolveUmTabuleiro(jogo):
    print()
    global tries
    global triesA
    tries = 0
    triesA = 0
    cortes = 0
    inicio = time()
    solucao = resolveTabuleiro(jogo)
    fim = time()
    print('\ntentativas: '+str(tries))
    print('\nCortes: '+str(triesA))
    tempo = fim-inicio
    global tempoTotal
    tempoTotal += tempo
    for linha in jogo[0]:
        print()
        for element in linha:
            if element:
                print('#',end='')
            else:
                print('0',end='')
    print()
    print('\n'+embelezeTempo(tempo)+'\n')


#nome = pS('qual o nome do arquivo?')
nome = "piccross//A{0:03d}"
tempoTotal = 0
for a in range(8):
    picFile = open(nome.format(a)+".txt")
    config = picFile.read()
    picFile.close()
    horizontalConfig,verticalConfig = config.split('#')
    horizontal = [[int(n) for n in dica.split()] for dica in horizontalConfig[:-1].split('\n')]
    verticalDicas = verticalConfig[1:].split('\n')
    vertical = []
    for y,dica in enumerate(verticalDicas):
        for numero in dica.split():
            vertical.append([y,int(numero)])
    tabuleiro = []
    for y in range(len(verticalDicas)):
        tabuleiro.append([False for x in range(len(horizontal))])
    verticalDicas,horizontalConfig,verticalConfig,config = [None,None,None,None]
    dicas = [horizontal,vertical]
    jogo = [tabuleiro,dicas]
    resolveUmTabuleiro(jogo)
    print('\n'+embelezeTempo(tempoTotal)+'\n')
    salva(tabuleiro,nome.format(a))
