import os


def rename_file(source_file_name: str, destination_file_name: str) -> None:
    with (
        open(source_file_name, "r", encoding="utf-8") as source_file,
        open(destination_file_name, "w", encoding="utf-8") as destination_file,
    ):
        content = source_file.read()
        destination_file.write(content)

def alteraChainFile(n,termo):
    fileWrite = open("chain//c.txt","w",encoding="utf-8")
    if f"{n:03d}.txt" in os.listdir("chain"):
        fileRead = open(f"chain//{n:03d}.txt","r",encoding="utf-8")
        linha = fileRead.readline()
        encontrou = False
        indice = len(termo)
        while linha:
            palavras = linha.split()
            if palavras[:-1] == termo:
                palavras[-1] = str(int(palavras[-1])+1)
                fileWrite.write( " ".join(palavras) + "\n")
                encontrou = True
            else:
                fileWrite.write(linha)
            linha = fileRead.readline()
        if not encontrou:
            fileWrite.write(" ".join(termo) + " 1\n")
        fileRead.close()
    else :
        fileWrite.write(" ".join(termo) + " 1\n")
    fileWrite.close()
    renome("chain//c.txt",f"chain//{n:03d}.txt")

file = open("sohMensagens.txt",encoding="utf-8")
mensagem = file.readline()
lista = []
while mensagem:
    palavras = mensagem.split()
    tamanho = len(palavras)
    for n in range(tamanho):
        palavra = palavras[n]
        if n == 0:
            alteraChainFile(n,[palavra])
            if tamanho == 1:
                alteraChainFile(n+1,[palavra,"¨"])
                break
        if tamanho > 1:
            if n>=tamanho-1:
                palavraSeguinte = "¨"
            else:
                palavraSeguinte = palavras[n+1]
            alteraChainFile(n+1,[palavra,palavraSeguinte])
            if palavraSeguinte == "¨":
                break
    mensagem = file.readline()
for letra in lista:
    print(letra)
file.close()

