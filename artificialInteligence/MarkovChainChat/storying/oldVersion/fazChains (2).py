from time import time
import os


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

def alteraChainFile(termos, tamanhoChain, isTitulo):
    if isTitulo:
        diretorio = "chainTitle//"+str(tamanhoChain)
    else:
        diretorio = "chainStory//"+str(tamanhoChain)
    nomeTemp = diretorio + "//c.txt"
    nomeReal = diretorio + "//chain.txt"
    fileWrite = open(nomeTemp,"w")
    if "chain.txt" in os.listdir(diretorio):
        fileRead = open(nomeReal,"r")
        linha = fileRead.readline()
        while linha:
            palavras = linha.split()
            termoTestando = " ".join(palavras[:-1])
            while termoTestando in termos:
                palavras[-1] = str(int(palavras[-1])+1)
                termos.remove(termoTestando)
            fileWrite.write(" ".join(palavras) + "\n")
            linha = fileRead.readline()
        fileRead.close()
        if termos:
            for termo in termos:
                fileWrite.write(termo + " 1\n")
    else :
        for termo in termos:
            fileWrite.write(termo + " 1\n")
    fileWrite.close()
    renome(nomeTemp,nomeReal)

def fazChain(texto,tamanhoChain,isTitulo = False):
    texto = texto.replace("\n"," ")
    texto = texto.replace("\t"," ")
    texto = texto.replace("“", " " ")
    texto = texto.replace("”", " " ")
    for spaced in [".","-",",","!","?","(","—",")",":","...","..","/","\\"]:
        texto = texto.replace(spaced, f" {spaced} ")
    palavras = texto.split()
    tamanhoTexto = len(palavras)
    listaDePares = []
    termo = " ".join(["¨" for a in range(tamanhoChain)]+[palavras[0]])
    listaDePares.append(termo)
    for n in range(tamanhoTexto):
        termos = palavras[n : n + tamanhoChain + 1]
        if len(termos) <= tamanhoChain :
            while len(termos) <= tamanhoChain :
                termos.append("¨")
            termo = " ".join(termos)
            listaDePares.append(termo)
            break
        termo = " ".join(termos)
        listaDePares.append(termo)
    alteraChainFile(listaDePares, tamanhoChain, isTitulo)

tamanho = 2
total = len(os.listdir("historias"))
for tamanho in range(2,3):
    quantia = 0
    for name in os.listdir("historias"):
        quantia += 1
        inicio = time()
        print(name)
        file = open("historias//" + name)
        elementos = file.readline().split(" : ")
        if elementos[:-1]:
            titulo = " : ".join(elementos[:-1])
            fazChain(titulo,tamanho,isTitulo = True)
        if elementos[-1:][0]:
            historia = elementos[-1:][0]
            fazChain(historia,tamanho)
        file.close()
        final = time()
        duracao = final - inicio
        print("falta : " + embelezeTempo(duracao*(total-quantia)))
        print()
