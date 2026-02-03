import pastaImagens as pI
from time import time
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


def salva(nome, img):
    try:
        img.save(nome + ".png")
    except:
        img.save(nome + "1.png")


def procuraMaiorSize(imagens):
    largura = 0
    altura = 0
    for img in imagens:
        tamanho = Image.open(img).size
        if tamanho[0] >= largura:
            largura = tamanho[0]
        if tamanho[1] >= altura:
            altura = tamanho[1]
    tamanho = (largura, altura)
    return tamanho



def main() -> None:
    print("diga um assunto")
    assunto = input()
    imagens = pI.pegaAssunto(assunto)
    tamanho = procuraMaiorSize(imagens)
    largura, altura = tamanho
    print(tamanho)
    total = largura * altura
    print(total)
    novaImagem = Image.new("RGBA", tamanho, (0, 0, 0, 0))
    quantia = len(imagens)
    print("dê um nome a imagem média")
    nome = input()
    inicio = time()
    porcentagem = 0
    momento = 0
    ultimo = time()
    try:
        for y in range(altura):
            for x in range(largura):
                momento += 1
                novaCor = [0, 0, 0, 0]
                for img in imagens:
                    imageToUse = Image.new("RGBA", tamanho, (0, 0, 0, 0))
                    imagem = Image.open(img).convert("RGBA")
                    imageToUse.paste(imagem, (0, 0))
                    pixel = imageToUse.getpixel((x, y))
                    divisor = 0
                    if pixel[3] != 0:
                        divisor += 1
                        for index in range(4):
                            novaCor[index] += pixel[index]
                    if divisor == 0:
                        divisor = 1
                for index in range(4):
                    novaCor[index] = int(novaCor[index] / divisor)
                novaImagem.putpixel((x, y), tuple(novaCor))
                if int(momento * 100 / total) != porcentagem:
                    final = time()
                    porcentagem = int(momento * 100 / total)
                    salva(nome, novaImagem)
                    print(str(porcentagem) + "%")
                    print_elapsed_time(final - ultimo)
                    ultimo = final
    except:
        salva(nome, novaImagem)
    salva(nome, novaImagem)
    fim = time()
    print_elapsed_time(fim - inicio)


if __name__ == "__main__":
    main()