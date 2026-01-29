import os
from time import time


def format_elapsed_time(seconds: float) -> str:
    if seconds < 0:
        seconds = -seconds
        sign = "-"
    else:
        sign = ""
    total_ms = int(round(seconds * 1000))
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
    if "chain.txt" in os.listdir(nome):
        fileRead = open(nomeReal, "r", encoding="UTF-8")
        linha = fileRead.readline()
        while linha:
            palavras = linha.split()
            if palavras[:-1] in termos:
                palavras[-1] = int(palavras[-1])
                while palavras[:-1] in termos:
                    palavras[-1] += 1
                    termos.remove(palavras[:-1])
                palavras[-1] = str(palavras[-1])
                fileWrite.write(" ".join(palavras) + "\n")
            else:
                fileWrite.write(linha)
            linha = fileRead.readline()
        for termo in termos:
            fileWrite.write(" ".join(termo) + " 1\n")
        fileRead.close()
    else:
        for termo in termos:
            fileWrite.write(" ".join(termo) + " 1\n")
    fileWrite.close()
    rename_file(nomeTemp, nomeReal)


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
file = open(nome + ".txt", "r", encoding="UTF-8")
linha = file.readline()[1:-1]
while linha:
    tamanho = len(linha)
    alterations = []
    for n in range(tamanho):
        palavra = linha[n]
        if n == 0:
            alterations.append(["¨", palavra])
            if tamanho == 1:
                alterations.append([palavra, "¨"])
                break
        if tamanho > 1:
            if n >= tamanho - 1:
                palavraSeguinte = "¨"
            else:
                palavraSeguinte = linha[n + 1]
            alterations.append([palavra, palavraSeguinte])
            if palavraSeguinte == "¨":
                break
    alteraMonoChainFile(nome, alterations)
    linha = file.readline()[:-1]
print(tamanho)
fim = time()
print(format_elapsed_time(fim - inicio))
file.close()
