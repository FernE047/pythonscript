import pytesseract as ocr
import time
import os


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


from PIL import Image


def descobre(nome):
    imagem = Image.open(nome)
    larg, alt = imagem.size
    for x in range(larg):
        for y in range(alt):
            pixel = imagem.getpixel((x, y))
            if pixel == (100, 191, 96):
                print((x, y))


start = time.time()
nome = os.path.join("jap", "1.png")
print("\n" + nome)
imagem = Image.open(nome)
imagemCut = imagem.crop((34, 909, 671, 1072))
imagemCut.save("cut.png")
# phrase = ocr.image_to_string(imagemCut, lang="jp")
# print(phrase)
final = time.time()
print("demorou ")
print_elapsed_time(final - start)
