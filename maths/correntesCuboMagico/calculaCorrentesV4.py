import math
from time import time


def print_elapsed_time(seconds: float) -> None:
    if seconds < 0:
        seconds = -seconds
        sign = "-"
    else:
        sign = ""
    total_ms = int(round(seconds * 1000))
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
    print(sign + ", ".join(parts))


def geraLista(listaInicial, x):
    y = len(listaInicial)
    if y <= 1:
        return listaInicial
    divisor = math.factorial(y - 1)
    elemento = listaInicial.pop(x // divisor)
    return [elemento] + geraLista(listaInicial, x % divisor)


def analisaAsListas(n):
    limite = 1000
    categorias = {}
    first = 0
    inicio = time()
    lista = [a for a in range(n)]
    for a in range(math.factorial(n)):
        categoria = achaCategoria(geraLista(lista.copy(), a))
        if categoria in categorias:
            categorias[categoria] += 1
        else:
            categorias[categoria] = 1
        if first <= limite:
            if first == limite:
                fim = time()
                duracao = fim - inicio
                print(str(limite) + " execucoes deu : ")
                print_elapsed_time(duracao)
                print("Previsao de Execucao Total  : ")
                print_elapsed_time(duracao * (math.factorial(n) / limite))
                first = limite + 1
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
    for indice, valor in tamanhos:
        categoria += [str(indice) for a in range(valor)]
    return " ".join(categoria)


inicio = time()
dic = analisaAsListas(8)
for cat in dic:
    print(f"{cat:8s} : {dic[cat]}")
print("execucao Total  : ")
print_elapsed_time(time() - inicio)