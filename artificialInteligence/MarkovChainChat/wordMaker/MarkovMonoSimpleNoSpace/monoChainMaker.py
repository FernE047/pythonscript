import os
from time import time
from textos import embelezeTempo

def renome(origemName,destinoName):
    origem = open(origemName,'r',encoding = "UTF-8")
    destino = open(destinoName,'w',encoding = "UTF-8")
    linha = origem.readline()
    while linha:
        destino.write(linha)
        linha = origem.readline()
    origem.close()
    destino.close()

def alteraMonoChainFile(nome,termos):
    nomeTemp = nome + "//c.txt"
    nomeReal = nome + "//chain.txt"
    fileWrite = open(nomeTemp,'w',encoding = "UTF-8")
    if "chain.txt" in os.listdir(nome):
        fileRead = open(nomeReal,'r',encoding = "UTF-8")
        linha = fileRead.readline()
        while linha:
            palavras = linha.split()
            if palavras[:-1] in termos:
                palavras[-1] = int(palavras[-1])
                while palavras[:-1] in termos:
                    palavras[-1] += 1
                    termos.remove(palavras[:-1])
                palavras[-1] = str(palavras[-1])
                fileWrite.write( " ".join(palavras) + "\n")
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
    renome(nomeTemp,nomeReal)

notSuccess = True
while notSuccess:
    try:
        print("o que deseja abrir?")
        nome = input()
        file = open(nome + '.txt','r')#, encoding = "UTF-8")
        notSuccess = False
        try:
            arqInput = open(nome+"//c.txt",'w',encoding = "UTF-8")
            arqInput.close()
        except:
            os.mkdir(nome)
    except:
        print("nome invalido")
inicio = time()
file = open(nome + '.txt','r',encoding = "UTF-8")
linha = file.readline()[1:-1]
while linha:
    tamanho = len(linha)
    alterations = []
    for n in range(tamanho):
        palavra = linha[n]
        if n == 0:
            alterations.append(["¨",palavra])
            if tamanho == 1:
                alterations.append([palavra,"¨"])
                break
        if tamanho > 1:
            if n>=tamanho-1:
                palavraSeguinte = "¨"
            else:
                palavraSeguinte = linha[n+1]
            alterations.append([palavra,palavraSeguinte])
            if palavraSeguinte == "¨":
                break
    alteraMonoChainFile(nome,alterations)
    linha = file.readline()[:-1]
print(tamanho)
fim = time()
print(embelezeTempo(fim-inicio))
file.close()

