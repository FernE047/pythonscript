from PIL import Image
from os import listdir
from time import time

# this code is legacy, I am only changing type hints and linter errors. it doesn't make sense to refactor it, since I already have a better version of it, and I don't want to break it by changing it too much
ddp = 20  # DISTANCIADEPROCURA  maior = mais lento e melhor
dt = ddp * 2 + 1  # DISTANCIATOTAL
py = dt  # PASSOSY             menor = mais lento e melhor, tem que ser maior que DT
px = dt  # PASSOSX             menor = mais lento e melhor, tem que ser maior que DT
inicio = 0.0


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


def open_image_as_rgba(image_path: str) -> Image.Image:
    with Image.open(image_path) as image:
        image_in_memory = image.copy()
        if image.mode != "RGBA":
            return image_in_memory.convert("RGBA")
        return image_in_memory


def openFrame(frame: str) -> Image.Image:
    return open_image_as_rgba(frame).crop((42, 78, 1039, 479))


def comparaPixel(pixelA: tuple[int, ...], pixelB: tuple[int, ...]) -> float:
    total = 1.0
    for i in range(3):
        total *= 1 - abs(pixelA[i] - pixelB[i]) / 255
    return total


def encontraIndice(aprovados: list[list[float]], totais: list[list[int]]) -> list[int]:
    maxValue = 0.0
    maxIndice = [ddp, ddp]
    for x in range(dt):
        for y in range(dt):
            value = aprovados[x][y] / totais[x][y]
            if value >= maxValue:
                maxValue = value
                maxIndice = [x, y]
    return [ddp - a for a in maxIndice]


def comparaFrames(
    mapa: Image.Image, frameB: Image.Image, posicao: list[int]
) -> list[int]:
    global inicio
    global ddp, dt, py, px
    inicio = time()
    tamanho = frameB.size
    aprovados = [[0.0 for _ in range(dt)] for _ in range(dt)]
    totais = [[0 for _ in range(dt)] for _ in range(dt)]
    for y in range(0, tamanho[1], py):
        for x in range(0, tamanho[0], px):
            pixelA = mapa.getpixel((posicao[0] + x, posicao[1] + y))
            if pixelA is None:
                continue
            if isinstance(pixelA, int) or isinstance(pixelA, float):
                continue
            if pixelA[2] == max(pixelA):
                continue
            for yAdd in range(-ddp, ddp + 1):
                if y + yAdd < 0:
                    continue
                if y + yAdd >= tamanho[1]:
                    break
                for xAdd in range(-ddp, ddp + 1):
                    if x + xAdd < 0:
                        continue
                    if x + xAdd >= tamanho[0]:
                        break
                    pixelB = frameB.getpixel((x + xAdd, y + yAdd))
                    if pixelB is None:
                        continue
                    if isinstance(pixelB, int) or isinstance(pixelB, float):
                        continue
                    if pixelB[2] == max(pixelB):
                        continue
                    aprovados[xAdd + ddp][yAdd + ddp] += comparaPixel(
                        pixelA, pixelB
                    )
                    totais[xAdd + ddp][yAdd + ddp] += 1
    inicio = time()
    indice = encontraIndice(aprovados, totais)
    return indice


def ampliaMapa(
    mapa: Image.Image, ampliacao: Image.Image, posicao: list[int], adds: list[int]
) -> tuple[Image.Image, list[int]]:
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
        novoTamanho_tuple = tuple(novoTamanho)
        assert len(novoTamanho_tuple) == 2
        novoMapa = Image.new("RGBA", novoTamanho_tuple, (255, 255, 255, 0))
        for a in range(2):
            if novaPosicao[a] < 0:
                novaPosicao[a] = 0
        novissimaPosicao = novaPosicao.copy()
        for a in range(2):
            if novissimaPosicao[a] > 0:
                novissimaPosicao[a] = 0
            else:
                novissimaPosicao[a] -= adds[a]
        novissimaPosicao_tuple = tuple(novissimaPosicao)
        assert len(novissimaPosicao_tuple) == 2
        novoMapa.paste(mapa, novissimaPosicao_tuple)
        ampliacaoTransparent = Image.new("RGBA", novoMapa.size, (255, 255, 255, 0))
        novaPosicao_tuple = tuple(novaPosicao)
        assert len(novaPosicao_tuple) == 2
        ampliacaoTransparent.paste(ampliacao, novaPosicao_tuple)
        novoMapa = Image.alpha_composite(ampliacaoTransparent, novoMapa)
        # novoMapa.paste(ampliacao,tuple(novaPosicao))
    else:
        novoTamanho = list(tamanhoMapa).copy()
        for a in range(2):
            if novaPosicao[a] + tamanhoAmpliacao[a] > tamanhoMapa[a]:
                novoTamanho[a] = novaPosicao[a] + tamanhoAmpliacao[a]
        novoTamanho_tuple = tuple(novoTamanho)
        assert len(novoTamanho_tuple) == 2
        novoMapa = Image.new("RGBA", novoTamanho_tuple, (255, 255, 255, 0))
        novoMapa.paste(mapa, (0, 0))
        ampliacaoTransparent = Image.new("RGBA", novoMapa.size, (255, 255, 255, 0))
        novaPosicao_tuple = tuple(novaPosicao)
        assert len(novaPosicao_tuple) == 2
        ampliacaoTransparent.paste(ampliacao, novaPosicao_tuple)
        novoMapa = Image.alpha_composite(ampliacaoTransparent, novoMapa)
        # novoMapa.paste(ampliacao,novaPosicao)
    return novoMapa, novaPosicao


def main() -> None:
    global inicio
    global ddp, dt, py, px

    # Argumentos do FFMPEG
    diretorioVideo = "./video"
    origemVideo = "-i ./level.mp4"
    destinoTemp = f"{diretorioVideo}/frame%04d.png"
    extraArguments = "-r {0:02d}/1"
    processoArgs = ["ffmpeg", origemVideo, extraArguments, destinoTemp]

    fps = 30

    processoArgs[2] = extraArguments.format(fps)
    # subprocess.call (" ".join(processoArgs))

    diretorioFrames = f"{diretorioVideo}/frame{{0:04d}}.png"

    mapa = openFrame(diretorioFrames.format(1))
    posicao = [0, 0]
    framesTotais = len(listdir(diretorioVideo))
    inicio = time()
    inicioTotal = time()
    n = 0
    try:
        for n in range(90, framesTotais):
            frameAtual = openFrame(diretorioFrames.format(n))
            adds = comparaFrames(mapa, frameAtual, posicao)
            while max([abs(a) for a in adds]) == ddp:
                ddp = max([abs(a) for a in adds]) + 1
                dt = ddp * 2 + 1
                py = dt
                px = dt
                print(f"ddp: {ddp}, dt: {dt}, py: {py}, px: {px}")
                adds = comparaFrames(mapa, frameAtual, posicao)
            mapa, posicao = ampliaMapa(mapa, frameAtual, posicao, adds)
            fim = time()
            duracao = fim - inicio
            inicio = time()
            print()
            print(f"{n} : ")
            print_elapsed_time(duracao)
            print_elapsed_time(duracao * (framesTotais - n))
            print(adds)
    except Exception as e:
        print(n)
        print("deu erro")
        print(e)
        pass
    fimTotal = time()
    duracao = fimTotal - inicioTotal
    print_elapsed_time(duracao)
    mapa.save("mapa.png")


if __name__ == "__main__":
    main()
