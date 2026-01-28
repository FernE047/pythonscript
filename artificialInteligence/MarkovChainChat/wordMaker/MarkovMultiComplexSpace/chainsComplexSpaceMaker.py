import os

def renome(name,destinoName):
    global enc
    origem = open(f"{name}//c.txt",'r',encoding = "UTF-8")
    destino = open(f"{name}{destinoName}",'w',encoding = "UTF-8")
    linha = origem.readline()
    while linha:
        destino.write(linha)
        linha = origem.readline()
    origem.close()
    destino.close()

def alteraChainFile(nome,n,termo):
    fileWrite = open(f"{nome}//c.txt",'w',encoding = "UTF-8")
    if f"{n:03d}.txt" in os.listdir(nome):
        fileRead = open(f"{nome}//{n:03d}.txt",'r',encoding = "UTF-8")
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
    renome(nome,f"//{n:03d}.txt")

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
        letraAnterior = ""
        for n in range(tamanho):
            letra = palavra[n]
            if n == 0:
                alteraChainFile(nome,n," ".join([str(m),letra]))
                if tamanho == 1:
                    alteraChainFile(nome,n+1," ".join([str(m),letra,"¨"]))
                    break
                else:
                    letraSeguinte = palavra[n+1]
                    alteraChainFile(nome,n+1," ".join([str(m),letra,letraSeguinte]))
                    letraAnterior = letra
                continue
            if tamanho > 1:
                try:
                    letraSeguinte = palavra[n+1]
                except:
                    letraSeguinte = "¨"
                alteraChainFile(nome,n+1," ".join([str(m),letraAnterior,letra,letraSeguinte]))
                if letraSeguinte == "¨":
                    break
            letraAnterior = letra
    mensagem = file.readline()[:-1]
arqInput = open(nome+"//c.txt",'w',encoding = "UTF-8")
for index, quantity in enumerate(palavraQuant):
    arqInput.write(f"{index} ")
    arqInput.write(f"{quantity}\n")
arqInput.close()
print(tamanho)
file.close()

