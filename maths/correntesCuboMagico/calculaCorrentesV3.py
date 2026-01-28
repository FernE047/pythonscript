import math
from time import time


def embelezeTempo(segundos: float) -> str:
    if segundos < 0:
        segundos = -segundos
        sign = "-"
    else:
        sign = ""
    total_ms = int(round(segundos * 1000))
    ms = total_ms % 1000
    total_s = total_ms // 1000
    s = total_s % 60
    total_min = total_s // 60
    m = total_min % 60
    total_h = total_min // 60
    h = total_h % 24
    d = total_h // 24
    parts: list[str] = []

    def add(value: int, singular: str, plural: str) -> None:
        if value:
            parts.append(f"{value} {singular if value == 1 else plural}")

    add(d, "day", "days")
    add(h, "hour", "hours")
    add(m, "minute", "minutes")
    add(s, "second", "seconds")
    if ms or not parts:
        parts.append(f"{ms} millisecond" if ms == 1 else f"{ms} milliseconds")
    return sign + ", ".join(parts)


def geraLista(listaInicial, x):
    y = len(listaInicial)
    if y <= 1:
        return listaInicial
    divisor = math.factorial(y) // y
    elemento = listaInicial.pop(x // divisor)
    return [elemento] + geraLista(listaInicial, x % divisor)


def categorizaCorrentes(correntes, total):
    tamanhos = [0 for a in range(total)]
    for corrente in correntes:
        tamanhos[len(corrente) - 1] += 1
    categoria = ""
    for indice in range(1, total):
        if categoria and tamanhos[indice]:
            categoria += " "
        categoria += " ".join([str(indice + 1) for a in range(tamanhos[indice])])
    if not categoria:
        categoria = "0"
    return categoria


def analisaAsListas(n):
    limite = 1000
    categorias = {}
    first = 0
    inicio = time()
    for a in range(math.factorial(n)):
        lista = [a for a in range(n)]
        listaNova = geraLista(lista, a)
        categoria, correntes = achaTodasCorrentes(listaNova)
        if categoria in categorias:
            categorias[categoria] += 1
        else:
            categorias[categoria] = 1
        if first <= limite:
            if first == limite:
                fim = time()
                duracao = fim - inicio
                print(str(limite) + " execucoes deu : " + embelezeTempo(duracao))
                print(
                    "Previsao de Execucao Total  : "
                    + embelezeTempo(duracao * (math.factorial(n) / limite))
                )
                first = limite + 1
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
    return (" ".join(categoria), correntes)


inicio = time()
dic = analisaAsListas(10)
for cat in dic:
    print(f"{cat:8s} : {dic[cat]}")
print("execucao Total  : " + embelezeTempo(time() - inicio))
