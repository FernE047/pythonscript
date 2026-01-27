def isInteger(elemento):
    global matriz
    tamanho = len(matriz)
    if elemento in range(tamanho):
        return True
    return False

def imprime():
    global matriz
    global iterations
    global tabulacao
    print(f"Iteracoes Totais {iterations:,}")
    if matriz:
        for linha in matriz:
            print(' '.join([str(elemento)+' '*(tabulacao-len(str(elemento))) for elemento in linha]))
    else:
        print("nao existe solução")

def posicoesAfetadas(coord):
    global matriz
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

def posicoesParaAlterar(coord):
    global matriz
    yC,xC,i = coord
    lista = []
    tamanho = len(matriz)
    for x in range(tamanho):
        if x == xC:
            continue
        elemento = matriz[yC][x][i]
        if not isInteger(elemento):
            lista.append((yC,x))
    for y in range(tamanho):
        if y == yC:
            continue
        elemento = matriz[y][xC][i]
        if not isInteger(elemento):
            lista.append((y,xC))
    if xC==yC:
        for c in range(tamanho):
            if c == xC:
                continue
            elemento = matriz[c][c][i]
            if not isInteger(elemento):
                lista.append((c,c))
    if xC == tamanho - yC - 1 :
        for c in range(tamanho):
            if c == yC:
                continue
            elemento = matriz[c][tamanho - c - 1][i]
            if not isInteger(elemento):
                lista.append((c,tamanho - c - 1))
    return lista

def numerosQueAfetam(coord):
    global matriz
    yC,xC,i = coord
    lista = []
    listaCompleta = [a for a in range(len(matriz))]
    tamanho = len(matriz)
    for x in range(tamanho):
        if x == xC:
            continue
        elemento = matriz[yC][x][i]
        if isInteger(elemento):
            lista.append(elemento)
    for y in range(tamanho):
        if y == yC:
            continue
        elemento = matriz[y][xC][i]
        if isInteger(elemento):
            lista.append(elemento)
    if lista == listaCompleta:
        return listaCompleta
    if xC==yC:
        for c in range(tamanho):
            if c == xC:
                continue
            elemento = matriz[c][c][i]
            if isInteger(elemento):
                lista.append(elemento)
        if lista == listaCompleta:
            return listaCompleta
    if xC == tamanho - yC - 1 :
        for c in range(tamanho):
            if c == yC:
                continue
            elemento = matriz[c][tamanho - c - 1][i]
            if isInteger(elemento):
                lista.append(elemento)
        if lista == listaCompleta:
            return listaCompleta
    return lista

def possibilidades(coord):
    global matriz
    y,x,i = coord
    impossibilidades = numerosQueAfetam(coord)
    lista = []
    for numero in range(len(matriz)):
        if numero not in impossibilidades:
            lista.append(numero)
    coloca(coord,lista)

def coloca(coord,elemento):
    global matriz
    y,x,i = coord
    tamanho = len(matriz)
    matriz[y][x][i] = elemento
    retorno = True
    if isInteger(elemento):
        for posicao in posicoesAfetadas((y,x)):
            lista = matriz[posicao[0]][posicao[1]][i]
            if not isInteger(lista):
                if elemento in lista:
                    if len(lista) == 1:
                        return False
                    lista.remove(elemento)
    return True

def devolve(coord,elemento):
    global matriz
    y,x,i = coord
    tamanho = len(matriz)
    possibilidades(coord)
    for y,x in posicoesParaAlterar(coord):
        if elemento not in numerosQueAfetam((y,x,i))+matriz[y][x][i]:
            matriz[y][x][i].append(elemento)

def melhorCoord():
    global matriz
    global usados
    tamanho = len(matriz)
    menor = tamanho+1
    coordDoMenor = tamanho
    if len(usados)==tamanho:
        for x in range(tamanho):
            for y in range(tamanho):
                if not isInteger(matriz[y][x][0]):
                    tamanhoLista = len(matriz[y][x][0])
                    if tamanhoLista < menor:
                        menor = tamanhoLista
                        coordDoMenor = (y,x,0)
                        if menor == 1:
                            return coordDoMenor
    if menor != tamanho+1:
        return coordDoMenor
    else:
        for x in range(tamanho):
            for y in range(tamanho):
                if not isInteger(matriz[y][x][1]):
                    tamanhoLista = len(matriz[y][x][1])
                    if tamanhoLista < menor:
                        menor = tamanhoLista
                        coordDoMenor = (y,x,1)
                        if menor == 1:
                            return coordDoMenor
    if menor == tamanho+1:
        coordDoMenor = (0,0,0)
    return coordDoMenor

def solve():
    global matriz
    global iterations
    global usados
    global taxaDeImpressao
    y,x,i = melhorCoord()
    if iterations%taxaDeImpressao==0:
        imprime()
        print()
    iterations += 1
    if len(usados) >= len(matriz)**2:
        return matriz
    poss = matriz[y][x][i].copy()
    for possibilidade in poss:
        if i == 1 :
            elemento = [matriz[y][x][0],possibilidade]
            if elemento in usados:
                continue
            else:
                usados.append(elemento)
        if coloca((y,x,i),possibilidade):
            matriz[y][x][i] = possibilidade
            solucao = solve()
            if solucao:
                return solucao
        if i == 1:
            usados.remove(elemento)
        devolve((y,x,i),possibilidade)

def fazMatriz(tamanho,indice):
    global matriz
    matriz = [[[[a for a in range(tamanho)],[a for a in range(tamanho)]] for b in range(tamanho)] for c in range(tamanho)]
    for x in range(tamanho):
        for i in range(indice):
            coloca((0,x,i),x)
    return matriz

taxaDeImpressao = 1000000
tabulacao = 20


iterations = 0
tamanho = 8
indice = 2
matriz = []
fazMatriz(tamanho,indice)
usados = [[a,a] for a in range(tamanho)]
matriz = solve()
imprime()
