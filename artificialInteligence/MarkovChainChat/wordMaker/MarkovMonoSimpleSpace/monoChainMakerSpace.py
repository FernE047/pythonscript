import os


def rename_file(source_file_name: str, destination_file_name: str) -> None:
    with (
        open(source_file_name, "r", encoding="utf-8") as source_file,
        open(destination_file_name, "w", encoding="utf-8") as destination_file,
    ):
        content = source_file.read()
        destination_file.write(content)


def alteraMonoChainFile(nome, termo, indice):
    nomeTemp = f"{nome}//c.txt"
    nomeReal = f"{nome}//{indice:03d}.txt"
    fileWrite = open(nomeTemp, "w", encoding="UTF-8")
    if f"{indice:03d}.txt" in os.listdir(nome):
        fileRead = open(nomeReal, "r", encoding="UTF-8")
        linha = fileRead.readline()
        encontrou = False
        indice = len(termo)
        while linha:
            palavras = linha.split()
            if palavras[:-1] == termo:
                palavras[-1] = str(int(palavras[-1]) + 1)
                fileWrite.write(" ".join(palavras) + "\n")
                encontrou = True
            else:
                fileWrite.write(linha)
            linha = fileRead.readline()
        if not encontrou:
            fileWrite.write(" ".join(termo) + " 1\n")
        fileRead.close()
    else:
        fileWrite.write(" ".join(termo) + " 1\n")
    fileWrite.close()
    renome(nomeTemp, nomeReal)


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
linha = file.readline()[:-1]
palavraQuant = []
while linha:
    palavras = linha.split()
    while len(palavras) > len(palavraQuant):
        palavraQuant.append(0)
    palavraQuant[len(palavras) - 1] += 1
    for m, palavra in enumerate(palavras):
        tamanho = len(palavra)
        for n in range(tamanho):
            letra = palavra[n]
            if n == 0:
                alteraMonoChainFile(nome, ["¨", letra], m)
                if tamanho == 1:
                    alteraMonoChainFile(nome, [letra, "¨"], m)
                    break
            if tamanho > 1:
                if n >= tamanho - 1:
                    letraSeguinte = "¨"
                else:
                    letraSeguinte = palavra[n + 1]
                alteraMonoChainFile(nome, [letra, letraSeguinte], m)
                if letraSeguinte == "¨":
                    break
    linha = file.readline()[:-1]
arqInput = open(nome + "//c.txt", "w", encoding="UTF-8")
for index, quantity in enumerate(palavraQuant):
    arqInput.write(f"{index} ")
    arqInput.write(f"{quantity}\n")
arqInput.close()
print(tamanho)
file.close()
