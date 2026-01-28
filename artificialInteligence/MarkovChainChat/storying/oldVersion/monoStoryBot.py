from random import randint


def getAWord(isTitle, anterior="¨"):
    if isTitle:
        diretorio = "monoChainTitle"
    else:
        diretorio = "monoChainStory"
    nome = diretorio + "//chain.txt"
    file = open(nome)
    linha = file.readline()
    data = {}
    while linha:
        palavras = linha.split()
        if anterior == palavras[0]:
            palavra = palavras[1]
            numero = int(palavras[-1])
        else:
            linha = file.readline()
            continue
        data[palavra] = numero
        linha = file.readline()
    total = sum(list(data.values()))
    escolhido = randint(1, total)
    soma = 0
    for indice, valor in enumerate(data.values()):
        soma += valor
        if soma >= escolhido:
            file.close()
            return list(data.keys())[indice]


def doATexto(isTitle):
    texto = []
    palavra = getAWord(isTitle)
    while palavra != "¨":
        texto.append(palavra)
        palavra = getAWord(isTitle, palavra)
    return " ".join(texto)


for a in range(10):
    print(doATexto(True) + " : " + doATexto(False), end="\n\n")
