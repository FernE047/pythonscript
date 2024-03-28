from random import randint
from numpy.random import choice

def getAnChar(nome,anterior = '¨'):
    file = open(nome,'r',encoding = "UTF-8")
    linha = file.readline()
    data = {}
    while linha:
        letras = [linha[a] for a in range(0,5,2)]
        if anterior == letras[0]:
            letra = letras[1]
            numero = int(letras[-1])
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

def doAWord(nome):
    texto = []
    letra = getAnChar(nome)
    while letra != "¨":
        texto.append(letra)
        letra = getAnChar(nome,letra)
    return "".join(texto)

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
            arqInput = open(nome + "//c.txt",'r',encoding = "UTF-8")
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
    subWorldQuant = choice([b for b in range(1,len(palavraStats)+1)],1,p=palavraStats)[0]
    for b in range(subWorldQuant):
        word.append(doAWord(nome + "//{0:03d}.txt".format(b)))
    print(" ".join(word),end='\n')
