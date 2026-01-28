from random import randint


def getABegining(isTitle):
    palavraInicial = getAWord(isTitle)
    if isTitle:
        diretorio = DIRECTORY + "chainTitle//" + str(TAMANHO)
    else:
        diretorio = DIRECTORY + "chainStory//" + str(TAMANHO)
    nome = diretorio + "//chain.txt"
    file = open(nome)
    linha = file.readline().lower()
    data = {}
    while linha:
        palavras = linha.split()
        if palavraInicial == palavras[0]:
            palavraUsaveis = palavras[1:-1]
            numero = int(palavras[-1])
        else:
            linha = file.readline().lower()
            continue
        palavra = " ".join(palavraUsaveis)
        if palavra not in data.keys():
            data[palavra] = numero
        else:
            data[palavra] += numero
        linha = file.readline().lower()
    total = sum(list(data.values()))
    escolhido = randint(1, total)
    soma = 0
    for indice, valor in enumerate(data.values()):
        soma += valor
        if soma >= escolhido:
            file.close()
            return [palavraInicial] + list(data.keys())[indice].split()


def getAWord(isTitle, anteriores="¨"):
    if anteriores == "¨":
        anteriores = ["¨" for a in range(TAMANHO)]
    if isTitle:
        diretorio = DIRECTORY + "chainTitle//" + str(TAMANHO)
    else:
        diretorio = DIRECTORY + "chainStory//" + str(TAMANHO)
    anterior = " ".join(anteriores)
    nome = diretorio + "//chain.txt"
    file = open(nome)
    linha = file.readline().lower()
    data = {}
    while linha:
        palavras = linha.split()
        palavraTeste = " ".join(palavras[:-2])
        if anterior == palavraTeste:
            palavra = palavras[-2]
            numero = int(palavras[-1])
        else:
            linha = file.readline().lower()
            continue
        if palavra not in data.keys():
            data[palavra] = numero
        else:
            data[palavra] += numero
        linha = file.readline().lower()
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
    palavras = getABegining(isTitle)
    for palavra in palavras[:-1]:
        if palavra == "¨":
            return " ".join(texto)
        texto.append(palavra)
        print(palavra, end=" ")
    palavra = palavras[-1]
    indice = 1
    while palavra != "¨":
        texto.append(palavra)
        print(palavra, end=" ")
        palavra = getAWord(isTitle, texto[indice : indice + TAMANHO])
        indice += 1
    return ""  # " ".join(texto)


DIRECTORY = (
    "C:\\pythonscript\\artificialInteligence\\MarkovChainChat\\storying\\FanficAnime\\"
)
TAMANHO = 1
for a in range(1000):
    doATexto(True)
    print(" : ", end="")
    doATexto(False)
    print("\n")
