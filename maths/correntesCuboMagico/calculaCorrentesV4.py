import math
from time import time
from textos import embelezeTempo as eT

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
    tamanhos = {}
    while False in situacoes:
        indiceCorrente = situacoes.index(False)
        elemento = lista[indiceCorrente]
        tamanho = 1
        situacoes[indiceCorrente] = True
        while elemento != indiceCorrente:
            situacoes[elemento] = True
            elemento = lista[elemento]
            tamanho += 1
        if tamanho > 1:
            if tamanho in tamanhos:
                tamanhos[tamanho] += 1
            else:
                tamanhos[tamanho] = 1
    categoria = []
    tamanhos = sorted(tamanhos.items(), key=lambda kv: kv[1])
    for indice,valor in tamanhos:
        categoria += [str(indice) for a in range(valor)]
    return ' '.join(categoria)

inicio = time()
dic = analisaAsListas(8)
for cat in dic:
    print(f'{cat:8s} : {dic[cat]}')
print('execucao Total  : '+eT(time()-inicio))
