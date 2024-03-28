import os
from collections import Counter
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
    amount = Counter([str(a) for a in termos])
    if "chain.txt" in os.listdir(nome):
        fileRead = open(nomeReal,'r',encoding = "UTF-8")
        linha = fileRead.readline()
        while linha:
            palavras = linha.split()
            if palavras[:-1] in termos:
                palavras[-1] = int(palavras[-1])
                palavras[-1] += amount[str(palavras[:-1])]
                while palavras[:-1] in termos:
                    termos.remove(palavras[:-1])
                palavras[-1] = str(palavras[-1])
                fileWrite.write( " ".join(palavras) + "\n")
            else:
                fileWrite.write(linha)
            linha = fileRead.readline()
        used = []
        for termo in termos:
            if termo not in used:
                fileWrite.write(" ".join(termo+[str(amount[str(termo)])]) + "\n")
                used.append(termo)
        fileRead.close()
    else :
        used = []
        for termo in termos:
            if termo not in used:
                fileWrite.write(" ".join(termo+[str(amount[str(termo)])]) + "\n")
                used.append(termo)
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
linha = file.readline()[:-1]
palavraQuant = []
count = 0
alterations = []
while linha:
    palavras = linha.split()
    while len(palavras)>len(palavraQuant):
        palavraQuant.append(0)
    palavraQuant[len(palavras)-1] += 1
    for palavra in palavras:
        tamanho = len(palavra)
        letraAnterior = ""
        for n in range(tamanho):
            letra = palavra[n]
            if n == 0:
                alterations.append(["¨","¨",letra])
                if tamanho == 1:
                    alterations.append(["¨",letra,"¨"])
                    break
                else:
                    letraSeguinte = palavra[n+1]
                    alterations.append(["¨",letra,letraSeguinte])
                    letraAnterior = letra
                continue
            if tamanho > 1:
                if n >= tamanho-1:
                    letraSeguinte = "¨"
                else:
                    letraSeguinte = palavra[n+1]
                alterations.append([letraAnterior,letra,letraSeguinte])
                if letraSeguinte == "¨":
                    break
            letraAnterior = letra
    if count == 100:
        alteraMonoChainFile(nome,alterations)
        alterations = []
        count = 0
    else:
        count += 1
    linha = file.readline()[:-1]
alteraMonoChainFile(nome,alterations)
arqInput = open(nome+"//c.txt",'w',encoding = "UTF-8")
for n in range(len(palavraQuant)):
    arqInput.write(str(n)+" ")
    arqInput.write(str(palavraQuant[n])+"\n")
arqInput.close()
print(tamanho)
fim = time()
print(embelezeTempo(fim-inicio))
file.close()
