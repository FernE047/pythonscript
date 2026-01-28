import os

duracao = open("duracao.txt", "r", encoding="utf8")
duracaoConteudo = duracao.read()
print(len(duracaoConteudo))
for letraPos in range(12, len(duracaoConteudo)):
    duracao = ""
    word = ""
    for retorno in range(11):
        word += duracaoConteudo[letraPos - 10 + retorno]
    if word == "aria-label=":
        letraPos += 2
        while duracaoConteudo[letraPos] != """:
            duracao += duracaoConteudo[letraPos]
            letraPos += 1
        print(duracao)
