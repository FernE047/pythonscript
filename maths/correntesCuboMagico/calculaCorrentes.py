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
        correntes = achaTodasCorrentes(listaNova)
        categoria = categorizaCorrentes(correntes,n)
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

def achaCorrente(lista,indiceInicial):
    elemento = lista[indiceInicial]
    corrente = [elemento]
    while elemento != indiceInicial:
        elemento = lista[elemento]
        corrente.append(elemento)
    return corrente

def achaTodasCorrentes(lista):
    situacoes = [('correto' if n == elemento else 'desconhecido') for n,elemento in enumerate(lista)]
    correntes = []
    for n,elemento in enumerate(situacoes):
        if elemento == 'correto':
            correntes.append([n])
    indiceCorrente = 0
    while 'desconhecido' in situacoes:
        corrente = achaCorrente(lista,situacoes.index('desconhecido'))
        for a in corrente:
            situacoes[a] = 'correto'
        correntes.append(corrente)
    return correntes

inicio = time()
dic = analisaAsListas(12)
for cat in dic:
    print('{0:8s} : '.format(cat)+str(dic[cat]))
print('execucao Total  : '+eT(time()-inicio))
