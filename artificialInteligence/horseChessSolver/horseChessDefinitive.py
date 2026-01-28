from time import time

def embelezeTempo(segundos: float) -> str:
    if segundos < 0:
        segundos = -segundos
        sign = "-"
    else:
        sign = ""
    total_ms = int(round(segundos * 1000))
    ms = total_ms % 1000
    total_s = total_ms // 1000
    s = total_s % 60
    total_min = total_s // 60
    m = total_min % 60
    total_h = total_min // 60
    h = total_h % 24
    d = total_h // 24
    parts: list[str] = []
    def add(value: int, singular: str, plural: str) -> None:
        if value:
            parts.append(f"{value} {singular if value == 1 else plural}")
    add(d, "day", "days")
    add(h, "hour", "hours")
    add(m, "minute", "minutes")
    add(s, "second", "seconds")
    if ms or not parts:
        parts.append(f"{ms} millisecond" if ms == 1 else f"{ms} milliseconds")
    return sign + ", ".join(parts)

class Tabuleiro:
    def __init__(self,dimensoes,tamanho=8,pos=[]):
        self.dimensoes = dimensoes
        self.tamanho = tamanho
        self.pos = pos
        if(self.dimensoes == 1):
            self.matriz = [False for a in range(tamanho)]
        else:
            self.matriz = Tabuleiro(self.dimensoes-1,self.tamanho)

    def setPos(self,pos):

    def setPosValue(self,value):
        if()

def criaMatrizSquare(dimensoes,tamanho):
    if(dimensoes==0):
        return False
    else:
        return [criaMatrizSquare(dimensoes-1,tamanho) for a in range(tamanho)]

def resolveUmTabuleiro(tabuleiro):
    print()
    global tries
    tries=0
    inicio = time()
    solucao = resolveTabuleiro(tabuleiro)
    fim = time()
    print("\ntentativas: "+str(tries))
    tempo = fim-inicio
    print("\n"+embelezeTempo(tempo)+"\n\n\n")

tabuleiro = criaTabuleiroSquare(3,5)
print(tabuleiro)
resolveUmTabuleiro(tabuleiro)
