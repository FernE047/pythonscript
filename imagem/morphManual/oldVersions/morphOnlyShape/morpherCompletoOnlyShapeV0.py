import subprocess
from time import time

# this code is legacy, I am only changing type hints and linter errors. it doesn't make sense to refactor it, since I already have a better version of it, and I don't want to break it by changing it too much


def print_elapsed_time(seconds: float) -> None:
    if seconds < 0:
        seconds = -seconds
        sign = "-"
    else:
        sign = ""
    total_ms = int(round(seconds * 1000))
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
    print(f"{sign}{', '.join(parts)}")

#esse algoritmo faz o morph completo

def fazProcesso(processo: str,nome: str) -> None:
    print(nome)
    inicio = time()
    subprocess.call(processo)
    fim = time()
    duracao = fim-inicio
    print_elapsed_time(duracao)


def main() -> None:
    inicioDef = time()
    fazProcesso("python ./analisaEFazConfig.py ","fazer configurações")
    fazProcesso("python ./morpher.py ","fazer animações")
    fimDef = time()
    print("\nfinalizado")
    print_elapsed_time(fimDef-inicioDef)
    input()


if __name__ == "__main__":
    main()