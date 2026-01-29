from random import randint


def getAnChar(nome, indice, anterior=""):
    nome += "//{0:03d}.txt"
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


def doAWord(nome):
    mensagem = ""
    letra = getAnChar(nome, 0)
    while letra != "¨":
        mensagem += letra
        letra = getAnChar(nome, len(mensagem), letra)
    return mensagem


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
    print(str(a) + " : " + doAWord(file_name))
