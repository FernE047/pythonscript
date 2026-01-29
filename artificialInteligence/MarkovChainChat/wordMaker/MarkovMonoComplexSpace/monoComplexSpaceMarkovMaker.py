from random import randint
from numpy.random import choice


def getAnChar(nome, anterior=""):
    if not anterior:
        anterior = []
    while len(anterior) != 2:
        anterior = ["¨"] + anterior
    file = open(nome, "r", encoding="UTF-8")
    linha = file.readline()
    data = {}
    while linha:
        letras = [linha[a] for a in range(0, 5, 2)]
        if anterior == letras[:2]:
            letra = letras[2]
            numero = int(linha[6:-1])
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


def doAWord(nome):
    texto = []
    letra = getAnChar(nome)
    while letra != "¨":
        texto.append(letra)
        letra = getAnChar(nome, texto[-2:])
    return "".join(texto)


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


def get_file_name() -> str:
    is_file_name_valid = True
    file_name = "default"
    while is_file_name_valid:
        print("type the file name (without .txt): ")
        file_name = input()
        try:
            with open(f"{file_name}.txt", "r", encoding="UTF-8") as _:
                pass
        except Exception as _:
            print("invalid name")
        is_file_name_valid = False
    return file_name


file_name = get_file_name()
palavrasQuant = []
arqInput = open(file_name + "//c.txt", "r", encoding="UTF-8")
linha = arqInput.readline()[:-1].split()
while linha:
    palavrasQuant.append(int(linha[-1]))
    linha = arqInput.readline()[:-1]
palavraStats = arrumaStats(palavrasQuant)
for a in range(1000):
    word = []
    subWorldQuant = choice(
        [b for b in range(1, len(palavraStats) + 1)], 1, p=palavraStats
    )[0]
    for b in range(subWorldQuant):
        word.append(doAWord(f"{file_name}//{b:03d}.txt"))
    print(" ".join(word), end="\n")
