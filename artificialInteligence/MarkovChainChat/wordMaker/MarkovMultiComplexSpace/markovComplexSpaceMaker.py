from random import randint
from numpy.random import choice

def getAnChar(nome,indice,indiceEspaco,anterior = ''):
    nome += "//{0:03d}.txt"
    file = open(nome.format(indice),encoding='utf-8')
    linha = file.readline()
    data = {}
    while linha:
        palavras = linha[:-1].split()
        if int(palavras[0]) == indiceEspaco:
            if anterior == palavras[1:-2]:
                letra = palavras[-2]
                numero = int(palavras[-1])
                data[letra] = numero
        linha = file.readline()
    total = sum(list(data.values()))
    escolhido = randint(1,total)
    soma = 0
    for indice,valor in enumerate(data.values()):
        soma += valor
        if soma >= escolhido:
            file.close()
            return list(data.keys())[indice]

def doAWord(nome,indiceEspaco):
    mensagem = ""
    anteriores = []
    letra = getAnChar(nome,0,indiceEspaco,anteriores)
    while letra != "¨":
        mensagem += letra
        if len(anteriores)==2:
            anteriores.pop(0)
        anteriores.append(letra)
        letra = getAnChar(nome,len(mensagem),indiceEspaco,anteriores)
    return mensagem

def arrumaStats(lista):
    soma = sum(lista)
    lista = [value / soma for value in lista]
    while sum(lista)!=1:
        if sum(lista)>1:
            add = sum(lista)-1
            lista[lista.index(max(lista))] -= add
        elif sum(lista)<1:
            add = 1-sum(lista)
            lista[lista.index(min(lista))] += add
    return lista

notSuccess = True
while notSuccess:
    try:
        print("o que deseja abrir?")
        nome = input()
        try:
            arqInput = open(nome+"//{0:03d}.txt",'r',encoding = "UTF-8")
            arqInput.close()
        except:
            pass
        notSuccess = False
    except:
        print("nome invalido")
palavrasQuant = []
arqInput = open(nome + "//c.txt",'r',encoding = "UTF-8")
linha = arqInput.readline()[:-1].split()
while linha:
    palavrasQuant.append(int(linha[-1]))
    linha = arqInput.readline()[:-1]
palavraStats = arrumaStats(palavrasQuant)
for a in range(1000):
    word = []
    subWorldQuant = choice([b for b in range(1,1+len(palavraStats))],1,p=palavraStats)[0]
    for b in range(subWorldQuant):
        word.append(doAWord(nome,b))
    print(" ".join(word),end='\n')
