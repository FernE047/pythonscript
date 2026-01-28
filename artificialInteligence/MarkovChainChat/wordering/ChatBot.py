from random import randint

def getAWord(indice,anterior = ""):
    nome = "chain//{0:03d}.txt"
    file = open(nome.format(indice),encoding="utf-8")
    linha = file.readline()
    data = {}
    while linha:
        palavras = linha.split()
        if indice == 0:
            palavra = palavras[0]
            numero = int(palavras[-1])
        else:
            if anterior == palavras[0]:
                palavra = palavras[1]
                numero = int(palavras[-1])
            else:
                linha = file.readline()
                continue
        data[palavra] = numero
        linha = file.readline()
    total = sum(list(data.values()))
    escolhido = randint(1,total)
    soma = 0
    for indice,valor in enumerate(data.values()):
        soma += valor
        if soma >= escolhido:
            file.close()
            return list(data.keys())[indice]

def doAMessage():
    mensagem = []
    palavra = getAWord(0)
    while palavra != "¨":
        mensagem.append(palavra)
        palavra = getAWord(len(mensagem),palavra)
    return " ".join(mensagem)

for a in range(1000):
    print(str(a)+" : "+doAMessage())
