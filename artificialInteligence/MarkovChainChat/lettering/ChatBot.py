from random import randint


def getAnChar(indice, anterior=""):
    nome = "chain//{0:03d}.txt"
    file = open(nome.format(indice), encoding="utf-8")
    linha = file.readline()
    data = {}
    while linha:
        if indice == 0:
            letra = linha[0]
            numero = int(linha[2:-1])
        else:
            if anterior == linha[0]:
                letra = linha[2]
                numero = int(linha[4:-1])
            else:
                linha = file.readline()
                continue
        data[letra] = numero
        linha = file.readline()
    total = sum(list(data.values()))
    escolhido = randint(1, total)
    soma = 0
    for indice, valor in enumerate(data.values()):
        soma += valor
        if soma >= escolhido:
            file.close()
            return list(data.keys())[indice]


def doAMessage():
    mensagem = ""
    letra = getAnChar(0)
    while letra != "¨":
        mensagem += letra
        letra = getAnChar(len(mensagem), letra)
    return mensagem


for a in range(1000):
    print(str(a) + " : " + doAMessage())
