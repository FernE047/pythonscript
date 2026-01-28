import os
from collections import Counter
from time import time


def embelezeTempo(segundos: float) -> str:
    if segundos < 0:
        segundos = -segundos
        sign = "-"
    else:
        sign = ""
    total_ms = int(round(segundos * 1000))
    ms = total_ms % 1000
    total_s = total_ms // 1000
    s = total_s % 60
    total_min = total_s // 60
    m = total_min % 60
    total_h = total_min // 60
    h = total_h % 24
    d = total_h // 24
    parts: list[str] = []

    def add(value: int, singular: str, plural: str) -> None:
        if value:
            parts.append(f"{value} {singular if value == 1 else plural}")

    add(d, "day", "days")
    add(h, "hour", "hours")
    add(m, "minute", "minutes")
    add(s, "second", "seconds")
    if ms or not parts:
        parts.append(f"{ms} millisecond" if ms == 1 else f"{ms} milliseconds")
    return sign + ", ".join(parts)


def rename_file(source_file_name: str, destination_file_name: str) -> None:
    with (
        open(source_file_name, "r", encoding="utf-8") as source_file,
        open(destination_file_name, "w", encoding="utf-8") as destination_file,
    ):
        content = source_file.read()
        destination_file.write(content)


def alteraMonoChainFile(nome, termos):
    nomeTemp = nome + "//c.txt"
    nomeReal = nome + "//chain.txt"
    fileWrite = open(nomeTemp, "w", encoding="UTF-8")
    amount = Counter([str(a) for a in termos])
    if "chain.txt" in os.listdir(nome):
        fileRead = open(nomeReal, "r", encoding="UTF-8")
        linha = fileRead.readline()
        while linha:
            palavras = linha.split()
            if palavras[:-1] in termos:
                palavras[-1] = int(palavras[-1])
                palavras[-1] += amount[str(palavras[:-1])]
                while palavras[:-1] in termos:
                    termos.remove(palavras[:-1])
                palavras[-1] = str(palavras[-1])
                fileWrite.write(" ".join(palavras) + "\n")
            else:
                fileWrite.write(linha)
            linha = fileRead.readline()
        used = []
        for termo in termos:
            if termo not in used:
                fileWrite.write(" ".join(termo + [str(amount[str(termo)])]) + "\n")
                used.append(termo)
        fileRead.close()
    else:
        used = []
        for termo in termos:
            if termo not in used:
                fileWrite.write(" ".join(termo + [str(amount[str(termo)])]) + "\n")
                used.append(termo)
    fileWrite.close()
    renome(nomeTemp, nomeReal)


notSuccess = True
while notSuccess:
    try:
        print("o que deseja abrir?")
        nome = input()
        file = open(nome + ".txt", "r")  # , encoding = "UTF-8")
        notSuccess = False
        try:
            arqInput = open(nome + "//c.txt", "w", encoding="UTF-8")
            arqInput.close()
        except:
            os.mkdir(nome)
    except:
        print("nome invalido")
inicio = time()
file = open(nome + ".txt", "r", encoding="UTF-8")
linha = file.readline()[:-1]
palavraQuant = []
count = 0
alterations = []
while linha:
    palavras = linha.split()
    while len(palavras) > len(palavraQuant):
        palavraQuant.append(0)
    palavraQuant[len(palavras) - 1] += 1
    for palavra in palavras:
        tamanho = len(palavra)
        letraAnterior = ""
        for index in range(tamanho):
            letra = palavra[index]
            if index == 0:
                alterations.append(["¨", "¨", letra])
                if tamanho == 1:
                    alterations.append(["¨", letra, "¨"])
                    break
                else:
                    letraSeguinte = palavra[index + 1]
                    alterations.append(["¨", letra, letraSeguinte])
                    letraAnterior = letra
                continue
            if tamanho > 1:
                if index >= tamanho - 1:
                    letraSeguinte = "¨"
                else:
                    letraSeguinte = palavra[index + 1]
                alterations.append([letraAnterior, letra, letraSeguinte])
                if letraSeguinte == "¨":
                    break
            letraAnterior = letra
    if count == 100:
        alteraMonoChainFile(nome, alterations)
        alterations = []
        count = 0
    else:
        count += 1
    linha = file.readline()[:-1]
alteraMonoChainFile(nome, alterations)
arqInput = open(nome + "//c.txt", "w", encoding="UTF-8")
for index, quantity in enumerate(palavraQuant):
    arqInput.write(f"{index} ")
    arqInput.write(f"{quantity}\n")
arqInput.close()
print(tamanho)
fim = time()
print(embelezeTempo(fim - inicio))
file.close()
