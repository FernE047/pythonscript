def isInteger(elemento,tamanho):
    if elemento in range(tamanho):
        return True
    return False

def imprime():
    global matriz
    global iterations
    print(f"Iteracoes Totais {iterations:,}")
    if matriz:
        for linha in matriz:
            print(f"{' '.join([f'{elemento}{' '*(30-len(str(elemento)))}' for elemento in linha])}")
    else:
        print("nao existe solução")

def posicoesAfetadas(matriz,coord):
    yC,xC = coord
    lista = []
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

def posicoesParaAlterar(matriz,coord):
    yC,xC,i = coord
    lista = []
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

def numerosQueAfetam(matriz,coord):
    yC,xC,i = coord
    lista = []
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

def possibilidades(matriz,coord):
    y,x,i = coord
    impossibilidades = numerosQueAfetam(matriz,coord)
    lista = []
    for numero in range(len(matriz)):
        if numero not in impossibilidades:
            lista.append(numero)
    coloca(matriz,coord,lista)

def coloca(matriz,coord,elemento):
    y,x,i = coord
    tamanho = len(matriz)
    matriz[y][x][i] = elemento
    if isInteger(elemento,tamanho):
        for posicao in posicoesAfetadas(matriz,(y,x)):
            lista = matriz[posicao[0]][posicao[1]][i]
            if not isInteger(lista,tamanho):
                if elemento in lista:
                    lista.remove(elemento)

def devolve(matriz,coord,elemento):
    y,x,i = coord
    tamanho = len(matriz)
    possibilidades(matriz,coord)
    for y,x in posicoesParaAlterar(matriz,coord):
        if elemento not in numerosQueAfetam(matriz,(y,x,i)):
            matriz[y][x][i].append(elemento)

def solve(matriz,coord,usados):
    global iterations
    y,x,i = coord
    if iterations%100000==0:
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

def fazMatriz(tamanho,indice):
    global matriz
    matriz = [[[[a for a in range(tamanho)],[a for a in range(tamanho)]] for b in range(tamanho)] for c in range(tamanho)]
    for x in range(tamanho):
        for i in range(indice):
            coloca(matriz,(0,x,i),x)
    return matriz


def main() -> None:
    iterations = 0
    tamanho = 5
    indice = 2
    matriz = []
    fazMatriz(tamanho,indice)
    usados = [[a,a] for a in range(tamanho)]
    matriz = solve(matriz,(1,0,0),usados)
    imprime()


if __name__ == "__main__":
    main()