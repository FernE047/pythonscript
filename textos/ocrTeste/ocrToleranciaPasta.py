from PIL import Image
import os
import pytesseract as ocr
import time


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


def tiraEspaçoBranco(texto: str) -> str:
    for espaco in [" ", "\n", "\t"]:
        if espaco in texto:
            texto = texto.replace(espaco, "")
    return texto


def open_image_as_rgb(image_path: str) -> Image.Image:
    with Image.open(image_path) as image:
        image_in_memory = image.copy()
        if image.mode != "RGB":
            return image_in_memory.convert("RGB")
        return image_in_memory


def applyTolerancia(img, tolerancia):
    imagem = open_image_as_rgb(img)
    width, height = imagem.size
    imagemNew = imagem.copy()
    for x in range(width):
        for y in range(height):
            pixel = imagem.getpixel((x, y))
            teste = pixel[0] + pixel[1] + pixel[2]
            if teste >= (255 * 3 - tolerancia):
                imagemNew.putpixel((x, y), (0, 0, 0))
            else:
                imagemNew.putpixel((x, y), (255, 255, 255))
    return imagemNew



def main() -> None:
    start = time.time()
    with open("passadeira Candy.txt", "w", encoding="utf-8") as curso:
        directory = ""
        pasta = os.path.join(directory, "PAPPDF", "PDFJaFeitos", "pasadeira Croche Candy")
        imagens = [os.path.join(pasta, arquivo) for arquivo in os.listdir(pasta)]
        for imagem in imagens:
            print(f"\n{imagem}")
            startProcessing = time.time()
            phrase = ocr.image_to_string(applyTolerancia(imagem, 20), lang="por")
            phraseBonita = tiraEspaçoBranco(phrase)
            endProcessing = time.time()
            print(f"{len(phraseBonita)}")
            print("procesamento: ")
            print_elapsed_time(endProcessing - startProcessing)
            print(phraseBonita)
            curso.write(f"{phraseBonita}\n\n")
        final = time.time()
    print("demorou ")
    print_elapsed_time(final - start)


if __name__ == "__main__":
    main()