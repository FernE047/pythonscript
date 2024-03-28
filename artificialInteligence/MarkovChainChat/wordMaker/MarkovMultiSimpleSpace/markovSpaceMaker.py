from random import randint
from numpy.random import choice

def getAnChar(nome,indice,indiceEspaco,anterior = ''):
    nome += "//{0:03d}.txt"
    file = open(nome.format(indice),encoding='utf-8')
    linha = file.readline()
    data = {}
    while linha:
        if int(linha[0]) == indiceEspaco:
            if indice == 0:
                letra = linha[2]
                numero = int(linha[4:-1])
            else:
                if anterior == linha[2]:
                    letra = linha[4]
                    numero = int(linha[6:-1])
                else:
                    linha = file.readline()
                    continue
            data[letra] = numero
        linha = file.readline()
    #print(anterior)
    #print(data)
    #print(indice)
    #print(indiceEspaco)
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
    letra = getAnChar(nome,0,indiceEspaco)
    while letra != "¨":
        mensagem += letra
        letra = getAnChar(nome,len(mensagem),indiceEspaco,letra)
    return mensagem

def arrumaStats(lista):
    lista = [lista[a]/sum(lista) for a in range(len(lista))]
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
    #print(subWorldQuant)
    for b in range(subWorldQuant):
        #print(b)
        word.append(doAWord(nome,b))
    print(" ".join(word),end='\n')
