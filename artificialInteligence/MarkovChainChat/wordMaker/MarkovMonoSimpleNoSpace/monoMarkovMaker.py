from random import randint


def getAnChar(nome, anterior="¨"):
    file = open(nome, "r", encoding="UTF-8")
    linha = file.readline()
    data = {}
    while linha:
        letras = [linha[a] for a in range(0, 5, 2)]
        if anterior == letras[0]:
            letra = letras[1]
            numero = int(letras[-1])
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
        letra = getAnChar(nome, letra)
    return "".join(texto)


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
for a in range(1000):
    print(doAWord(file_name + "//chain.txt"), end="\n")