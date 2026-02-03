import pytesseract as ocr
import time
import os
from PIL import Image


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



def main() -> None:
    start = time.time()
    nome = os.path.join("jap", "1.png")
    print("\n" + nome)
    imagem = Image.open(nome)
    largura, altura = imagem.size()
    # phrase = ocr.image_to_string(Image.open(nome), lang="jp")
    # print(phrase)
    # final=time.time()
    # print("demorou ")
    # print_elapsed_time(final-start)


if __name__ == "__main__":
    main()