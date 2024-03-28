import math
from time import time
from textos import embelezeTempo as eT

def geraLista(listaInicial,x):
    y = len(listaInicial)
    if y <= 1:
        return(listaInicial)
    divisor = math.factorial(y)//y
    elemento = listaInicial.pop(x // divisor)
    return [elemento] + geraLista(listaInicial,x % divisor)

def categorizaCorrentes(correntes,total):
    tamanhos = [0 for a in range(total)]
    for corrente in correntes:
        tamanhos[len(corrente)-1] += 1
    categoria = ''
    for indice in range(1,total):
        if categoria and tamanhos[indice]:
            categoria += ' '
        categoria += ' '.join([str(indice+1) for a in range(tamanhos[indice])])
    if not categoria:
        categoria = '0'
    return categoria

def analisaAsListas(n):
    limite=1000
    categorias = {}
    first = 0
    inicio = time()
    for a in range(math.factorial(n)):
        lista = [a for a in range(n)]
        listaNova = geraLista(lista,a)
        categoria,correntes = achaTodasCorrentes(listaNova)
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

def achaTodasCorrentes(lista):
    situacoes = [False for n in lista]
    correntes = []
    tamanhos = {}
    indicesTamanhos = []
    while False in situacoes:
        indiceCorrente = situacoes.index(False)
        elemento = lista[indiceCorrente]
        corrente = [elemento]
        situacoes[indiceCorrente] = True
        while elemento != indiceCorrente:
            situacoes[elemento] = True
            elemento = lista[elemento]
            corrente.append(elemento)
        tamanho = len(corrente)
        if tamanho > 1:
            if tamanho in tamanhos:
                tamanhos[tamanho] += 1
            else:
                tamanhos[tamanho] = 1
                indicesTamanhos.append(tamanho)
        correntes.append(corrente)
    categoria = []
    indicesTamanhos.sort()
    for indice in indicesTamanhos:
        categoria += [str(indice) for a in range(tamanhos[indice])]
    return (' '.join(categoria),correntes)

inicio = time()
dic = analisaAsListas(10)
for cat in dic:
    print('{0:8s} : '.format(cat)+str(dic[cat]))
print('execucao Total  : '+eT(time()-inicio))
