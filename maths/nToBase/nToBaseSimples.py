import math


def nToBase(n, base):
    global LIMITE
    sequencia = []
    potenciaMaior = int(math.log(n, base))
    for potencia in range(potenciaMaior, LIMITE - 1, -1):
        termo = base**potencia
        fator = int(n / termo)
        n -= fator * termo
        sequencia.append(str(fator))
        if potencia == 0:
            if LIMITE != 0:
                sequencia.append(",")
    numero = "".join(sequencia)
    return numero


def impressao(n, base, tamanhoBase=0, tamanhoN=3):
    global LIMITE
    if tamanhoBase == 0:
        tamanhoBase = 10 - LIMITE
    resultado = nToBase(n, base)
    mensagem = []
    mensagem.append(str(base))
    mensagem.append((" : {0:0" + str(tamanhoN) + "} : ").format(n))
    mensagem.append((" {:0>" + str(tamanhoBase) + "}").format(resultado))
    print("".join(mensagem))


LIMITE = -100
base = 11
for n in range(1, 101):
    impressao(n, base)
