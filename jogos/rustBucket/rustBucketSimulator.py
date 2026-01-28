from PIL import Image

'''

TIPOS:

0 - ignora
1 - slime    (0,0,255)
2 - porco    (255,<255,255)
3 - fantasma (0,255,255)
4 - lula     (255,255,0)
5 - polvo    (0,127,0)
6 - verde    (0,255,0)
7 - caveira  (0,127,0)(opc)

DIRECAO:

0 - cima
1 - direita
2 - baixo
3 - esquerda
4 - cima + direita
5 - cima + esquerda
6 - baixo + direita
7 - baixo + esquerda

'''

class Node:
    def __init__(self, aType, aCoord, aCaminhoFeito = None):
        self.coord = aCoord
        if aType[:7] == "caveira":
            self.type = 1
        else:
            self.type = ["misc","slime","porco","fantasma","lula","polvo","verde"].index(aType)
        if aCaminhoFeito == None:
            self.caminhoFeito = []
        else:
            self.caminhoFeito = aCaminhoFeito

    def setCaminhoFeito(self, aCaminhoFeito):
        self.caminhoFeito = CaminhoFeito

    def getValue(self):
        if self.type in (1,3):
            return sum([2**(len(self.caminhoFeito)-1-i)*[1,0,1,0][self.caminhoFeito[i]] for i in range(len(self.caminhoFeito))])
        elif self.type == 2:
            direcao = self.caminhoFeito[0]
            custo = [0]
            for coord in self.caminhoFeito:
                if coord == direcao:
                    custo[-1] += 1
                else:
                    direcao = coord
                    custo.append(1)
            return custo
        else:
            return len(self.caminhoFeito)

    def getCaminhoFeito(self):
        return self.caminhoFeito

    def getType(self):
        return ["misc","slime","porco","fantasma","lula","polvo","verde"][self.type]

    def valido(self,mapa):
        if self.type not in (4,5):
            if max(self.caminhoFeito)>3:
                return False
        elif self.type == 4:
            if min(self.caminhoFeito)<4:
                return False
        if self.type == 3:
            return True
        for i in range(2):
            if self.coord[i] < 0:
                return False
            if self.coord[i] >= mapa.size[i]:
                return False
        if mapa.getpixel(self.coord) not in ((255,255,255),(255,255,255,255),(255,0,0),(255,0,0,255)):
            return False
        return True

    def copia(self,direcao):
        novaCoord = move(self.coord, direcao)
        novoCaminhoFeito = self.caminhoFeito.copy()
        novoCaminhoFeito.append(direcao)
        return Node(self.getType(),tuple(novaCoord),novoCaminhoFeito)

    def __eq__(self,obj):
        return self.coord == obj.coord

    def __gt__(self,obj):
        if self.type == 2:
            valueSelf = self.getValue()
            valueObj = obj.getValue()
            if len(valueObj) == len(valueSelf):
                return sum([valueSelf[i]*2**(len(valueSelf)-i) for i in range(len(valueSelf))]) > sum([valueObj[i]*2**(len(valueObj)-i) for i in range(len(valueObj))])
            else:
                return len(valueObj) > len(valueSelf)
        else:
            return self.getValue() >= obj.getValue()

    def __str__(self):
        texto = []
        texto.append("TIPO : " + self.getType())
        texto.append(str(self.coord))
        texto.append(str(self.getValue()))
        if self.caminhoFeito != None:
            if self.type == 2:
                lista = self.caminhoFeito[1:]
            else:
                lista = self.caminhoFeito
            texto.append(', '.join([["cima","direita","baixo","esquerda","cimeita","cimerda","baixeita","baixerda"][direcao] for direcao in lista]))
        return '\n'.join(texto)

class Elemento:
    def __init__(self, aType, aCoord):
        self.coord = aCoord
        self.type = aType
        if self.type[:5] == "porco":
            self.direcao = int(self.type[-3:])%4
            self.type = self.type[:5]
            self.categoria = self.type[5:-3]

    def nextTurn(self, elementos, mapa):
        cor = mapa.getpixel(self.coord)
        mapa.putpixel((self.coord),(255,255,255,255))
        print(self.coord)
        if self.type != "hero":
            if self.type[:5] == "porco":
                caminho = self.melhorCaminho(elementos[0], Node(self.type[:5],self.coord,[self.direcao]), mapa)[1:]
                print(self.melhorCaminho(elementos[0], Node(self.type[:5],self.coord,[self.direcao]), mapa))
            else:
                caminho = self.melhorCaminho(elementos[0], Node(self.type,self.coord), mapa)
                print(self.melhorCaminho(elementos[0], Node(self.type,self.coord), mapa))
            if caminho:
                passo = caminho[0]
                self.direcao = passo
                self.coord = move(self.coord,passo)
            print(self.coord)
            print()
        mapa.putpixel((self.coord),cor)

    def avaliaProximos(self, mapa, nodesAtuais, nodesAnteriores):
        nodesFuturos = []
        for node in nodesAtuais:
            for direcao in range(8):
                novoNode = node.copia(direcao)
                if not novoNode.valido(mapa):
                    continue
                if novoNode not in nodesAnteriores:
                    novoNodeEncontrado = False
                    #print(novoNode)
                    for node_futuro in nodesFuturos:
                        if novoNode == node_futuro:
                            novoNodeEncontrado = True
                            if novoNode > node_futuro:
                                node_futuro = novoNode
                            break
                    if not novoNodeEncontrado:
                        nodesFuturos.append(novoNode)
        return nodesFuturos

    def melhorCaminho(self, objetivo, inicio, mapa):
        nodesAtuais = self.avaliaProximos(mapa,[inicio],[])
        #imprime(nodesAtuais)
        nodesAnteriores = [inicio]
        while objetivo not in nodesAtuais:
            nodesFuturos = self.avaliaProximos(mapa, nodesAtuais, nodesAnteriores)
            nodesAnteriores = nodesAtuais
            nodesAtuais = nodesFuturos
            if not nodesAtuais:
                return []
            #imprime(nodesAtuais)
        for node in nodesAtuais:
            if node == objetivo:
                return node.caminhoFeito

def move(coord, direcao):
    novaCoord = list(coord).copy()
    if direcao == 0:
        novaCoord[1] -= 1
    elif direcao == 1:
        novaCoord[0] += 1
    elif direcao == 2:
        novaCoord[1] += 1
    elif direcao == 3:
        novaCoord[0] -= 1
    elif direcao == 4:
        novaCoord[1] -= 1
        novaCoord[0] += 1
    elif direcao == 5:
        novaCoord[1] -= 1
        novaCoord[0] -= 1
    elif direcao == 6:
        novaCoord[1] += 1
        novaCoord[0] += 1
    elif direcao == 7:
        novaCoord[1] += 1
        novaCoord[0] -= 1
    return tuple(novaCoord)
        

def imprime(nodes):
    for node in nodes:
        print(node,end="\n\n")

def leMapa(mapa):
    largura,altura = mapa.size
    elementos = []
    for x in range(largura):
        for y in range(altura):
            coord = (x,y)
            cor = mapa.getpixel(coord)
            if cor in ((255,0,0,255),(255,0,0)):
                elementos = [Elemento("hero",coord)]+elementos
            if cor in ((0,0,255,255),(0,0,255)):
                elementos.append(Elemento("slime",coord))
            if (cor[0] == 255) and (cor[2] == 255) and (cor[1] < 255):
                tom = cor[1]
                if tom in range(128,132):
                    elementos.append(Elemento(f"porco{cor[1]:03d}",coord))
                elif tom in range(88,92):
                    elementos.append(Elemento(f"porcoMetal{cor[1]:03d}",coord))
                elif tom in range(48,52):
                    elementos.append(Elemento(f"porcoOuro{cor[1]:03d}",coord))
                elif tom in range(0,4):
                    elementos.append(Elemento(f"porcoEstatua{cor[1]:03d}",coord))
            if (cor[0] == 0) and (cor[1] == 255) and (cor[2] == 255):
                elementos.append(Elemento("fantasma",coord))
            if (cor[0] == 0) and (cor[1] == 127) and (cor[2] == 255):
                elementos.append(Elemento("caveira",coord))
            if (cor[0] == 255) and (cor[1] == 255) and (cor[2] == 0):
                elementos.append(Elemento("lula",coord))
            if (cor[0] == 0) and (cor[1] == 127) and (cor[2] == 0):
                elementos.append(Elemento("polvo",coord))
            if (cor[0] == 0) and (cor[1] == 255) and (cor[2] == 0):
                elementos.append(Elemento("verde",coord))
            if (cor[0] == 0) and (cor[1] == 73) and (cor[2] == 73):
                elementos.append(Elemento("caveiraEstatua",coord))
    return elementos

imagem = Image.open("input.png")
elementos = leMapa(imagem)
a = 0
while True:
    for elemento in elementos[1:]:
        print("b")
        print(elemento.type)
        elemento.nextTurn(elementos,imagem)
    imagem.save("anima\\frame"+str(a)+".png")
    a += 1
    if(imagem.getpixel(elementos[0].coord) not in ((255,0,0,255),(255,0,0))):
        break
imagem.close()
