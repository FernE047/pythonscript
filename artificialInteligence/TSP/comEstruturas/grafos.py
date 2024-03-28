#NoBatch

class Grafo:
    def __init__(self, tamanho = None, grafoBase = None):
        if grafoBase == None:
            if tamanho == None:
                self.tamanho = 1
                self.matriz = [[0]]
            else:
                self.tamanho = tamanho
                self.matriz = [[0 for n in range(tamanho)] for m in range(tamanho)]
        else:
            self.tamanho = len(grafoBase)
            self.matriz = grafoBase

    def getElement(self,coord):
        return self.matriz[coord[0]][coord[1]]

    def setElement(self,coord,valor,symmetry = True):
        self.matriz[coord[0]][coord[1]] = valor
        if symmetry:
            self.matriz[coord[1]][coord[0]] = valor

    def imprime(self):
        print(str(self))

    def __str__(self):
        texto = []
        for linha in self.matriz:
            texto.append(' '.join([' '*(3-len(str(elemento)))+str(elemento) for elemento in linha]))
        return '\n'.join(texto)
            
    def __len__(self):
        return self.tamanho

def GrafoFromArq(nome, lim = None):
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
        vertices.append((float(x),float(y)))
        linha = file.readline()
        if lim:
            indice += 1
    grafo = Grafo(len(vertices))
    for n,origem in enumerate(vertices):
        for m,destino in enumerate(vertices):
            coord = (n,m)
            distancia = ((destino[0]-origem[0])**2+(destino[1]-origem[1])**2)**0.5
            grafo.setElement(coord,distancia,False)
    return grafo
