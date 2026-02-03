import shelve
from PIL import Image
from userUtil import pegaImagem as pI
from random import randint
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


def procuraBranco(imagem, quantia):
    largura, altura = imagem.size
    total = 0
    for x in range(largura):
        for y in range(altura):
            coord = (x, y)
            pixel = imagem.getpixel(coord)
            if pixel == (255, 255, 255, 255):
                total += 1
            if total == quantia:
                return coord
    return coord


def randomTotal(imagem):
    largura, altura = imagem.size
    shuffledImage = Image.new("RGBA", (largura, altura), (255, 255, 255, 255))
    for x in range(largura):
        for y in range(altura):
            coord = (x, y)
            pixelOriginal = imagem.getpixel(coord)
            newX = randint(0, largura - 1)
            newY = randint(0, altura - 1)
            newCoord = (newX, newY)
            pixel = shuffledImage.getpixel(newCoord)
            while pixel != (255, 255, 255, 255):
                newX = randint(0, largura - 1)
                newY = randint(0, altura - 1)
                newCoord = (newX, newY)
                pixel = shuffledImage.getpixel(newCoord)
            newCoord = (newX, newY)
            shuffledImage.putpixel(newCoord, pixelOriginal)
    return shuffledImage


def brancosTotal(imagem):
    largura, altura = imagem.size
    totalBranco = largura * altura
    shuffledImage = Image.new("RGBA", (largura, altura), (255, 255, 255, 255))
    for x in range(largura):
        for y in range(altura):
            coord = (x, y)
            pixelOriginal = imagem.getpixel(coord)
            posicao = randint(1, totalBranco)
            newCoord = procuraBranco(shuffledImage, posicao)
            totalBranco -= 1
            shuffledImage.putpixel(newCoord, pixelOriginal)
    return shuffledImage


def meioAMeio(imagem, porcentagemRandom):
    largura, altura = imagem.size
    total = largura * altura
    totalRandom = 0
    totalBranco = total
    porcentagem = totalRandom / total
    shuffledImage = Image.new("RGBA", (largura, altura), (255, 255, 255, 255))
    for x in range(largura):
        for y in range(altura):
            coord = (x, y)
            pixelOriginal = imagem.getpixel(coord)
            if porcentagem < porcentagemRandom:
                newX = randint(0, largura - 1)
                newY = randint(0, altura - 1)
                newCoord = (newX, newY)
                pixel = shuffledImage.getpixel(newCoord)
                while pixel != (255, 255, 255, 255):
                    newX = randint(0, largura - 1)
                    newY = randint(0, altura - 1)
                    newCoord = (newX, newY)
                    pixel = shuffledImage.getpixel(newCoord)
                newCoord = (newX, newY)
                totalRandom += 1
                totalBranco -= 1
                porcentagem = totalRandom / total
            else:
                posicao = randint(1, totalBranco)
                newCoord = procuraBranco(shuffledImage, posicao)
                totalBranco -= 1
            shuffledImage.putpixel(newCoord, pixelOriginal)
    return shuffledImage



def main() -> None:
    imagem = pI(infoAdicional=1)
    tempos = []
    for porc in range(100, -1, -1):
        BD = shelve.open("BDRandom")
        inicio = time()
        shuffledImage = meioAMeio(imagem, porc)
        fim = time()
        tempo = fim - inicio
        print(f"porcentagem de aleatoridade:{porc}%\n")
        print_elapsed_time(tempo)
        print()
        shuffledImage.save(f"output{porc:03d}.png")
        tempos.append(tempo)
        BD[f"tempos{porc:03d}"] = tempos
        BD.close()
    temposOrdenados = sorted(tempos)
    print("Resultados : ")
    for tempo in temposOrdenados:
        print(f"{tempos.index(tempo)}% : {tempo}")


if __name__ == "__main__":
    main()