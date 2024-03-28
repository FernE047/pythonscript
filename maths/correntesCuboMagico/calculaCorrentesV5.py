import math
from time import time
from textos import embelezeTempo as eT
import gc

def geraLista(listaInicial,x):
    y = len(listaInicial)
    if y <= 1:
        return(listaInicial)
    divisor = math.factorial(y-1)
    elemento = listaInicial.pop(x // divisor)
    return [elemento] + geraLista(listaInicial,x % divisor)

def analisaAsListas(n):
    limite=1000
    categorias = {}
    first = 0
    inicio = time()
    lista = [a for a in range(n)]
    for a in range(math.factorial(n)):
        categoria = achaCategoria(geraLista(lista.copy(),a))
        if categoria in categorias:
            categorias[categoria] += 1
        else:
            categorias[categoria] = 1
        if first<=limite:
            if first == limite:
                fim = time()
                duracao = fim-inicio
                print(str(limite)+' execucoes deu : '+eT(duracao))
                print('Previsao de Execucao Total  : '+eT(duracao*(math.factorial(n)/limite)))
                first = limite+1
            else:
                first += 1
    return categorias

def achaCategoria(lista):
    situacoes = [False for n in lista]
    tamanhos = [0 for n in lista]
    while False in situacoes:
        indiceCorrente = situacoes.index(False)
        elemento = lista[indiceCorrente]
        tamanho = 0
        situacoes[indiceCorrente] = True
        while elemento != indiceCorrente:
            situacoes[elemento] = True
            elemento = lista[elemento]
            tamanho += 1
        tamanhos[tamanho] += 1
    categoria = []
    for indice in range(1,len(lista)):
        if tamanhos[indice] != 0:
            categoria += [str(indice+1) for a in range(tamanhos[indice])]
    return ' '.join(categoria)

inicio = time()
try:
    dic = analisaAsListas(12)
    for cat in dic:
        print('{0:8s} : '.format(cat)+str(dic[cat]))
    print('execucao Total  : '+eT(time()-inicio))
except:
    print(gc.collect())
