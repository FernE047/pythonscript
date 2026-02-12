import subprocess
from PIL import Image
from os import listdir
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


def openFrame(frame):
    return Image.open(frame).crop((42, 78, 1039, 479))


def comparaPixel(pixelA, pixelB):
    total = 1
    for i in range(3):
        total *= 1 - abs(pixelA[i] - pixelB[i]) / 255
    return total


def comparaFrames(mapa, frameB, posicao):
    inicio = time()
    tamanho = frameB.size
    aprovados = [[0 for a in range(DT)] for b in range(DT)]
    totais = [[0 for a in range(DT)] for b in range(DT)]
    maiorValue = 0
    maiorIndice = [DDP, DDP]
    for yAdd in range(-DDP, DDP + 1):
        for xAdd in range(-DDP, DDP + 1):
            aprovados = 0
            total = 0
            for y in range(0, tamanho[1], PY):
                if y + yAdd < 0:
                    continue
                if y + yAdd >= tamanho[1]:
                    break
                for x in range(0, tamanho[0], PX):
                    if x + xAdd < 0:
                        continue
                    if x + xAdd >= tamanho[0]:
                        break
                    pixelA = mapa.getpixel((posicao[0] + x, posicao[1] + y))
                    if pixelA[2] == max(pixelA[:-1]):
                        continue
                    pixelB = frameB.getpixel((x + xAdd, y + yAdd))
                    if pixelB[2] == max(pixelB[:-1]):
                        continue
                    aprovados += comparaPixel(pixelA, pixelB)
                    total += 1
            if total != 0:
                value = aprovados / total
            else:
                value = 0
            if value > maiorValue:
                maiorValue = value
                maiorIndice = [-xAdd, -yAdd]
    fim = time()
    duracao = fim - inicio
    return maiorIndice


def ampliaMapa(mapa, ampliacao, posicao, adds):
    tamanhoMapa = mapa.size
    tamanhoAmpliacao = ampliacao.size
    novaPosicao = [posicao[a] + adds[a] for a in range(2)]
    if min(novaPosicao) < 0:
        novoTamanho = list(tamanhoMapa).copy()
        for a in range(2):
            if novaPosicao[a] < 0:
                novoTamanho[a] = tamanhoMapa[a] - novaPosicao[a]
            else:
                novoTamanho[a] = novaPosicao[a] + tamanhoAmpliacao[a]
        novoMapa = Image.new("RGBA", tuple(novoTamanho), (255, 255, 255, 0))
        for a in range(2):
            if novaPosicao[a] < 0:
                novaPosicao[a] = 0
        novissimaPosicao = novaPosicao.copy()
        for a in range(2):
            if novissimaPosicao[a] > 0:
                novissimaPosicao[a] = 0
            else:
                novissimaPosicao[a] -= adds[a]
        novoMapa.paste(mapa, tuple(novissimaPosicao))
        ampliacaoTransparent = Image.new("RGBA", novoMapa.size, (255, 255, 255, 0))
        ampliacaoTransparent.paste(ampliacao, tuple(novaPosicao))
        novoMapa = Image.alpha_composite(ampliacaoTransparent, novoMapa)
        # novoMapa.paste(ampliacao,tuple(novaPosicao))
    else:
        novoTamanho = list(tamanhoMapa).copy()
        for a in range(2):
            if novaPosicao[a] + tamanhoAmpliacao[a] > tamanhoMapa[a]:
                novoTamanho[a] = novaPosicao[a] + tamanhoAmpliacao[a]
        novoMapa = Image.new("RGBA", tuple(novoTamanho), (255, 255, 255, 0))
        novoMapa.paste(mapa, (0, 0))
        ampliacaoTransparent = Image.new("RGBA", novoMapa.size, (255, 255, 255, 0))
        ampliacaoTransparent.paste(ampliacao, tuple(novaPosicao))
        novoMapa = Image.alpha_composite(ampliacaoTransparent, novoMapa)
        # novoMapa.paste(ampliacao,novaPosicao)
    return novoMapa, novaPosicao



def main() -> None:
    DDP = 20  # DISTANCIADEPROCURA  maior = mais lento e melhor
    DT = DDP * 2 + 1  # DISTANCIATOTAL
    PY = DT  # PASSOSY             menor = mais lento e melhor, tem que ser maior que DT
    PX = DT  # PASSOSX             menor = mais lento e melhor, tem que ser maior que DT

    # Argumentos do FFMPEG
    diretorioVideo = "./video"
    origemVideo = "-i ./level.mp4"
    destinoTemp = diretorioVideo + "/frame%04d.png"
    extraArguments = "-r {0:02d}/1"
    processoArgs = ["ffmpeg", origemVideo, extraArguments, destinoTemp]

    fps = 30

    processoArgs[2] = extraArguments.format(fps)
    # subprocess.call (" ".join(processoArgs))

    diretorioFrames = diretorioVideo + "/frame{0:04d}.png"

    mapa = openFrame(diretorioFrames.format(1))
    tamanho = mapa.size
    posicao = [0, 0]
    framesTotais = len(listdir(diretorioVideo))
    inicioTotal = time()
    inicio = time()
    try:
        for n in range(90, framesTotais):
            frameAtual = openFrame(diretorioFrames.format(n))
            adds = comparaFrames(mapa, frameAtual, posicao)
            while max([abs(a) for a in adds]) == DDP:
                print("a")
                DDP = max([abs(a) for a in adds]) + 1
                DT = DDP * 2 + 1
                PY = DT
                PX = DT
                adds = comparaFrames(mapa, frameAtual, posicao)
            mapa, posicao = ampliaMapa(mapa, frameAtual, posicao, adds)
            fim = time()
            duracao = fim - inicio
            inicio = time()
            mapa.save("mapa.png")
            print()
            print(f"{n} : ")
            print_elapsed_time(duracao)
            print_elapsed_time(duracao * (framesTotais - n))
            print(adds)
    except:
        print(n)
        print("deu erro")
        pass
    frameAtual.close()
    fimTotal = time()
    duracao = fimTotal - inicioTotal
    print_elapsed_time(duracao)
    mapa.save("mapa.png")
    mapa.close()


if __name__ == "__main__":
    main()