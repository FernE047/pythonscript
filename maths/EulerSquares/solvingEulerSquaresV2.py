def imprime(matriz):
    global iterations
    print("Iteracoes Totais " +str(iterations))
    if matriz:
        for linha in matriz:
            print(" ".join([str(elemento) for elemento in linha]))
    else:
        print("nao existe solução")

def verifica(matriz,xLim,yLim,elemento):
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

def possibilidades(matriz,x,y,usados):
    lista = []
    tamanho = len(matriz)
    for a in range(tamanho):
        for b in range(tamanho):
            if (a,b) not in usados:
                if(verifica(matriz,x,y,(a,b))):
                    lista.append((a,b))
    return lista

def solve(x,y,matriz,usados):
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

iterations = 0
tamanho = 5
largura = tamanho
altura  = tamanho
usados = [(a,a) for a in range(largura)]
matriz = [usados.copy()]+[[(0,0) for x in range(largura)] for y in range(1,altura)]
matriz = solve(0,1,matriz,usados)
imprime(matriz)
