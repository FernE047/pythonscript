from send2trash import send2trash
from os import listdir
from PIL import Image
from os import remove
from time import time
import subprocess


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


def openFrame(frame):
    return Image.open(frame)  # .crop((42,78,1039,479))


def comparaPixel(pixelA, pixelB):
    total = 1
    for i in range(3):
        total *= 1 - abs(pixelA[i] - pixelB[i]) / 255
    return total


def encontraIndice(aprovados, totais):
    maxValue = 0
    maxIndice = [DDP, DDP]
    for x in range(DT):
        for y in range(DT):
            value = aprovados[x][y] / totais[x][y]
            if value >= maxValue:
                maxValue = value
                maxIndice = [x - DDP, y - DDP]
    return maxIndice


def comparaFrames(mapa, frameB, posicao):
    aprovados = [[0 for a in range(DT)] for b in range(DT)]
    totais = [[0 for a in range(DT)] for b in range(DT)]
    for y in range(0, frameB.size[1], PY):
        for x in range(0, frameB.size[0], PX):
            pixelA = frameB.getpixel((x, y))
            if pixelA[2] == max(pixelA):
                continue
            for yAdd in range(-DDP, DDP + 1):
                if posicao[1] + y + yAdd < 0:
                    continue
                if posicao[1] + y + yAdd >= mapa.size[1]:
                    break
                for xAdd in range(-DDP, DDP + 1):
                    if posicao[0] + x + xAdd < 0:
                        continue
                    if posicao[0] + x + xAdd >= mapa.size[0]:
                        break
                    pixelB = mapa.getpixel(
                        (posicao[0] + x + xAdd, posicao[1] + y + yAdd)
                    )
                    if pixelB[2] != max(pixelB):
                        aprovados[xAdd + DDP][yAdd + DDP] += comparaPixel(
                            pixelA, pixelB
                        )
                        totais[xAdd + DDP][yAdd + DDP] += 1
    indice = encontraIndice(aprovados, totais)
    return indice


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
    return novoMapa, novaPosicao


# Constantes e Variaveis Importantes

inicioTotal = time()
DDP = 20  # DISTANCIADEPROCURA  maior = mais lento e melhor
DT = DDP * 2 + 1  # DISTANCIATOTAL
PY = DT  # PASSOSY             menor = mais lento e melhor, tem que ser maior que DT
PX = DT  # PASSOSX             menor = mais lento e melhor, tem que ser maior que DT

# Argumentos do FFMPEG

diretorioVideo = "C:\\pythonscript\\imagem\\SpeedrunMapping\\video"
origemVideo = "-i C:\pythonscript\\imagem\\SpeedrunMapping\\level.mp4"  # "-i C:\\pythonscript\\videos\\videos\\video0002.mp4"
destinoTemp = diretorioVideo + "\\frame%02d.png"
extraArguments = "-r {0:02d}/1 -ss {1:02d}:{2:02d}:{3:02d}.0 -t 1.03"
processoArgs = ["ffmpeg", origemVideo, extraArguments, destinoTemp]
fps = 10

# duracao arredondada em minutos do video
segundos = 27
minutos = 1
horas = 0

# iniciadores
processoArgs[2] = extraArguments.format(fps, 0, 0, 0)
subprocess.call(" ".join(processoArgs))
diretorioFrames = diretorioVideo + "\\"
mapa = openFrame(diretorioFrames + listdir(diretorioVideo)[0])
tamanho = mapa.size
posicao = [0, 0]
inicio = time()
try:
    for hora in range(horas + 1):
        if hora == horas:
            limiteMinutos = minutos + 1
        else:
            limiteMinutos = 60
        for minuto in range(limiteMinutos):
            if minuto == minutos:
                limiteSegundos = segundos + 1
            else:
                limiteSegundos = 60
            for segundo in range(limiteSegundos):
                processoArgs[2] = extraArguments.format(fps, hora, minuto, segundo)
                subprocess.call(" ".join(processoArgs))
                for n, frame in enumerate(listdir(diretorioVideo)):
                    frameAtual = openFrame(diretorioFrames + frame)
                    adds = comparaFrames(mapa, frameAtual, posicao)
                    while max([abs(a) for a in adds]) == DDP:
                        DDP = max([abs(a) for a in adds]) + 1
                        DT = DDP * 2 + 1
                        PY = DT
                        PX = DT
                        print("novo DDP : " + str(DDP))
                        adds = comparaFrames(mapa, frameAtual, posicao)
                    mapa, posicao = ampliaMapa(mapa, frameAtual, posicao, adds)
                    remove(diretorioFrames + frame)
                    # send2trash(diretorioFrames + frame)
                    print(f"{hora:02d}:{minuto:02d}:{segundo:02d}.{n:02d}")
                fim = time()
                duracao = fim - inicio
                inicio = time()
                mapa.save("mapa.png")
                print(
                    embelezeTempo(
                        duracao
                        * (
                            horas * 3600
                            + minutos * 60
                            + segundos
                            - hora * 3600
                            - minuto * 60
                            - segundo
                        )
                    )
                )
except:
    print(posicao)
    print(f"{hora:02d}:{minuto:02d}:{segundo:02d}.{n:02d}")
frameAtual.close()
fimTotal = time()
duracao = fimTotal - inicioTotal
print(embelezeTempo(duracao))
mapa.save("mapa.png")
mapa.close()
