from EstruturasBaralho import Baralho
from EstruturasBaralho import Carta
from random import randint

class Mao:
    def __init__(self):
        self.cartas = []

    def imprime(self):
        for carta in self.cartas:
            print(str(carta))
    
    def add(self,carta):
        self.cartas.append(carta)
        
    def getCarta(self,indice):
        return self.getCartas()[indice]
        
    def getCartas(self):
        return self.cartas
    
    def removeCarta(self,indice):
        return self.cartas.pop(indice)

    def __str__(self):
        texto = ''
        for carta in self.cartas:
            texto += str(carta) + '\n'
        return texto

    def __len__(self):
        return len(self.cartas)

class Jogador:
    def __init__(self, ordem, isHuman = False):
        self.mao = Mao()
        self.isHuman = isHuman
        self.indice = ordem
        texto = 'xyzSTUVWXYZ345678abcdefghijklmnopqrstuvw'
        self.embaralhamento = ''
        for a in range(randint(10,100)):
            self.embaralhamento += texto[randint(0,39)]
        self.corte = randint(0,39)

    def embaralha(self,baralho):
        baralho.embaralha(self.embaralhamento)
        
    def corta(self,baralho):
        #if isHuman:
        baralho.corta(self.corte)

    def distribuiCartas(self,baralho,jogadores):
        #if isHuman:
        viraVez = randint(1,len(jogadores)*3)
        cartaCont = 0
        for _ in range(3):
            for jogador in jogadores:
                jogador.recebeCarta(baralho.pegaCarta())
                cartaCont += 1
                if cartaCont == viraVez:
                    vira = baralho.pegaCarta()
        return vira

    def jogaAleatorio(self):
        return self.mao.removeCarta(randint(0,len(self.mao)-1))

    def jogaMaior(self,manilha):
        maiorCartaIndice = 0
        maiorCarta = self.mao.getCarta(maiorCartaIndice)
        for indice in range(1,len(self.mao)):
            carta = self.mao.getCarta(indice)
            if carta.compara(maiorCarta,manilha) == 1:
                maiorCartaIndice = indice
                maiorCarta = self.mao.getCarta(maiorCartaIndice)                
        return self.mao.removeCarta(maiorCartaIndice)
    
    def recebeCarta(self,carta):
        self.mao.add(carta);
        
    def imprime(self):
        if self.isHuman:
            print('Jogador ' + str(self.indice) + ':')
        else:
            print('PC ' + str(self.indice) + ':')
        self.mao.imprime()
        
    def __str__(self):
        texto = ''
        if self.isHuman:
            texto += 'Jogador '
        else:
            texto += 'PC '
        texto += str(self.indice) + ':\n'
        texto += str(self.mao)

class Partida:
    def __init__(self,vira,jogadores,jogadorInicial):
        self.jogadores = jogadores
        self.manilha = (vira.figura + 1)%10
        self.rodada = 0
        self.vira = vira
        self.vez = jogadorInicial % len(jogadores)
        self.ganhadoresDasRodadas = [-1,-1,-1]
        self.ganhadores = []
        self.rodadas = []
        self.isEmpatado = False      

    def jogaRodada(self, modo = 'random'):
        totalJogadores = len(self.jogadores)
        rodada = [0 for a in range(totalJogadores)]
        maiorCarta = (self.vez+1)%totalJogadores
        empate = False
        print()
        for n in range(totalJogadores):
            jogador = self.jogadores[self.vez]
            if self.isEmpatado:
                rodada[self.vez] = jogador.jogaMaior(self.manilha)
                self.isEmpatado = False
            else:
                if modo == 'maior':
                    rodada[self.vez] = jogador.jogaMaior(self.manilha)
                else:
                    rodada[self.vez] = jogador.jogaAleatorio()
            print("Jogador " if jogador.isHuman else "PC " + str(self.vez) + " : " + str(rodada[self.vez]))
            situacao = rodada[self.vez].compara(rodada[maiorCarta],self.manilha)
            if situacao == 1:
                maiorCarta = self.vez
                print("maior")
                empate = False
            elif situacao == 0:
                print("empatou")
                empate = True
            self.vez += 1
            self.vez %= totalJogadores
        print()
        if empate:
            self.isEmpatado = True
        else:
            self.isEmpatado = False
            self.ganhadoresDasRodadas[self.rodada] = maiorCarta%totalJogadores
            self.vez = maiorCarta
        self.rodadas.append(rodada)
        self.rodada += 1

    def isFinished(self):
        if self.ganhadores:
            return True
        if self.rodada == 0:
            return False
        if self.ganhadoresDasRodadas[0] == -1:
            if self.rodada == 1:
                return False
            else:
                if self.ganhadoresDasRodadas[1] == -1:
                    if self.rodada == 2:
                        return False
                    else:
                        if self.ganhadoresDasRodadas[2] == -1:
                            self.ganhadores = [a for a in range(len(self.jogadores))]
                            return True
                        else:
                            self.ganhadores = [a for a in range(self.ganhadoresDasRodadas[2]%2,len(self.jogadores),2)]
                            return True
                else:
                    self.ganhadores = [a for a in range(self.ganhadoresDasRodadas[1]%2,len(self.jogadores),2)]
                    return True
        else:
            if self.rodada == 1:
                return False
            else:
                if self.ganhadoresDasRodadas[1] == self.ganhadoresDasRodadas[0]:
                    self.ganhadores = [a for a in range(self.ganhadoresDasRodadas[0]%2,len(self.jogadores),2)]
                    return True
                else:
                    if self.ganhadoresDasRodadas[1] == -1:
                        self.ganhadores = [a for a in range(self.ganhadoresDasRodadas[0]%2,len(self.jogadores),2)]
                        return True
                    else:
                        if self.rodada == 2:
                            return False
                        else:
                            if self.ganhadoresDasRodadas[2] == -1:
                                self.ganhadores = [a for a in range(self.ganhadoresDasRodadas[0]%2,len(self.jogadores),2)]
                                return True
                            else:
                                self.ganhadores = [a for a in range(self.ganhadoresDasRodadas[2]%2,len(self.jogadores),2)]
                                return True

    def devolveCartas(self,baralho):
        for rodada in self.rodadas:
            for carta in rodada:
                baralho.addCarta(carta)
        for indice in range(3-self.rodada):
            for jogador in self.jogadores:
                baralho.addCarta(jogador.mao.removeCarta(indice))
        baralho.addCarta(self.vira)

    def whoWon(self):
        return self.ganhadores

    def imprime(self):
        for jogador in self.jogadores:
            jogador.imprime()
            print()
        self.vira.imprime()

    def __str__(self):
        texto = ''
        for jogador in self.jogadores():
            texto += str(jogador) + '\n\n'
        texto += str(self.vira)
        return texto

class Jogo:
    def __init__(self,participantes):
        self.baralho = Baralho()
        self.jogadores = [Jogador(a) for a in range(participantes)]
        self.pontos = [0 for a in range(participantes)]
        self.vez = 0
        self.ultimaPartida = 0

    def jogaPartida(self,modo = 'random'):
        self.getJogador(0).embaralha(self.baralho)
        self.getJogador(-1).corta(self.baralho)
        vira = self.getJogador(0).distribuiCartas(self.baralho,[self.getJogador(a) for a in range(1,len(self.jogadores)+1)])
        partida = Partida(vira,self.jogadores,self.vez+1)
        partida.imprime()
        while not partida.isFinished():
            partida.jogaRodada(modo = modo)
        ganhadores = partida.whoWon()
        print(ganhadores)
        for ganhador in ganhadores:
            self.pontos[ganhador] += 1
        partida.devolveCartas(self.baralho)
        self.vez += 1
        self.ultimaPartida = partida
        

    def getJogador(self,indice):
        return self.jogadores[(self.vez+indice)%len(self.jogadores)]

##jogo = Jogo(6)
##jogo.jogaPartida()
##print(5*'\n')
##n = 1
##while(12 not in jogo.pontos):
##    jogo.jogaPartida(modo = 'maior')
##    print(5*'\n')
##    n += 1
##print(jogo.pontos)
##print(n)
