# this code is legacy, I am only changing type hints and linter errors. it doesn't make sense to refactor it, since I already have a better version of it, and I don't want to break it by changing it too much


def isInteger(elemento: list[int], tamanho: int) -> bool:
    if elemento in range(tamanho):
        return True
    return False


def imprime() -> None:
    global matriz
    global iterations
    global profundidade
    print(f"Profundidade {profundidade}")
    print(f"Iteracoes Totais {iterations:,}")
    if matriz:
        for linha in matriz:
            print(
                f"{' '.join([f'{elemento}{' ' * (30 - len(str(elemento)))}' for elemento in linha])}"
            )
    else:
        print("nao existe solução")


def posicoesAfetadas(
    matriz: list[list[list[list[int]]]], coord: tuple[int, int]
) -> list[tuple[int, int]]:
    yC, xC = coord
    lista: list[tuple[int, int]] = []
    tamanho = len(matriz)
    for x in range(tamanho):
        if x == xC:
            continue
        lista.append((yC, x))
    for y in range(tamanho):
        if y == yC:
            continue
        lista.append((y, xC))
    if xC == yC:
        for c in range(tamanho):
            if c == xC:
                continue
            lista.append((c, c))
    if xC == tamanho - yC - 1:
        for c in range(tamanho):
            if c == yC:
                continue
            lista.append((c, tamanho - c - 1))
    return lista


def posicoesParaAlterar(
    matriz: list[list[list[list[int]]]], coord: tuple[int, int, int]
) -> list[tuple[int, int]]:
    yC, xC, i = coord
    lista: list[tuple[int, int]] = []
    tamanho = len(matriz)
    for x in range(tamanho):
        if x == xC:
            continue
        elemento = matriz[yC][x][i]
        if not isInteger(elemento, tamanho):
            lista.append((yC, x))
    for y in range(tamanho):
        if y == yC:
            continue
        elemento = matriz[y][xC][i]
        if not isInteger(elemento, tamanho):
            lista.append((y, xC))
    if xC == yC:
        for c in range(tamanho):
            if c == xC:
                continue
            elemento = matriz[c][c][i]
            if not isInteger(elemento, tamanho):
                lista.append((c, c))
    if xC == tamanho - yC - 1:
        for c in range(tamanho):
            if c == yC:
                continue
            elemento = matriz[c][tamanho - c - 1][i]
            if not isInteger(elemento, tamanho):
                lista.append((c, tamanho - c - 1))
    return lista


def numerosQueAfetam(
    matriz: list[list[list[list[int]]]], coord: tuple[int, int, int]
) -> list[list[int]] | list[int]:
    yC, xC, i = coord
    lista: list[list[int]] = []
    listaCompleta = [a for a in range(len(matriz))]
    tamanho = len(matriz)
    for x in range(tamanho):
        if x == xC:
            continue
        elemento = matriz[yC][x][i]
        if isInteger(elemento, tamanho):
            lista.append(elemento)
    for y in range(tamanho):
        if y == yC:
            continue
        elemento = matriz[y][xC][i]
        if isInteger(elemento, tamanho):
            lista.append(elemento)
    if lista == listaCompleta:
        return listaCompleta
    if xC == yC:
        for c in range(tamanho):
            if c == xC:
                continue
            elemento = matriz[c][c][i]
            if isInteger(elemento, tamanho):
                lista.append(elemento)
        if lista == listaCompleta:
            return listaCompleta
    if xC == tamanho - yC - 1:
        for c in range(tamanho):
            if c == yC:
                continue
            elemento = matriz[c][tamanho - c - 1][i]
            if isInteger(elemento, tamanho):
                lista.append(elemento)
        if lista == listaCompleta:
            return listaCompleta
    return lista


def possibilidades(
    matriz: list[list[list[list[int]]]], coord: tuple[int, int, int]
) -> None:
    impossibilidades = numerosQueAfetam(matriz, coord)
    lista: list[int] = []
    for numero in range(len(matriz)):
        if numero not in impossibilidades:
            lista.append(numero)
    coloca(matriz, coord, lista)


def coloca(
    matriz: list[list[list[list[int]]]],
    coord: tuple[int, int, int],
    elemento: list[int],
) -> bool:
    y, x, i = coord
    tamanho = len(matriz)
    matriz[y][x][i] = elemento
    if isInteger(elemento, tamanho):
        for posicao in posicoesAfetadas(matriz, (y, x)):
            lista = matriz[posicao[0]][posicao[1]][i]
            if not isInteger(lista, tamanho):
                if elemento in lista:  # type: ignore
                    if len(lista) == 1:
                        return False
                    lista.remove(elemento)  # type: ignore
    return True


def devolve(
    matriz: list[list[list[list[int]]]], coord: tuple[int, int, int], elemento: int
) -> None:
    y, x, i = coord
    possibilidades(matriz, coord)
    for y, x in posicoesParaAlterar(matriz, coord):
        if elemento not in numerosQueAfetam(matriz, (y, x, i)) + matriz[y][x][i]:
            matriz[y][x][i].append(elemento)
    return None


def solve(
    matriz: list[list[list[list[int]]]],
    coord: tuple[int, int, int],
    usados: list[list[int]],
) -> list[list[list[list[int]]]] | None:
    global iterations
    y, x, i = coord
    if iterations % 100000 == 0:
        imprime()
        print()
    iterations += 1
    if y == len(matriz):
        if i != 1:
            return solve(matriz, (1, 0, 1), usados)
        else:
            return matriz
    poss = matriz[y][x][i].copy()
    for possibilidade in poss:
        if i == 1:
            elemento: list[int | list[int]] = [matriz[y][x][0], possibilidade]
            if elemento in usados:
                continue
            else:
                usados.append(elemento) #type: ignore
        if coloca(matriz, (y, x, i), possibilidade):  # type: ignore
            matriz[y][x][i] = possibilidade  # type: ignore
            if x == len(matriz) - 1:
                solucao = solve(matriz, (y + 1, 0, i), usados)
            else:
                solucao = solve(matriz, (y, x + 1, i), usados)
            if solucao:
                return solucao
        if i == 1:
            usados.remove(elemento)  # type: ignore
        devolve(matriz, (y, x, i), possibilidade)
    return None


def fazMatriz(tamanho: int, indice: int) -> list[list[list[list[int]]]]:
    global matriz
    matriz = [
        [
            [[a for a in range(tamanho)], [a for a in range(tamanho)]]
            for _ in range(tamanho)
        ]
        for _ in range(tamanho)
    ]
    for x in range(tamanho):
        for i in range(indice):
            coloca(matriz, (0, x, i), x)  # type: ignore
    return matriz


matriz: list[list[list[list[int]]]] = []
iterations = 0
profundidade = 0


def main() -> None:
    global matriz
    tamanho = 5
    indice = 2
    fazMatriz(tamanho, indice)
    usados = [[a, a] for a in range(tamanho)]
    matriz = solve(matriz, (1, 0, 0), usados)  # type: ignore
    imprime()


if __name__ == "__main__":
    main()
