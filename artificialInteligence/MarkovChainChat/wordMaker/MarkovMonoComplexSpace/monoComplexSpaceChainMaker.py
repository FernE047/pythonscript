import os

def renome(origemName,destinoName):
    origem = open(origemName,'r',encoding = "UTF-8")
    destino = open(destinoName,'w',encoding = "UTF-8")
    linha = origem.readline()
    while linha:
        destino.write(linha)
        linha = origem.readline()
    origem.close()
    destino.close()

def alteraMonoChainFile(nome,termo,indice):
    nomeTemp = nome + "//c.txt"
    nomeReal = nome + "//{0:03d}.txt".format(indice)
    fileWrite = open(nomeTemp,'w',encoding = "UTF-8")
    if "{0:03d}.txt".format(indice) in os.listdir(nome):
        fileRead = open(nomeReal,'r',encoding = "UTF-8")
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
file = open(nome + '.txt','r')#,encoding = "UTF-8")
linha = file.readline()[:-1]
palavraQuant = []
while linha:
    palavras = linha.split()
    while len(palavras)>len(palavraQuant):
        palavraQuant.append(0)
    palavraQuant[len(palavras)-1] += 1
    for m,palavra in enumerate(palavras):
        tamanho = len(palavra)
        letraAnterior = ""
        for n in range(tamanho):
            letra = palavra[n]
            if n == 0:
                alteraMonoChainFile(nome,["¨","¨",letra],m)
                if tamanho == 1:
                    alteraMonoChainFile(nome,["¨",letra,"¨"],m)
                    break
                else:
                    letraSeguinte = palavra[n+1]
                    alteraMonoChainFile(nome,["¨",letra,letraSeguinte],m)
                    letraAnterior = letra
                continue
            if tamanho > 1:
                if n >= tamanho-1:
                    letraSeguinte = "¨"
                else:
                    letraSeguinte = palavra[n+1]
                alteraMonoChainFile(nome,[letraAnterior,letra,letraSeguinte],m)
                if letraSeguinte == "¨":
                    break
            letraAnterior = letra
    linha = file.readline()[:-1]
arqInput = open(nome+"//c.txt",'w',encoding = "UTF-8")
for n in range(len(palavraQuant)):
    arqInput.write(str(n)+" ")
    arqInput.write(str(palavraQuant[n])+"\n")
arqInput.close()
print(tamanho)
file.close()
