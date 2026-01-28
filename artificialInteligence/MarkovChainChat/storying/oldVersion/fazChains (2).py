from time import time
from textos import embelezeTempo as eT
import os

def renome(origemName,destinoName):
    origem = open(origemName,'r')
    destino = open(destinoName,'w')
    linha = origem.readline()
    while linha:
        destino.write(linha)
        linha = origem.readline()
    origem.close()
    destino.close()

def alteraChainFile(termos, tamanhoChain, isTitulo):
    if isTitulo:
        diretorio = "chainTitle//"+str(tamanhoChain)
    else:
        diretorio = "chainStory//"+str(tamanhoChain)
    nomeTemp = diretorio + "//c.txt"
    nomeReal = diretorio + "//chain.txt"
    fileWrite = open(nomeTemp,'w')
    if "chain.txt" in os.listdir(diretorio):
        fileRead = open(nomeReal,'r')
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
    texto = texto.replace('\n',' ')
    texto = texto.replace('\t',' ')
    texto = texto.replace('“', ' " ')
    texto = texto.replace('”', ' " ')
    for spaced in ['.','-',',','!','?','(','—',')',':','...','..','/','\\']:
        texto = texto.replace(spaced, f' {spaced} ')
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
        file = open('historias//' + name)
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
        print("falta : " + eT(duracao*(total-quantia)))
        print()
