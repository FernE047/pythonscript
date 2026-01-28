from estruturas import Collatz
from estruturas import Funcao
from estruturas import Regra
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

inicial=5   #min=2
final=6
collatzFuturo=Collatz(inicial)
tempos=[]
for a in range(inicial,final):
    inicio=time()
    saida = open(f'collatz{a}de{a+1}.txt','w')
    collatzAtual = collatzFuturo
    collatzFuturo = Funcao()
    saida.write(str(collatzAtual)+'\n')
    regrasPrincipais = collatzAtual.getRegras(['principal'])
    regrasAtivas = collatzAtual.getRegras(['ativa'])
    regrasPassivas = collatzAtual.getRegras(['passiva'])
    for regra in regrasPassivas:
        collatzFuturo.addRegra(regra.copia())
    for regra in regrasPrincipais:
        regraNova=regra.copia()
        regraNova.setTipo('passiva')
        collatzFuturo.addRegra(regraNova)
    for regra1 in regrasAtivas:
        for regra2 in collatzAtual.estruturaReal().getRegras():
            saida.write('passo 1 :\n\n\n')
            newFormato=regra1.resolvePara(regra2,saida=saida)
            saida.write('\n')
            if(newFormato):
                newFormula=regra1.getFormula().copia()
                if(regra2.getTipo()=='ativa'):
                    newRegra=Regra(newFormato,newFormula,'ativa')
                    collatzFuturo.addRegra(newRegra)
                else:
                    for regra3 in regrasAtivas:
                        texto='\n'.join(['',str(regra1),str(regra2),str(regra3),''])
                        formula1=regra1.getFormula().copia()
                        formula2=regra2.getFormula().copia()
                        formula3=regra3.getFormula().inversa().copia()
                        texto+='\n'.join([str(formula1),str(formula2),str(formula3),''])
                        formula4=formula3.aplica(formula2.aplica(formula1))
                        texto+=str(formula4)+'\n'
                        formatoDestino=regra3.getFormato()
                        texto+='\n'.join([str(formula4),str(newFormato),str(formatoDestino),''])
                        saida.write(texto)
                        newFormato2=newFormato.resolvePara(formatoDestino,formula4,saida=saida)
                        saida.write('teste : '+str(newFormato2)+'\n')
                        if(newFormato2):
                            newRegra=Regra(newFormato2,formula4,'principal')
                            collatzFuturo.addRegra(newRegra)
    saida.close()
    fim=time()
    print(f'collatz {a+1} : ')
    print(collatzFuturo)
    collatzFuturo.salva(a+1)
    tempos.append(fim-inicio)
    print(embelezeTempo(tempos[-1]))
    print('\n')
if(len(tempos)>1):
    somaTempos=0
    for tempo in tempos:
        somaTempos+=tempo
    print('total : '+embelezeTempo(somaTempos))
