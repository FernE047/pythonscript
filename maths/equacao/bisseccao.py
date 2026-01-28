from userUtil import pegaInteiro
import numpy as np
from typing import Literal

def pegaFloat(mensagem: str, valorPadrao: float | Literal["."]) -> float | Literal["."]:
    while True:
        entrada=input(f'{mensagem} (padrão: {valorPadrao}) : ')
        if(entrada==""):
            return valorPadrao
        try:
            return float(entrada)
        except Exception as _:
            print("valor inválido, tente novamente")

def entradaDeCoeficientes():
    n=0
    coeficientes=[]
    while True:
        valor=pegaFloat("digite o coeficiente de x^"+str(n),".")
        if(valor=="."):
            return coeficientes
        else:
            coeficientes.append(valor)
            n+=1

def valorEquacao(x,listaCoeficientes):
    soma=0
    for n,coef in enumerate(reversed(listaCoeficientes)):
        soma+=coef*x**(len(listaCoeficientes)-1-n)
    return soma

def umaEquacao(listaCoeficientes):
    return lambda x:valorEquacao(x,listaCoeficientes)

def refina(equacao,busca):
    listaDeIntervalos=[]
    sinal=lambda n: n>0
    espacoDeBusca=(np.linspace(busca[0],busca[1],busca[2])).tolist()
    for index in range(len(espacoDeBusca)-1):
        x=espacoDeBusca[index]
        a=equacao(x)
        print("F("+str(x)+") : "+str(a))
        if(a==0):
            listaDeIntervalos.append((a,a))
        else:
            proximoX=espacoDeBusca[index+1]
            b=equacao(proximoX)
            if(sinal(a)!=sinal(b)):
                listaDeIntervalos.append((x,proximoX))
    return(listaDeIntervalos)

def descobre(equacao,parada,intervalo):
    valor={}
    sinal=lambda n: valor[str(n)]>0
    iteracao=0
    a,b=intervalo
    while True:
        iteracao+=1
        diferenca=b-a
        meio=a+diferenca/2
        for x in (a,b,meio):
            if(x not in valor.keys()):
                valor[str(x)]=equacao(x)
        if(abs(diferenca)<parada):
            print("\nquantia de iterações : "+str(iteracao))
            return(meio)
        if(sinal(a)==sinal(meio)):
            valor.pop(str(a))
            a=meio
        elif(sinal(b)==sinal(meio)):
            valor.pop(str(b))
            b=meio
            
coeficientes=entradaDeCoeficientes()
equacao=umaEquacao(coeficientes)
inicio=pegaFloat("digite o ponto inicial de refinamento",".")
if(inicio=="."):
    inicio=-100
fim=pegaFloat("digite o ponto final de refinamento",".")
if(fim=="."):
    fim=100
quantidade=pegaInteiro("digite quantos pontos pegar entre "+str(inicio)+" e "+str(fim)+" para o refinamento",".")
if(quantidade=="."):
    quantidade=201
busca=[inicio,fim,quantidade]
refinamento=refina(equacao,busca)
print(refinamento)
parada=pegaFloat("digite o criterio de parada",".")
for intervalo in refinamento:
    resultado=descobre(equacao,parada,intervalo)
    print("resultado : "+str(resultado),end="\n\n")
