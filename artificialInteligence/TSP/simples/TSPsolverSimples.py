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


def GrafoFromArq(nome, lim=None):
    file = open(nome)
    linha = file.readline()
    vertices = []
    if lim:
        indice = 1
    while linha:
        if lim:
            if indice == lim:
                break
        elementos = linha.split()
        x = elementos[2]
        y = elementos[1]
        vertices.append((float(x), float(y)))
        linha = file.readline()
        if lim:
            indice += 1
    grafo = [[0 for _ in vertices] for _ in vertices]
    for n, origem in enumerate(vertices):
        for m, destino in enumerate(vertices):
            distancia = (
                (destino[0] - origem[0]) ** 2 + (destino[1] - origem[1]) ** 2
            ) ** 0.5
            grafo[n][m] = distancia
    return grafo


def geraFilhos(estado):
    global grafo
    filhos = []
    for index in range(len(grafo)):
        if index not in estado[1]:
            filhos.append(fazMovimento(estado, index))
    return filhos


def fazMovimento(estado, movimento):
    custo = estado[0]
    if estado[1]:
        global grafo
        custo += grafo[estado[1][-1]][movimento]
    caminho = estado[1] + [movimento]
    return (custo, caminho)


def imprime(duracao):
    global grafo
    global solucao
    estado = (0, [])
    for linha in grafo:
        print(
            " ".join(
                [" " * (3 - len(str(elemento))) + str(elemento) for elemento in linha]
            )
        )
    print()
    for movimento in solucao[1]:
        estado = fazMovimento(estado, movimento)
        print("caminho : " + str(estado[1]))
        print("custo   : " + str(estado[0]), end="\n\n")
    print("iteracoes : " + str(iterations))
    print("cortes    : " + str(cortes))
    print("duracao   : " + embelezeTempo(duracao))
    print("\n\n\n")


def solvePorProfundidade(estado, menorEstado=None):
    global iterations
    global cortes
    iterations += 1
    filhos = geraFilhos(estado)
    if len(filhos) == 0:
        if menorEstado == None:
            return estado
        else:
            if estado[0] < menorEstado[0]:
                return estado
    for filho in filhos:
        if menorEstado == None:
            menorEstado = solvePorProfundidade(filho, menorEstado)
        else:
            if filho[0] < menorEstado[0]:
                menorEstado = solvePorProfundidade(filho, menorEstado)
            else:
                cortes += 1
    return menorEstado


def solvePorLargura(estado):
    global iterations
    iterations += 1
    menorEstado = "a"
    estados = [estado]
    while estados:
        proximosEstados = []
        for estado in estados:
            filhos = geraFilhos(estado)
            if filhos:
                for filho in filhos:
                    if filho not in proximosEstados:
                        proximosEstados.append(filho)
            else:
                if menorEstado == "a":
                    menorEstado = estado
                else:
                    if estado[0] < menorEstado[0]:
                        menorEstado = estado
        estados = proximosEstados.copy()
    return menorEstado


def solve(grafo, mode=1):
    global iterations
    global cortes
    global solucao
    global estadoInicial
    inicio = time()
    iterations = 0
    cortes = 0
    estadoInicial = (0, [])
    if mode:
        solucao = solvePorProfundidade(estadoInicial)
    else:
        solucao = solvePorLargura(estadoInicial)
    final = time()
    imprime(final - inicio)


silent = False
iterations = 0
cortes = 0
estadoInicial = ()
solucao = ()

grafo = [
    [0, 10, 10, 1, 10],
    [10, 0, 1, 10, 10],
    [1, 10, 0, 10, 10],
    [10, 10, 10, 0, 1],
    [10, 1, 10, 10, 0],
]

solve(grafo, 0)

grafo = [[0, 1, 2, 4], [1, 0, 2, 3], [2, 2, 0, 5], [4, 3, 5, 0]]

solve(grafo, 1)

for a in range(1, 23):
    grafo = GrafoFromArq("grafo0004.txt", lim=a)
    solve(grafo, 1)
