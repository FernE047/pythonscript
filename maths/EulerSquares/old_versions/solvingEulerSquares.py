# this code is legacy, I am only changing type hints and linter errors. it doesn't make sense to refactor it, since I already have a better version of it, and I don't want to break it by changing it too much

CoordData = tuple[int, int]
MatrizData = list[list[CoordData]]

def imprime(matriz: MatrizData) -> None:
    if matriz:
        for linha in matriz:
            print(" ".join([str(elemento) for elemento in linha]))
    else:
        print("nao existe solução")


def verifica(matriz: MatrizData, xLim: int, yLim: int) -> bool:
    elemento = matriz[yLim][xLim]
    for x in range(xLim):
        if matriz[yLim][x][0] == elemento[0]:
            return False
        if matriz[yLim][x][1] == elemento[1]:
            return False
    for y in range(yLim):
        if matriz[y][xLim][0] == elemento[0]:
            return False
        if matriz[y][xLim][1] == elemento[1]:
            return False
    if xLim == yLim:
        for c in range(xLim):
            if matriz[c][c][0] == elemento[0]:
                return False
            if matriz[c][c][1] == elemento[1]:
                return False
    tam = len(matriz)
    if xLim == tam - yLim - 1:
        for c in range(yLim):
            if matriz[c][tam - c - 1][0] == elemento[0]:
                return False
            if matriz[c][tam - c - 1][1] == elemento[1]:
                return False
    return True


def solve(x: int, y: int, matriz: MatrizData, possibilidades: list[CoordData]) -> MatrizData | None:
    global tries
    global iterations
    if iterations % 100000 == 0:
        print(f"{iterations:,}")
        print(f"{tries:,}")
        imprime(matriz)
        print()
    iterations += 1
    if y == len(matriz):
        return matriz
    for indice in range(len(possibilidades)):
        tries += 1
        elemento = possibilidades[indice]
        if elemento == (0, 0):
            continue
        possibilidades[indice] = (0, 0)
        matriz[y][x] = elemento
        if verifica(matriz, x, y):
            if x == len(matriz[0]) - 1:
                solucao = solve(0, y + 1, matriz, possibilidades)
            else:
                solucao = solve(x + 1, y, matriz, possibilidades)
            if solucao:
                return solucao
        matriz[y][x] = (0, 0)
        possibilidades[indice] = elemento
    return None

tries = 0
iterations = 0

def main() -> None:
    tamanho = 5
    largura = tamanho
    altura = tamanho
    possibilidades: list[CoordData] = []
    for x in range(largura):
        for y in range(altura):
            if x != y:
                possibilidades.append((x, y))
    matriz = [[(a, a) for a in range(largura)]] + [
        [(0, 0) for _ in range(largura)] for _ in range(1, altura)
    ]
    matriz_result = solve(0, 1, matriz, possibilidades)
    if matriz_result is None:
        return
    imprime(matriz_result)


if __name__ == "__main__":
    main()
