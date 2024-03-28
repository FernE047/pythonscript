import os

def renome(origemName,destinoName):
    origem = open(origemName,'r',encoding='utf-8')
    destino = open(destinoName,'w',encoding='utf-8')
    linha = origem.readline()
    while linha:
        destino.write(linha)
        linha = origem.readline()
    origem.close()
    destino.close()

def alteraChainFile(n,termo):
    if termo == "":
        print(n)
    fileWrite = open("chain//c.txt",'w',encoding='utf-8')
    if "{0:03d}.txt".format(n) in os.listdir("chain"):
        fileRead = open("chain//{0:03d}.txt".format(n),'r',encoding='utf-8')
        linha = fileRead.readline()
        encontrou = False
        indice = len(termo)
        while linha:
            if linha[:indice] == termo:
                numero = int(linha[indice+1:])+1
                fileWrite.write( linha[:indice+1] + str(numero) + "\n")
                encontrou = True
            else:
                fileWrite.write(linha)
            linha = fileRead.readline()
        if not encontrou:
            fileWrite.write(termo + " 1\n")
        fileRead.close()
    else :
        fileWrite.write(termo + " 1\n")
    fileWrite.close()
    renome("chain//c.txt","chain//{0:03d}.txt".format(n))

file = open('sohMensagens.txt',encoding='utf-8')
mensagem = file.readline()[1:]
lista = []
while mensagem:
    tamanho = len(mensagem)
    for n in range(tamanho):
        letra = mensagem[n]
        if n == 0:
            if letra == "\n":
                letra = "¨"
            if letra == "<":
                letra = "~"
                alteraChainFile(n,letra)
                alteraChainFile(n+1,letra+" ¨")
                break
            alteraChainFile(n,letra)
        if tamanho > 1:
            try:
                letraSeguinte = mensagem[n+1]
            except:
                letraSeguinte = "¨"
            if letraSeguinte == "\n":
                letraSeguinte = "¨"
            alteraChainFile(n+1,letra+" "+letraSeguinte)
            if letraSeguinte == "¨":
                break
    mensagem = file.readline()
for letra in lista:
    print(letra)
file.close()

