# type: ignore

# this code is a mess

# this code is legacy, I am only changing type hints and linter errors. it doesn't make sense to refactor it, since I already have a better version of it, and I don't want to break it by changing it too much

CoordData = tuple[int, int]
BiggerCoordData = tuple[int, int, int]
MatrizData = list[list[CoordData]]
BiggerMatrizData = list[list[list[int]]]


def isInteger(elemento: int, tamanho: int) -> bool:
    if elemento in range(tamanho):
        return True
    return False

def imprime() -> None:
    global matriz
    global iterations
    print(f"Iteracoes Totais {iterations:,}")
    if matriz:
        for linha in matriz:
            print(f"{' '.join([f'{elemento}{' '*(30-len(str(elemento)))}' for elemento in linha])}")
    else:
        print("nao existe solução")

def posicoesAfetadas(matriz: MatrizData, coord: CoordData) -> list[CoordData]:
    yC, xC = coord
    lista: list[CoordData] = []
    tamanho = len(matriz)
    for x in range(tamanho):
        if x == xC:
            continue
        lista.append((yC,x))
    for y in range(tamanho):
        if y == yC:
            continue
        lista.append((y,xC))
    if xC==yC:
        for c in range(tamanho):
            if c == xC:
                continue
            lista.append((c,c))
    if xC == tamanho - yC - 1 :
        for c in range(tamanho):
            if c == yC:
                continue
            lista.append((c,tamanho - c - 1))
    return lista

def posicoesParaAlterar(matriz: MatrizData, coord: BiggerCoordData) -> list[CoordData]:
    yC, xC, i = coord
    lista: list[CoordData] = []
    tamanho = len(matriz)
    for x in range(tamanho):
        if x == xC:
            continue
        elemento = matriz[yC][x][i]
        if not isInteger(elemento,tamanho):
            lista.append((yC,x))
    for y in range(tamanho):
        if y == yC:
            continue
        elemento = matriz[y][xC][i]
        if not isInteger(elemento,tamanho):
            lista.append((y,xC))
    if xC==yC:
        for c in range(tamanho):
            if c == xC:
                continue
            elemento = matriz[c][c][i]
            if not isInteger(elemento,tamanho):
                lista.append((c,c))
    if xC == tamanho - yC - 1 :
        for c in range(tamanho):
            if c == yC:
                continue
            elemento = matriz[c][tamanho - c - 1][i]
            if not isInteger(elemento,tamanho):
                lista.append((c,tamanho - c - 1))
    return lista

def numerosQueAfetam(matriz: MatrizData, coord: BiggerCoordData) -> list[int]:
    yC, xC, i = coord
    lista: list[int] = []
    listaCompleta = [index for index in range(len(matriz))]
    tamanho = len(matriz)
    for x in range(tamanho):
        if x == xC:
            continue
        elemento = matriz[yC][x][i]
        if isInteger(elemento,tamanho):
            lista.append(elemento)
    for y in range(tamanho):
        if y == yC:
            continue
        elemento = matriz[y][xC][i]
        if isInteger(elemento,tamanho):
            lista.append(elemento)
    if lista == listaCompleta:
        return listaCompleta
    if xC==yC:
        for c in range(tamanho):
            if c == xC:
                continue
            elemento = matriz[c][c][i]
            if isInteger(elemento,tamanho):
                lista.append(elemento)
        if lista == listaCompleta:
            return listaCompleta
    if xC == tamanho - yC - 1 :
        for c in range(tamanho):
            if c == yC:
                continue
            elemento = matriz[c][tamanho - c - 1][i]
            if isInteger(elemento,tamanho):
                lista.append(elemento)
        if lista == listaCompleta:
            return listaCompleta
    return lista

def possibilidades(matriz: MatrizData, coord: BiggerCoordData) -> None:
    impossibilidades = numerosQueAfetam(matriz, coord)
    lista: list[int] = []
    for numero in range(len(matriz)):
        if numero not in impossibilidades:
            lista.append(numero)
    coloca(matriz,coord,lista)

def coloca(matriz: MatrizData, coord: BiggerCoordData, elemento: list[int]) -> None:
    y, x, i = coord
    tamanho = len(matriz)
    matriz[y][x][i] = elemento
    if isInteger(elemento,tamanho):
        for posicao in posicoesAfetadas(matriz,(y,x)):
            lista = matriz[posicao[0]][posicao[1]][i]
            if not isInteger(lista,tamanho):
                if elemento in lista:
                    lista.remove(elemento)

def devolve(matriz: MatrizData, coord: BiggerCoordData, elemento: int) -> None:
    y, x, i = coord
    possibilidades(matriz, coord)
    for y, x in posicoesParaAlterar(matriz, coord):
        if elemento not in numerosQueAfetam(matriz, (y, x, i)):
            matriz[y][x][i].append(elemento)

def solve(matriz: MatrizData, coord: BiggerCoordData, usados: list[list[int]]) -> MatrizData | None:
    global iterations
    y, x, i = coord
    if iterations % 100000 == 0:
        imprime()
        print()
    iterations += 1
    if(y==len(matriz)):
        if(i!=1):
            return solve(matriz,(1,0,1),usados)
        else:
            return matriz
    for possibilidade in matriz[y][x][i].copy():
        if i == 1 :
            elemento = [matriz[y][x][0],possibilidade]
            if elemento in usados:
                continue
            else:
                usados.append(elemento)
        coloca(matriz,(y,x,i),possibilidade)
        matriz[y][x][i] = possibilidade
        if(x==len(matriz)-1):
            solucao = solve(matriz,(y+1,0,i),usados)
        else:
            solucao = solve(matriz,(y,x+1,i),usados)
        if solucao:
            return solucao
        if i == 1:
            usados.remove(elemento)
        devolve(matriz,(y,x,i),possibilidade)
    return None

def fazMatriz(tamanho: int, indice: int) -> MatrizData:
    global matriz
    matriz = [[[[a for a in range(tamanho)],[a for a in range(tamanho)]] for b in range(tamanho)] for c in range(tamanho)]
    for x in range(tamanho):
        for i in range(indice):
            coloca(matriz,(0,x,i),x)
    return matriz

iterations = 0

def main() -> None:
    tamanho = 5
    indice = 2
    matriz = fazMatriz(tamanho,indice)
    usados = [[a,a] for a in range(tamanho)]
    matriz = solve(matriz,(1,0,0),usados)
    imprime()


if __name__ == "__main__":
    main()