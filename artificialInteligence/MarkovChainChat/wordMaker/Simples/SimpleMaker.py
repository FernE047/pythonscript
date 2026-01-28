from numpy.random import choice
from random import randint


def randomMidVowels():
    global letras
    global vogais
    letrasPossiveis = letras[0:5]
    return choice(letrasPossiveis, 1, p=vogais)[0]


def randomMidCons():
    global letras
    global cons
    letrasPossiveis = letras[5:]
    return choice(letrasPossiveis, 1, p=cons)[0]


def firstLetter():
    global letras
    global beginLetter
    letraAdicional = ""
    letra = choice(letras, 1, p=beginLetter)[0]
    if letra == "q":
        letraAdicional = "u"
    if letra in ["b", "c", "d", "f", "g", "k", "p", "t", "v"]:
        chanceAdicional = choice([0, 1], 1, p=[0.95, 0.05])
        if chanceAdicional:
            letraAdicional = randomMidCons()
            while letraAdicional not in ["l", "r", "h"]:
                letraAdicional = randomMidCons()
    return letra + letraAdicional


def randomEnd(quant, isFirstVowel=True):
    mid = ""
    consoanteAdicional = 0
    for a in range(quant):
        if (bool(a % 2)) == isFirstVowel:
            mid += randomMidVowels()
            consoanteAdicional = 0
        else:
            letra = randomMidCons()
            if letra == "q":
                mid += "qu"
            elif letra in ["l", "s", "r", "y", "w", "z", "x", "n", "m"]:
                if not (consoanteAdicional):
                    consoanteAdicional = choice([0, 1], 1, p=[0.75, 0.25])[0]
                    if consoanteAdicional:
                        isFirstVowel = not (isFirstVowel)
                mid += letra
            else:
                mid += letra
                if letra not in ["h", "j"]:
                    consoanteAdicional = choice([0, 1], 1, p=[0.95, 0.05])
                    if consoanteAdicional:
                        letra = randomMidCons()
                        while letra not in ["l", "r", "h"]:
                            letra = randomMidCons()
                        mid += letra
    return mid


def makeSubWord(tamanhos, tamanhoStats):
    lenght = choice(tamanhos, 1, p=tamanhoStats)[0]
    begin = firstLetter()
    end = randomEnd(lenght - 1, isFirstVowel=(begin in ["a", "e", "i", "o", "u"]))
    return begin + end


def makeWord():
    global palavraQuant
    global palavraStats
    global tamanhos
    global tamanhoStats
    wordsQuant = choice(palavraQuant, 1, p=palavraStats)[0]
    words = []
    for a in range(wordsQuant):
        indice = palavraQuant.index(a + 1)
        tamanhosUsed = tamanhos[indice]
        tamanhoStatsUsed = tamanhoStats[indice]
        words.append(makeSubWord(tamanhosUsed, tamanhoStatsUsed))
    return " ".join(words)


def arrumaStats(lista):
    soma = sum(lista)
    lista = [value / soma for value in lista]
    while sum(lista) != 1:
        if sum(lista) > 1:
            add = sum(lista) - 1
            lista[lista.index(max(lista))] -= add
        elif sum(lista) < 1:
            add = 1 - sum(lista)
            lista[lista.index(min(lista))] += add
    return lista


notSuccess = True
while notSuccess:
    try:
        print("o que deseja abrir?")
        nome = input()
        try:
            arqInput = open(
                "artificialInteligence/MarkovChainChat/wordMaker/Simples/"
                + nome
                + ".txt",
                "r",
                encoding="UTF-8",
            )
        except:
            arqInput = open(nome + ".txt", "r")
        notSuccess = False
    except:
        print("nome invalido")
entrada = [
    "Q",
    "W",
    "E",
    "R",
    "T",
    "Y",
    "U",
    "I",
    "O",
    "P",
    "A",
    "S",
    "D",
    "F",
    "G",
    "H",
    "J",
    "K",
    "L",
    "Z",
    "X",
    "C",
    "V",
    "B",
    "N",
    "M",
    "Á",
    "À",
    "Â",
    "Ã",
    "É",
    "È",
    "Ê",
    "Í",
    "Ì",
    "Î",
    "Ó",
    "Ò",
    "Ô",
    "Õ",
    "Ú",
    "Ù",
    "Û",
    "á",
    "à",
    "â",
    "ã",
    "é",
    "è",
    "ê",
    "í",
    "ì",
    "î",
    "ó",
    "ò",
    "ô",
    "õ",
    "ú",
    "ù",
    "û",
    "ä",
    "ë",
    "ï",
    "ö",
    "ü",
    "Ä",
    "Ë",
    "Ï",
    "Ö",
    "Ü",
    "\n",
    " ",
    "-",
    "ç",
    ",",
    "/",
    "Æ",
]
saida = [
    "q",
    "w",
    "e",
    "r",
    "t",
    "y",
    "u",
    "i",
    "o",
    "p",
    "a",
    "s",
    "d",
    "f",
    "g",
    "h",
    "j",
    "k",
    "l",
    "z",
    "x",
    "c",
    "v",
    "b",
    "n",
    "m",
    "a",
    "a",
    "a",
    "a",
    "e",
    "e",
    "e",
    "i",
    "i",
    "i",
    "o",
    "o",
    "o",
    "o",
    "u",
    "u",
    "u",
    "a",
    "a",
    "a",
    "a",
    "e",
    "e",
    "e",
    "i",
    "i",
    "i",
    "o",
    "o",
    "o",
    "o",
    "u",
    "u",
    "u",
    "a",
    "e",
    "i",
    "o",
    "u",
    "a",
    "e",
    "i",
    "o",
    "u",
    "\n",
    " ",
    " ",
    "c",
    " ",
    " ",
    "ae",
]
letras = [
    "a",
    "e",
    "i",
    "o",
    "u",
    "q",
    "w",
    "r",
    "t",
    "y",
    "p",
    "s",
    "d",
    "f",
    "g",
    "h",
    "j",
    "k",
    "l",
    "z",
    "x",
    "c",
    "v",
    "b",
    "n",
    "m",
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
]
linha = arqInput.readline()
beginLetter = [0 for a in letras]
midLetter = [0 for a in letras]
tamanhos = []
tamanhoStats = []
palavraQuant = []
palavraStats = []
while linha:
    for index, entry in enumerate(entrada):
        linha = linha.replace(entry, saida[index])
    palavras = linha[:-1].split(" ")
    while len(palavras) > len(palavraQuant):
        palavraQuant.append(len(palavraQuant) + 1)
        palavraStats.append(0)
        tamanhos.append([])
        tamanhoStats.append([])
    if len(palavras) in palavraQuant:
        palavraStats[len(palavras) - 1] += 1
    for m, palavra in enumerate(palavras):
        tamanhosUsed = tamanhos[m]
        tamanhoStatsUsed = tamanhoStats[m]
        for n, caracter in enumerate(list(palavra)):
            try:
                if n == 0:
                    beginLetter[letras.index(caracter)] += 1
                else:
                    midLetter[letras.index(caracter)] += 1
            except:
                pass
        tamanho = len(palavra)
        if tamanho not in tamanhosUsed:
            tamanhosUsed.append(tamanho)
            tamanhoStatsUsed.append(1)
        else:
            tamanhoStatsUsed[tamanhosUsed.index(tamanho)] += 1
    linha = arqInput.readline()
beginLetter = arrumaStats(beginLetter)
vogais = arrumaStats(midLetter[0:5])
cons = arrumaStats(midLetter[5:])
for tamanhoStatsUsed in tamanhoStats:
    lista = arrumaStats(tamanhoStatsUsed)
    for index, listaa in enumerate(lista):
        tamanhoStatsUsed[index] = listaa
palavraStats = arrumaStats(palavraStats)
arqInput.close()
notSuccess = True
while notSuccess:
    try:
        print("quantas palavras?")
        numero = int(input())
        if numero >= 0:
            notSuccess = False
    except:
        print("numero invalido")
for a in range(numero):
    print(makeWord())
"""palavras = []
while len(palavras)!= numero:
    continuar = True
    palavra = makeWord()
    print(palavra)
    print("s/n/e")
    escolha = input()
    if escolha == "s":
        palavras.append(palavra)
    elif escolha == "e":
        print("edite")
        palavra = input()
        palavras.append(palavra)
    print()
for palavra in palavras:
    print(" ".join([a.capitalize() for a in palavra.split(" ")]))"""
