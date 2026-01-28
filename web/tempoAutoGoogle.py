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

quantia=1
while quantia!=0:
    trying = True
    while trying:
        try:
            print("\nquantos termos a pesquisar?")
            quantia = int(input())
            trying = False
        except:
            print("digite um número")
    if(quantia!=0):
        minimo = quantia*25
        media = quantia*50
        maximo = quantia*75
        print("\nminimo : "+embelezeTempo(minimo))
        print("media : "+embelezeTempo(media))
        print("maximo : "+embelezeTempo(maximo))
