from time import time
from PIL import Image


def embelezeTempo(segundos: float) -> str:
    if segundos < 0:
        segundos = -segundos
        sign = "-"
    else:
        sign = ""
    total_ms = int(round(segundos * 1000))
    ms = total_ms % 1000
    total_s = total_ms // 1000
    s = total_s % 60
    total_min = total_s // 60
    m = total_min % 60
    total_h = total_min // 60
    h = total_h % 24
    d = total_h // 24
    parts: list[str] = []

    def add(value: int, singular: str, plural: str) -> None:
        if value:
            parts.append(f"{value} {singular if value == 1 else plural}")

    add(d, "day", "days")
    add(h, "hour", "hours")
    add(m, "minute", "minutes")
    add(s, "second", "seconds")
    if ms or not parts:
        parts.append(f"{ms} millisecond" if ms == 1 else f"{ms} milliseconds")
    return sign + ", ".join(parts)

def salva(tabuleiro,nome):
    imagem = Image.new('RGBA',(len(tabuleiro[0]),len(tabuleiro)),(255,255,255,255))
    for y, coluna in enumerate(tabuleiro):
        for x, celula in enumerate(coluna):
            if celula:
                imagem.putpixel((x,y),(0,0,0,255))
    imagem.save(nome+".png")
    imagem.close()

def situacaoCompara(situacoes,dica,ultimaCelula,limite,tamanho):
    if(dica[0]==0):
        if situacoes:
            return False
        else:
            return True
    if(len(situacoes)>len(dica)):
        return False
    if(situacoes):
        if(len(situacoes)>1):
            for index,situacao in enumerate(situacoes[:-1]):
                if(situacao!=dica[index]):
                    return False
        else:
            index=-1
        if not ultimaCelula:
            if(situacoes[index+1]!=dica[index+1]):
                return False
            if(len(situacoes)<len(dica)):
                if(tamanho-(limite+1)<len(dica[len(situacoes):])+sum(dica[len(situacoes):])-1):
                    return False
        else:
            if(situacoes[index+1]>dica[index+1]):
                return False
            if(situacoes[index+1] == dica[index+1]):
                if(tamanho-(limite+1)<len(dica[len(situacoes):])+sum(dica[len(situacoes):])-2):
                    return False
            else:
                if(tamanho-(limite+1)<len(dica[len(situacoes):])+sum(dica[len(situacoes):])+dica[index+1]-situacoes[index+1]-1):
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
    for _ in verticalDicas:
        tabuleiro.append([False for _ in horizontal])
    verticalDicas,horizontalConfig,verticalConfig,config = [None,None,None,None]
    dicas = [horizontal,vertical]
    jogo = [tabuleiro,dicas]
    resolveUmTabuleiro(jogo)
    print('\n'+embelezeTempo(tempoTotal)+'\n')
    salva(tabuleiro,nome.format(a))
