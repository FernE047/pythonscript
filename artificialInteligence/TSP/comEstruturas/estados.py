#NoBatch

class Estado:
    def __init__(self, grafo, caminhoFeito = None, trajetoTotal = None):
        self.grafo = grafo
        if caminhoFeito == None:
            self.caminho = []
        else:
            self.caminho = caminhoFeito
        if trajetoTotal == None:
            self.custo = 0
        else:
            self.custo = trajetoTotal

    def geraFilhos(self):
        filhos = []
        for index in range(len(self.grafo)):
            if index not in self.caminho:
                filhos.append(self.fazMovimento(index))
        return filhos

    def fazMovimento(self,movimento):
        estado = self.copy()
        custoTotal = estado.custo
        if self.caminho :
            custoTotal += self.grafo.getElement((self.caminho[-1],movimento))
        caminhoFeito = estado.caminho + [movimento]
        return Estado(self.grafo, caminhoFeito, custoTotal)

    def copy(self):
        caminhoFeito = self.caminho.copy()
        return Estado(self.grafo,caminhoFeito,self.custo)

    def imprime(self):
        estado = Estado(self.grafo)
        self.grafo.imprime()
        print()
        print(str(estado),end='\n\n')
        for movimento in self.caminho[1:]:
            estado = estado.fazMovimento(movimento)
            print(str(estado),end='\n\n')
        print("\n\n\n\n\n\n")
        return estado

    def __str__(self):
        texto = ''
        texto += 'caminho : ' + str(self.caminho)
        texto += '\ncusto   : ' + str(self.custo)
        return texto

    def __eq__(self,obj): 
        if type(obj) is type(self):
            if self.custo != obj.custo:
                return False
            for elemento in self.caminho:
                if elemento not in obj.caminho:
                    return False
            return True
        return False
