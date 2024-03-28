from random import shuffle
from random import randint

class Carta:
    def __init__(self,naipe,figura):
        self.naipe  = naipe
        self.figura = figura

    def compara(self,obj,figuraManilha):
        if not type(self) is type(obj):
            return 1
        if self.figura == figuraManilha:
            if obj.figura != figuraManilha:
                return 1
            if self.naipe > obj.naipe:
                return 1
            else:
                return -1
        if obj.figura == figuraManilha:
            return -1
        if self.figura > obj.figura:
            return 1
        if obj.figura == self.figura:
            return 0
        return -1
    
    def imprime(self):
        print(str(self))

    def __str__(self):
        texto = ''
        figuras = ['4','5','6','7','Q','J','K','A','2','3']
        naipes = ['Ouro','Espadilha','Copas','Paus']
        texto += figuras[self.figura]
        texto += ' '
        texto += naipes[self.naipe]
        return texto

    def __eq__(self,obj):
        if not type(self) is type(obj):
            return False
        if self.naipe != obj.naipe:
            return False
        if self.figura != obj.figura:
            return False
        return True

class Baralho:
    def __init__(self):
        self.cartas = []
        for figura in range(10):
            for naipe in range(4):
                carta = Carta(naipe,figura)
                self.cartas.append(carta)

    def embaralha(self,seed):
        for elemento in list(seed):
            carta = self.cartas.pop(ord(elemento)%40)
            self.cartas = [carta] + self.cartas

    def corta(self, numero = -1):
        if numero < 0:
            corteTotal = randint(0,len(self)-1)
        else:
            corteTotal = numero
        for _ in range(corteTotal):
            self.addCarta(self.pegaCarta())

    def imprime(self):
        for n,carta in enumerate(self.cartas):
            print(('0'+str(n) if n<10 else str(n)) + ' : ' + str(carta))

    def pegaCarta(self,cima = True):
        if cima:
            return self.cartas.pop(0)
        else:
            return self.cartas.pop(-1)

    def addCarta(self, carta, baixo = True):
        if baixo:
            self.cartas = self.cartas + [carta]
        else:
            self.cartas = [carta] + self.cartas

    def __len__(self):
        return len(self.cartas)

    def __str__(self):
        texto = ''
        for n,carta in enumerate(self.cartas):
            texto += ('0'+str(n) if n<10 else str(n)) + ' : ' + str(carta) + '\n'
        return texto

    def __eq__(self,obj):
        if not type(self) is type(obj):
            return False
        for n,carta in enumerate(self.cartas):
            if carta != obj.cartas[n]:
                return False
        return True
