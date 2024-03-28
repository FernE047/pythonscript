from random import randint

def getAWord(indice,isTitle,anterior = ''):
    if isTitle:
        diretorio = "chainTitle//0"
    else:
        diretorio = "chainStory//0"
    nome = diretorio + "//{0:03d}.txt"
    file = open(nome.format(indice))
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

def doATexto(isTitle):
    texto = []
    palavra = getAWord(0,isTitle)
    while palavra != "¨":
        texto.append(palavra)
        palavra = getAWord(len(texto),isTitle,palavra)
    return " ".join(texto)

for a in range(10):
    print(doATexto(True)+" : "+doATexto(False),end='\n\n')
