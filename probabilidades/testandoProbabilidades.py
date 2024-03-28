from random import randint
from time import time
import textos

def proximo(numero):
    global POT
    global tamanhoSeed
    proximo=numero**POT
    proximoLista=list(str(proximo))
    while(len(proximoLista)>tamanhoSeed):
        proximoLista.pop(-1)
    return(int(''.join(proximoLista)))
    

def imprime(num):
    global tamanhoSeed
    global indice
    formato="{0:0"+str(tamanhoSeed)+"d}"
    print(formato.format(indice)+" : "+str(num))

def chance(casos):
    global repeticao
    LIMITE=1
    retorno=False
    valores=[0 for a in range(casos)]
    for elemento in repeticao:
        valores[elemento%casos]+=1
    print("")
    print("chance de "+str(casos)+" : ")
    for valor,quant in enumerate(valores):
        if(quant!=0):
            porc=quant*100/len(repeticao)
            print(str(valor)+" : "+str(porc)+"%")
            if(porc<=LIMITE):
                retorno=True
    return(retorno)

POT=5
tamanhoSeed=4
seed=randint(10**(tamanhoSeed-1),10**tamanhoSeed-1)
indice=0
imprime(seed)
num=proximo(seed)
indice+=1
imprime(num)
repeticao=[seed,num]
while True:
    indice+=1
    num=proximo(num)
    imprime(num)
    if(num in repeticao):
        break
    else:
        repeticao.append(num)
for a in range(1,len(repeticao)):
    if(chance(a)):
        break
    

