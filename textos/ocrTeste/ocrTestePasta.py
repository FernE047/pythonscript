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


def tiraEspaçoBranco(texto: str) -> str:
    for espaco in [" ", "\n", "\t"]:
        if espaco in texto:
            texto = texto.replace(espaco, "")
    return texto


def open_image(image_path: str) -> Image.Image:
    with Image.open(image_path) as image:
        image_in_memory = image.copy()
        return image_in_memory


def main() -> None:
    start = time.time()
    directory = ""
    pasta = os.path.join(directory, "PAPPDF", "PDFJaFeitos", "pasadeira Croche Candy")
    imagens = os.listdir()
    imagens = [os.path.join(pasta, arquivo) for arquivo in os.listdir(pasta)]
    for imagem in imagens:
        print("\n" + imagem)
        phrase = ocr.image_to_string(open_image(imagem), lang="por")
        phraseBonita = tiraEspaçoBranco(phrase)
        print(str(len(phrase)))
        print(str(len(phraseBonita)) + "\n")
        print(phraseBonita)
    final = time.time()
    print("demorou ")
    print_elapsed_time(final - start)


if __name__ == "__main__":
    main()