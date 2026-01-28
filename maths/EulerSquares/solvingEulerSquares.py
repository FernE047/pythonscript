def imprime(matriz):
    if matriz:
        for linha in matriz:
            print(" ".join([str(elemento) for elemento in linha]))
    else:
        print("nao existe solução")

def verifica(matriz,xLim,yLim):
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

def solve(x,y,matriz,possibilidades):
    global tries
    global iterations
    if iterations%100000==0:
        print(f"{iterations:,}")
        print(f"{tries:,}")
        imprime(matriz)
        print()
    iterations += 1
    if(y==len(matriz)):
        return matriz
    for indice in range(len(possibilidades)):
        tries += 1
        elemento = possibilidades[indice]
        if elemento == 0:
            continue
        possibilidades[indice] = 0
        matriz[y][x] = elemento
        if verifica(matriz,x,y):
            if(x==len(matriz[0])-1):
                solucao = solve(0,y+1,matriz,possibilidades)
            else:
                solucao = solve(x+1,y,matriz,possibilidades)
            if solucao:
                return solucao
        matriz[y][x] = (0,0)
        possibilidades[indice] = elemento

tries = 0
iterations = 0
tamanho = 5
largura = tamanho
altura  = tamanho
possibilidades = []
for x in range(largura):
    for y in range(altura):
        if x != y:
            possibilidades.append((x,y))
matriz = [[(a,a) for a in range(largura)]]+[[(0,0) for x in range(largura)] for y in range(1,altura)]
matriz = solve(0,1,matriz,possibilidades)
imprime(matriz)
