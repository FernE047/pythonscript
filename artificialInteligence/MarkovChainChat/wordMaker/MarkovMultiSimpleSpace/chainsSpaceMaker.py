import os

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

def alteraChainFile(nome,n,termo):
    fileWrite = open(nome+"//c.txt",'w',encoding = "UTF-8")
    if "{0:03d}.txt".format(n) in os.listdir(nome):
        fileRead = open(nome+"//{0:03d}.txt".format(n),'r',encoding = "UTF-8")
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
    renome(nome,"//{0:03d}.txt".format(n))

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
mensagem = file.readline()[1:-1]
palavraQuant = []
while mensagem:
    palavras = mensagem.split()
    while len(palavras)>len(palavraQuant):
        palavraQuant.append(0)
    palavraQuant[len(palavras)-1] += 1
    for m,palavra in enumerate(palavras):
        tamanho = len(palavra)
        for n in range(tamanho):
            letra = palavra[n]
            if n == 0:
                '''if letra == "\n":
                    letra = "¨"'''
                alteraChainFile(nome,n," ".join([str(m),letra]))
                if tamanho == 1:
                    alteraChainFile(nome,n+1," ".join([str(m),letra,"¨"]))
            if tamanho > 1:
                try:
                    letraSeguinte = palavra[n+1]
                except:
                    letraSeguinte = "¨"
                if letraSeguinte == "\n":
                    letraSeguinte = "¨"
                alteraChainFile(nome,n+1," ".join([str(m),letra,letraSeguinte]))
                if letraSeguinte == "¨":
                    break
    mensagem = file.readline()[:-1]
arqInput = open(nome+"//c.txt",'w',encoding = "UTF-8")
for n in range(len(palavraQuant)):
    arqInput.write(str(n)+" ")
    arqInput.write(str(palavraQuant[n])+"\n")
arqInput.close()
print(tamanho)
file.close()

