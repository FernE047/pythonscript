import internet
import requests, bs4, re
import random

def tamanhoParaTitulo():
    population = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,17]
    weight = [1,1,6,16,35,63,49,33,30,28,39,37,30,15,5,1]
    return(random.choices(population,weights=weight))

def procuraTextoEmLista(palavra,lista):
    

while True:
    print("\n\nqual o primeiro termo?")
    termo=input().lower()
    tituloTamanho=tamanhoParaTitulo()
    print("tamanho do titulo "+tituloTamanho+" palavras")
    informacao=internet.pesquisaGoogle(termo,adicao='+site%3A%2Ffanfiction.com.br%2F')
    tituloOficial=[termo]
    titulos=[]
    while (len(tituloOficial)<=tituloTamanho):
        for info in informacao:
            newInfo=info.select(".LC20lb")
            if(newInfo):
                texto=newInfo[0].get_text().lower()
                indice=procuraTextoEmLista(termo,texto.split())
                titulos+=[texto]
    print("\ntitulo\n")
            
