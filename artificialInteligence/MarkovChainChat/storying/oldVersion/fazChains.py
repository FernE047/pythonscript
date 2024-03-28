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

def alteraChainFile(n,termo,isTitulo):
    if isTitulo:
        diretorio = "chainTitle//0"
    else:
        diretorio = "chainStory//0"
    nomeTemp = diretorio + "//c.txt"
    nomeReal = diretorio + "//{0:03d}.txt"
    fileWrite = open(nomeTemp,'w')
    if "{0:03d}.txt".format(n) in os.listdir(diretorio):
        fileRead = open(nomeReal.format(n),'r')
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
    renome(nomeTemp,nomeReal.format(n))

def fazChain(texto,isTitulo = False):
    palavras = texto.split()
    tamanho = len(palavras)
    for n in range(tamanho):
        palavra = palavras[n]
        if n == 0:
            alteraChainFile(n,[palavra],isTitulo)
            if tamanho == 1:
                alteraChainFile(n+1,[palavra,"¨"],isTitulo)
                break
        if tamanho > 1:
            if n>=tamanho-1:
                palavraSeguinte = "¨"
            else:
                palavraSeguinte = palavras[n+1]
            alteraChainFile(n+1,[palavra,palavraSeguinte],isTitulo)
            if palavraSeguinte == "¨":
                break

for name in os.listdir("historias"):
    print(name)
    file = open('historias//' + name)
    elementos = file.readline().split(" : ")
    historia = elementos[-1:][0]
    titulo = ": ".join(elementos[:-1])
    fazChain(titulo,isTitulo = True)
    fazChain(historia)
    file.close()

