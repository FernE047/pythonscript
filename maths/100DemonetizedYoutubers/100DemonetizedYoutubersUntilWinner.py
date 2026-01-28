import random
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

def imprimeDados(probIndividual,total):
    print('\ntotal : '+str(total)+'\n\ncoletivo')
    for participante,prob in enumerate(probIndividual):
        if(prob!=0):
            print(f'participante {participante} : {prob*100/total:.20f}%')
    print('\nindividual')
    for participante,quant in enumerate(probIndividual):
        if(quant!=0):
            print(f'participante {participante} : {quant}')
    print()
    print('total : '+str(total))
    print()

total=0
participante=1
probIndividual=[0 for a in range(100)]
inicioDefinitivo=time()
comeco=time()
try:
    while True:
        total+=1
        for participante in range(100):
            ehCerto=False
            chutes=random.sample(range(participante,100),50)
            for tentativa in range(50):
                chute=chutes[tentativa]
                if(chute==participante):
                    ehCerto=True
                    break
            if(not(ehCerto)):
                probIndividual[participante]+=1
                break
        if(ehCerto):
            print('temos um ganhador')
            break
    fim=time()
    imprimeDados(probIndividual,total)
    duracao=fim-comeco
    print('execução total : '+embelezeTempo(duracao))
    print('media total :    '+embelezeTempo((duracao)/total))
except:
    fim=time()
    imprimeDados(probIndividual,total)
    duracao=fim-comeco
    print('execução total : '+embelezeTempo(duracao))
    print('media total :    '+embelezeTempo((duracao)/total))
    print('expectativa 100k : '+embelezeTempo(((duracao)/total)*100000))
#media total :    0.0005307446075174813 segundos
#expectativa 100k : 53.07446075174813 segundos
