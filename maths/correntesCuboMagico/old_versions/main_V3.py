import math
from time import time

# this code is legacy, I am only changing type hints and linter errors. it doesn't make sense to refactor it, since I already have a better version of it, and I don't want to break it by changing it too much

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
    print(f"{sign}{', '.join(parts)}")


def geraLista(listaInicial: list[int], x: int) -> list[int]:
    y = len(listaInicial)
    if y <= 1:
        return listaInicial
    divisor = math.factorial(y) // y
    elemento = listaInicial.pop(x // divisor)
    return [elemento] + geraLista(listaInicial, x % divisor)


def categorizaCorrentes(correntes: list[list[int]], total: int) -> str:
    tamanhos = [0 for _ in range(total)]
    for corrente in correntes:
        tamanhos[len(corrente) - 1] += 1
    categoria = ""
    for indice in range(1, total):
        if categoria and tamanhos[indice]:
            categoria += " "
        categoria += " ".join([str(indice + 1) for _ in range(tamanhos[indice])])
    if not categoria:
        categoria = "0"
    return categoria


def analisaAsListas(n: int) -> dict[str, int]:
    limite = 1000
    categorias: dict[str, int] = {}
    first = 0
    inicio = time()
    for a in range(math.factorial(n)):
        lista = [a for a in range(n)]
        listaNova = geraLista(lista, a)
        categoria, _ = achaTodasCorrentes(listaNova)
        if categoria in categorias:
            categorias[categoria] += 1
        else:
            categorias[categoria] = 1
        if first <= limite:
            if first == limite:
                fim = time()
                duracao = fim - inicio
                print(f"{limite} execucoes deu : ")
                print_elapsed_time(duracao)
                print("Previsao de Execucao Total  : ")
                print_elapsed_time(duracao * (math.factorial(n) / limite))
                first = limite + 1
            else:
                first += 1
    return categorias


def achaTodasCorrentes(lista: list[int]) -> tuple[str, list[list[int]]]:
    situacoes = [False for _ in lista]
    correntes: list[list[int]] = []
    tamanhos: dict[int, int] = {}
    indicesTamanhos: list[int] = []
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
    categoria: list[str] = []
    indicesTamanhos.sort()
    for indice in indicesTamanhos:
        categoria += [str(indice) for _ in range(tamanhos[indice])]
    return (" ".join(categoria), correntes)



def main() -> None:
    inicio = time()
    dic = analisaAsListas(10)
    for cat in dic:
        print(f"{cat:8s} : {dic[cat]}")
    print("execucao Total  : ")
    print_elapsed_time(time() - inicio)


if __name__ == "__main__":
    main()