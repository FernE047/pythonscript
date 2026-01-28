import subprocess
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

#esse algoritmo faz o morph completo

def fazProcesso(processo,nome):
    inicio = time()
    subprocess.call (processo)
    fim = time()
    duracao = fim-inicio
    print(nome+" demorou : "+embelezeTempo(duracao))
    
inicioDef = time()
fazProcesso("python C:\\pythonscript\\imagem\\morphOnlyShape\\analisaEFazConfig.py ","fazer configurações")
fazProcesso("python C:\\pythonscript\\imagem\\morphOnlyShape\\morpher.py ","fazer animações")
fimDef = time()
print("\nfinalizado")
print("execução : "+embelezeTempo(fimDef-inicioDef))
a = input()
