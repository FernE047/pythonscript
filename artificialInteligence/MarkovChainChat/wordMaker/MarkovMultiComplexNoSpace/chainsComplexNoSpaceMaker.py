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




def rename_file(source_file_name:str, destination_file_name:str) -> None:
    with open(source_file_name, "r", encoding="utf-8") as source_file, open(destination_file_name, "w", encoding="utf-8") as destination_file:
        content = source_file.read()
        destination_file.write(content)


def alteraChainFile(nome, n, termos):
    fileWrite = open(f"{nome}//c.txt", "w", encoding="UTF-8")
    amount = Counter([str(a) for a in termos])
    if f"{n:03d}.txt" in os.listdir(nome):
        fileRead = open(f"{nome}//{n:03d}.txt", "r", encoding="UTF-8")
        linha = fileRead.readline()[:-1]
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
                fileWrite.write(linha + "\n")
            linha = fileRead.readline()[:-1]
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
    renome(nome, f"//{n:03d}.txt")


def alteraFiles(nome, alterations):
    for n in alterations:
        alteraChainFile(nome, n, alterations[n])


is_file_name_valid = False
file_name = "default"
while not is_file_name_valid:
    try:
        print("type the file name (without .txt): ")
        file_name = input()
        with open(f"{file_name}.txt", "r", encoding="UTF-8") as file:
            is_file_name_valid = True
            try:
                with open(f"{file_name}/c.txt", "r", encoding="UTF-8") as file_input:
                    file_input = open(f"{file_name}/c.txt", "w", encoding="UTF-8")
            except Exception as _:
                os.mkdir(file_name)
    except Exception as _:
        print("invalid name")
inicio = time()
mensagem = file.readline()[1:-1]
count = 0
alterations = {}
palavraQuant = []
while mensagem:
    palavras = mensagem.split()
    while len(palavras) > len(palavraQuant):
        palavraQuant.append(0)
    palavraQuant[len(palavras) - 1] += 1
    for palavra in palavras:
        tamanho = len(palavra)
        letraAnterior = ""
        for n in range(tamanho):
            letra = palavra[n]
            if n == 0:
                if n not in alterations:
                    alterations[n] = [[letra]]
                else:
                    alterations[n].append([letra])
                if tamanho == 1:
                    if n + 1 not in alterations:
                        alterations[n + 1] = [[letra, "¨"]]
                    else:
                        alterations[n + 1].append([letra, "¨"])
                    break
                else:
                    letraSeguinte = palavra[n + 1]
                    if n + 1 not in alterations:
                        alterations[n + 1] = [[letra, letraSeguinte]]
                    else:
                        alterations[n + 1].append([letra, letraSeguinte])
                    letraAnterior = letra
                continue
            if tamanho > 1:
                try:
                    letraSeguinte = palavra[n + 1]
                except:
                    letraSeguinte = "¨"
                if n + 1 not in alterations:
                    alterations[n + 1] = [[letraAnterior, letra, letraSeguinte]]
                else:
                    alterations[n + 1].append([letraAnterior, letra, letraSeguinte])
                if letraSeguinte == "¨":
                    break
            letraAnterior = letra
    if count == 100:
        alteraFiles(nome, alterations)
        alterations = {}
        count = 0
    else:
        count += 1
    mensagem = file.readline()[:-1]
alteraFiles(nome, alterations)
arqInput = open(nome + "//c.txt", "w", encoding="UTF-8")
for index, quantity in enumerate(palavraQuant):
    arqInput.write(f"{index} ")
    arqInput.write(f"{quantity}\n")
arqInput.close()
print(tamanho)
fim = time()
print(embelezeTempo(fim - inicio))
file.close()
