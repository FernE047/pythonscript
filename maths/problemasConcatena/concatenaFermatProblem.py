from time import time


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
    print(sign + ", ".join(parts))


def pos(a, pot):
    respostas = []
    a = a**pot
    for b in range(1, a):
        bPot = b**pot
        textB = str(bPot)
        for c in range(a):
            cPot = c**pot
            textC = str(cPot)
            textNum = textB + textC
            num = int(textNum)
            if num > a:
                break
            if num == a:
                respostas.append((b, c))
    return respostas


def faz(limit, pot):
    tempoRecorde = 0
    for t in range(limit):
        inicio = time()
        num = pos(t, pot)
        if num:
            print(str(t) + " : " + str(t**pot))
            for resp in num:
                print(str(resp[0]) + "," + str(resp[1]))
            print("")
        fim = time()
        duracao = fim - inicio
        if duracao >= tempoRecorde:
            print(str(t) + " :")
            print_elapsed_time(duracao)
            tempoRecorde = duracao
            resto = limit - t
            print("falta :")
            print_elapsed_time(duracao * resto)


faz(10000, 2)
