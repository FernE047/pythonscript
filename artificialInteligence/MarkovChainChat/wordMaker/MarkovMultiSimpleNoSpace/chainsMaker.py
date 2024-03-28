import os
from collections import Counter
from time import time
from textos import embelezeTempo

def renome(name,destinoName):
    global enc
    origem = open(nome+"//c.txt",'r',encoding = "UTF-8")
    destino = open(nome+destinoName,'w',encoding = "UTF-8")
    linha = origem.readline()
    while linha:
        destino.write(linha)
        linha = origem.readline()
    origem.close()
    destino.close()

def alteraChainFile(nome,n,termos):
    fileWrite = open(nome+"//c.txt",'w',encoding = "UTF-8")
    amount = Counter([str(a) for a in termos])
    if "{0:03d}.txt".format(n) in os.listdir(nome):
        fileRead = open(nome+"//{0:03d}.txt".format(n),'r',encoding = "UTF-8")
        linha = fileRead.readline()[:-1]
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
                fileWrite.write(linha + "\n")
            linha = fileRead.readline()[:-1]
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
    renome(nome,"//{0:03d}.txt".format(n))

def alteraFiles(nome,alterations):
    for n in alterations:
        alteraChainFile(nome,n,alterations[n])

notSuccess = True
while notSuccess:
    try:
        print("o que deseja abrir?")
        nome = input()
        file = open(nome + '.txt','r', encoding = "UTF-8")
        notSuccess = False
        try:
            arqInput = open(nome+"//c.txt",'w',encoding = "UTF-8")
            arqInput.close()
        except:
            os.mkdir(nome)
    except:
        print("nome invalido")
inicio = time()
mensagem = file.readline()[1:-1]
count = 0
alterations = {}
while mensagem:
    tamanho = len(mensagem)
    for n in range(tamanho):
        letra = mensagem[n]
        if n == 0:
            if n not in alterations:
                alterations[n] = [[letra]]
            else:
                alterations[n].append([letra])
        if tamanho > 1:
            try:
                letraSeguinte = mensagem[n+1]
            except:
                letraSeguinte = "¨"
            if n+1 not in alterations:
                alterations[n+1] = [[letra,letraSeguinte]]
            else:
                alterations[n+1].append([letra,letraSeguinte])
            if letraSeguinte == "¨":
                break
    if count == 100:
        alteraFiles(nome,alterations)
        alterations = {}
        count = 0
    else:
        count += 1
    mensagem = file.readline()[:-1]
alteraFiles(nome,alterations)
print(tamanho)
fim = time()
print(embelezeTempo(fim-inicio))
file.close()
