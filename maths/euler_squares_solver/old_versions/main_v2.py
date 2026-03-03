# this code is legacy, I am only changing type hints and linter errors. it doesn't make sense to refactor it, since I already have a better version of it, and I don't want to break it by changing it too much

CoordData = tuple[int, int]
MatrizData = list[list[CoordData]]


def imprime(matriz: MatrizData) -> None:
    global iterations
    print(f"Iteracoes Totais {iterations}")
    if matriz:
        for linha in matriz:
            print(" ".join([str(elemento) for elemento in linha]))
    else:
        print("nao existe solução")

def verifica(matriz: MatrizData, xLim: int, yLim: int, elemento: CoordData) -> bool:
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
    if xLim==yLim:
        for c in range(xLim):
            if matriz[c][c][0] == elemento[0]:
                return False
            if matriz[c][c][1] == elemento[1]:
                return False
    tam = len(matriz)
    if xLim == tam - yLim - 1 :
        for c in range(yLim):
            if matriz[c][tam-c-1][0] == elemento[0]:
                return False
            if matriz[c][tam-c-1][1] == elemento[1]:
                return False
    return True

def possibilidades(matriz: MatrizData, x: int, y: int, usados: list[CoordData]) -> list[CoordData]:
    lista: list[CoordData] = []
    tamanho = len(matriz)
    for a in range(tamanho):
        for b in range(tamanho):
            if (a,b) not in usados:
                if(verifica(matriz,x,y,(a,b))):
                    lista.append((a,b))
    return lista

def solve(x: int, y: int, matriz: MatrizData, usados: list[CoordData]) -> MatrizData | None:
    global iterations
    if iterations%100000==0:
        print(f"{iterations:,}")
        imprime(matriz)
        print()
    iterations += 1
    if(y==len(matriz)):
        return matriz
    for possibilidade in possibilidades(matriz,x,y,usados):
        matriz[y][x] = possibilidade
        usados.append(possibilidade)
        if(x==len(matriz)-1):
            solucao = solve(0,y+1,matriz,usados)
        else:
            solucao = solve(x+1,y,matriz,usados)
        if solucao:
            return solucao
        usados.pop()
        matriz[y][x] = (0,0)
    return None

iterations = 0

def main() -> None:
    global iterations
    tamanho = 5
    largura = tamanho
    altura  = tamanho
    usados = [(a,a) for a in range(largura)]
    matriz = [usados.copy()]+[[(0,0) for _ in range(largura)] for _ in range(1,altura)]
    matriz_result = solve(0,1,matriz,usados)
    if matriz_result is None:
        return
    imprime(matriz_result)


if __name__ == "__main__":
    main()