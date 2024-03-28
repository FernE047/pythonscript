from time import time
from textos import embelezeTempo
from PIL import Image

def salva(tabuleiro,nome):
    imagem = Image.new('RGBA',(len(tabuleiro[0]),len(tabuleiro)),(255,255,255,255))
    for y in range(len(tabuleiro)):
        for x in range(len(tabuleiro[0])):
            if(tabuleiro[y][x] == 1):
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
        if ultimaCelula != 1 :
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

def verificaColunasParcial(tabuleiro,dicas,limiteY,minimoX,limiteX,novaLinha):
    for x in range(minimoX,limiteX):
        dica = dicas[0][x]
        situacao = []
        ultimaCelula = 0
        for y in range(limiteY+1):
            if(y == limiteY):
                if(novaLinha):
                    celula = novaLinha[x-minimoX]
                else:
                    celula = tabuleiro[y][x]
            else:
                celula = tabuleiro[y][x]
            if ultimaCelula == 1:
                if(celula == 1):
                    contagem += 1
                else:
                    situacao.append(contagem)
            else:
                if celula == 1:
                    contagem = 1
            ultimaCelula = celula
        if ultimaCelula == 1:
            situacao.append(contagem)
        if(not situacaoCompara(situacao,dica,ultimaCelula,limiteY,len(tabuleiro))):
            return False
    return True

def possibilidades(tamanho,dica,dicas,tabuleiro,y):
    if(not(dica)):
        return([[-1 for a in range(tamanho)]])
    if(tamanho == dica[0]):
        return([[1 for a in range(tamanho)]])
    if(dica[0] == 0):
        return([[-1 for a in range(tamanho)]])
    if(len(dica)-1+sum(dica)==tamanho):
        possibilidade = []
        for n in dica:
            for a in range(n):
                possibilidade.append(1)
            possibilidade.append(-1)
        possibilidade.pop(-1)
        return([possibilidade])
    lista = []
    numero = dica[0]
    if(len(dica)==1):
        for inicial in range(tamanho-numero+1):
            possibilidade = [-1 for a in range(tamanho)]
            for x in range(numero):
                possibilidade[inicial+x]=1
            if(verificaColunasParcial(tabuleiro,dicas,y,len(dicas[0])-tamanho,len(dicas[0])-tamanho+len(possibilidade),possibilidade)):
                lista.append(possibilidade)
    else:
        for inicial in range(tamanho-numero+1-sum(dica[1:])-len(dica[1:])):
            possibilidade = [-1 for a in range(inicial+numero)]
            for x in range(numero):
                possibilidade[inicial+x]=1
            if(verificaColunasParcial(tabuleiro,dicas,y,len(dicas[0])-tamanho,len(dicas[0])-tamanho+len(possibilidade)+1,possibilidade+[-1])):
                adicionais = possibilidades(tamanho-inicial-numero-1,dica[1:],dicas,tabuleiro,y)
                for add in adicionais:
                    lista.append(possibilidade+[-1]+add)
    return(lista)

def resolveTabuleiro(tabuleiro,dicas,numeroLinha):
    if(numeroLinha == len(tabuleiro)):
        return tabuleiro
    else:
        linhaOriginal = tabuleiro[numeroLinha]
        for linhaPoss in possibilidades(len(tabuleiro[0]),dicas[1][numeroLinha],dicas,tabuleiro,numeroLinha):
            global tries
            tries += 1
            tabuleiro[numeroLinha] = linhaPoss
            solucao = resolveTabuleiro(tabuleiro,dicas,numeroLinha+1)
            if(solucao):
                return solucao
        tabuleiro[numeroLinha] = linhaOriginal

def resolveUmTabuleiro(tabuleiro,dicas):
    print()
    global tries
    tries = 0
    cortes = 0
    inicio = time()
    solucao = resolveTabuleiro(tabuleiro,dicas,0)
    fim = time()
    print('\ntentativas: '+str(tries))
    tempo = fim-inicio
    global tempoTotal
    tempoTotal += tempo
    for linha in tabuleiro:
        print()
        for element in linha:
            if(element>0):
                print('#',end='')
            else:
                if(element == 0):
                    print('?',end='')
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
    horizontal,vertical = config.split('#')
    horizontal = [[int(n) for n in dica.split()] for dica in horizontal[:-1].split('\n')]
    vertical = [[int(n) for n in dica.split()] for dica in vertical[1:].split('\n')]
    tabuleiro = []
    for y in range(len(vertical)):
        tabuleiro.append([0 for x in range(len(horizontal))])
    dicas = [horizontal,vertical]
    resolveUmTabuleiro(tabuleiro,dicas)
    print('\n'+embelezeTempo(tempoTotal)+'\n')
    salva(tabuleiro,nome.format(a))
print('\n'+embelezeTempo(tempoTotal)+'\n\n\n')
