from random import randint

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

notSuccess = True
while notSuccess:
    try:
        print("o que deseja abrir?")
        nome = input() + "//chain.txt"
        try:
            arqInput = open(nome,'r',encoding = "UTF-8")
            arqInput.close()
        except:
            pass
        notSuccess = False
    except:
        print("nome invalido")
for a in range(1000):
    print(doAWord(nome),end='\n')
