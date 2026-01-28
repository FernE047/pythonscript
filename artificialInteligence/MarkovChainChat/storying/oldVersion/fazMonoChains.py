import os


def rename_file(source_file_name: str, destination_file_name: str) -> None:
    with (
        open(source_file_name, "r", encoding="utf-8") as source_file,
        open(destination_file_name, "w", encoding="utf-8") as destination_file,
    ):
        content = source_file.read()
        destination_file.write(content)


def alteraMonoChainFile(termo, isTitulo):
    if isTitulo:
        diretorio = "monoChainTitle"
    else:
        diretorio = "monoChainStory"
    nomeTemp = diretorio + "//c.txt"
    nomeReal = diretorio + "//chain.txt"
    fileWrite = open(nomeTemp, "w")
    if "chain.txt" in os.listdir(diretorio):
        fileRead = open(nomeReal, "r")
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


def fazMonoChain(texto, isTitulo=False):
    palavras = texto.split()
    tamanho = len(palavras)
    for n in range(tamanho):
        palavra = palavras[n]
        if n == 0:
            alteraMonoChainFile(["¨", palavra], isTitulo)
            if tamanho == 1:
                alteraMonoChainFile([palavra, "¨"], isTitulo)
                break
        if tamanho > 1:
            if n >= tamanho - 1:
                palavraSeguinte = "¨"
            else:
                palavraSeguinte = palavras[n + 1]
            alteraMonoChainFile([palavra, palavraSeguinte], isTitulo)
            if palavraSeguinte == "¨":
                break


for name in os.listdir("historias"):
    print(name)
    file = open("historias//" + name)
    elementos = file.readline().split(" : ")
    historia = elementos[-1:][0]
    titulo = ": ".join(elementos[:-1])
    fazMonoChain(titulo, isTitulo=True)
    fazMonoChain(historia)
    file.close()
