from grafos import Graph
from grafos import get_graph_from_file
from estados import Estado


def solvePorProfundidade(estado, menorEstado=None):
    global iterations
    global cortes
    iterations += 1
    filhos = estado.geraFilhos()
    if len(filhos) == 0:
        if menorEstado == None:
            return estado
        else:
            if estado.custo < menorEstado.custo:
                return estado
    for filho in filhos:
        if menorEstado == None:
            menorEstado = solvePorProfundidade(filho, menorEstado)
        else:
            if filho.custo < menorEstado.custo:
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
            filhos = estado.geraFilhos()
            if filhos:
                for filho in filhos:
                    if filho not in proximosEstados:
                        proximosEstados.append(filho)
            else:
                if menorEstado == "a":
                    menorEstado = estado
                else:
                    if estado.custo < menorEstado.custo:
                        menorEstado = estado
        estados = proximosEstados.copy()
    return menorEstado


silent = False
iterations = 0
cortes = 0
grafo = [
    [0, 10, 10, 1, 10],
    [10, 0, 1, 10, 10],
    [1, 10, 0, 10, 10],
    [10, 10, 10, 0, 1],
    [10, 1, 10, 10, 0],
]
grafo = Graph(base_graph=grafo)
estadoInicial = Estado(grafo)
solucao = solvePorLargura(estadoInicial)
solucao.imprime()
grafo = Graph(4)
grafo.set_element([0, 1], 1)
grafo.set_element([0, 2], 2)
grafo.set_element([0, 3], 4)
grafo.set_element([1, 2], 2)
grafo.set_element([1, 3], 3)
grafo.set_element([2, 3], 5)
estadoInicial = Estado(grafo)
solucao = solvePorProfundidade(estadoInicial)
print(iterations)
print(cortes)
iterations = 0
cortes = 0
solucao.imprime()
for a in range(1, 23):
    grafo = get_graph_from_file("grafo0004.txt", limit=a)
    estadoInicial = Estado(grafo)
    solucao = solvePorProfundidade(estadoInicial)
    solucao.imprime()
    print("iteracoes : " + str(iterations))
    print("cortes    : " + str(cortes))
    print("\n\n\n")
    iterations = 0
    cortes = 0
