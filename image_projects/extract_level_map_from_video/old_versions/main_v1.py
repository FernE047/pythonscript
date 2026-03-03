from PIL import Image
from os import listdir
from time import time

# this code is legacy, I am only changing type hints and linter errors. it doesn't make sense to refactor it, since I already have a better version of it, and I don't want to break it by changing it too much

PY = 20  # PASSOSY             menor mais lento e melhor
PX = 60  # PASSOSX             menor mais lento e melhor
DDP = 15  # DISTANCIADEPROCURA maior mais lento e melhor
DT = DDP * 2 + 1  # DISTANCIATOTAL

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
    return open_image_as_rgba(frame).crop((40, 70, 1039, 479))


def comparaPixel(pixelA: tuple[int, ...], pixelB: tuple[int, ...]) -> float:
    total = 1.0
    for i in range(3):
        total *= 1 - abs(pixelA[i] - pixelB[i]) / 255
    return total


def comparaFrames(frameA: Image.Image, frameB: Image.Image) -> list[int]:
    tamanho = frameA.size
    aprovados = [[0.0 for _ in range(DT)] for _ in range(DT)]
    totais = [[0 for _ in range(DT)] for _ in range(DT)]
    for y in range(0, tamanho[1], DT):
        for x in range(0, tamanho[0], DT):
            pixelA = frameA.getpixel((x, y))
            if pixelA is None:
                continue
            if isinstance(pixelA, int) or isinstance(pixelA, float):
                continue
            if pixelA[2] == max(pixelA):
                continue
            for yAdd in range(-DDP, DDP + 1):
                for xAdd in range(-DDP, DDP + 1):
                    if x + xAdd < 0:
                        continue
                    if x + xAdd >= tamanho[0]:
                        break
                    if y + yAdd < 0:
                        continue
                    if y + yAdd >= tamanho[1]:
                        break
                    pixelB = frameB.getpixel((x + xAdd, y + yAdd))
                    if pixelB is None:
                        continue
                    if isinstance(pixelB, int) or isinstance(pixelB, float):
                        continue
                    if pixelB[2] == max(pixelB):
                        continue
                    aprovados[xAdd + DDP][yAdd + DDP] += comparaPixel(pixelA, pixelB)
                    totais[xAdd + DDP][yAdd + DDP] += 1
                if y + yAdd >= tamanho[1]:
                    break
    probabilidades = [
        [aprovados[x][y] / totais[x][y] for y in range(DT)] for x in range(DT)
    ]
    firstIndice = [max(probabilidades[x]) for x in range(DT)]
    maximo = max(firstIndice)
    teste = sum([probabilidades[x].count(maximo) for x in range(DT)])
    print(teste)
    indiceX = firstIndice.index(maximo)
    yAdd = probabilidades[indiceX].index(maximo) - DDP
    xAdd = indiceX - DDP
    return [-xAdd, -yAdd]


def ampliaMapa(mapa: Image.Image, ampliacao: Image.Image, posicao: list[int], adds: list[int]) -> tuple[Image.Image, list[int]]:
    tamanhoMapa = mapa.size
    tamanhoAmpliacao = ampliacao.size
    novaPosicao = [posicao[a] + adds[a] for a in range(2)]
    if min(novaPosicao) < 0:
        print("a")
        novoTamanho = list(tamanhoMapa).copy()
        for a in range(2):
            if novaPosicao[a] < 0:
                novoTamanho[a] = tamanhoMapa[a] - novaPosicao[a]
            else:
                novoTamanho[a] = novaPosicao[a] + tamanhoAmpliacao[a]
        novo_tamanho_tuple = tuple(novoTamanho)
        assert len(novo_tamanho_tuple) == 2, "novoTamanho must have exactly 2 elements"
        novoMapa = Image.new("RGBA", novo_tamanho_tuple, (255, 255, 255, 0))
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
        assert len(novissimaPosicao_tuple) == 2, "novissimaPosicao must have exactly 2 elements"
        novaPosicao_tuple = tuple(novaPosicao)
        assert len(novaPosicao_tuple) == 2, "novaPosicao must have exactly 2 elements"
        novoMapa.paste(mapa, novissimaPosicao_tuple)
        novoMapa.paste(ampliacao, novaPosicao_tuple)
    else:
        novaPosicao_tuple = (novaPosicao[0], novaPosicao[1])
        teste = [
            novaPosicao[a] + tamanhoAmpliacao[a] > tamanhoMapa[a] for a in range(2)
        ]
        if True in teste:
            print("b")
            novoTamanho = list(tamanhoMapa).copy()
            for a in range(2):
                if teste[a]:
                    novoTamanho[a] = novaPosicao[a] + tamanhoAmpliacao[a]
            novo_tamanho_tuple = tuple(novoTamanho)
            assert len(novo_tamanho_tuple) == 2, "novoTamanho must have exactly 2 elements"
            novoMapa = Image.new("RGBA", novo_tamanho_tuple, (255, 255, 255, 0))
        else:
            print("c")
            novoMapa = mapa
        novoMapa.paste(mapa, (0, 0))
        novoMapa.paste(ampliacao, novaPosicao_tuple)
    return novoMapa, novaPosicao


def main() -> None:

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

    ultimoFrame = openFrame(diretorioFrames.format(1))
    mapa = openFrame(diretorioFrames.format(1))
    posicao = [0, 0]
    framesTotais = len(listdir(diretorioVideo))
    inicio = time()
    inicioTotal = time()
    for n in range(150, framesTotais):
        frameAtual = openFrame(diretorioFrames.format(n))
        adds = comparaFrames(ultimoFrame, frameAtual)
        mapa, posicao = ampliaMapa(mapa, frameAtual, posicao, adds)
        ultimoFrame, _ = ampliaMapa(ultimoFrame, frameAtual, [0, 0], adds)
        ultimoFrame.save(f"results/frame{n:04d}.png")
        ultimoFrame = frameAtual
        fim = time()
        duracao = fim - inicio
        inicio = time()
        print()
        print(f"{n} : ")
        print_elapsed_time(duracao)
        print_elapsed_time(duracao * (framesTotais - n))
        mapa.save("mapa.png")
    mapa.save("mapa.png")
    mapa.save("mapa.png")
    fimTotal = time()
    duracao = fimTotal - inicioTotal
    print_elapsed_time(duracao)


if __name__ == "__main__":
    main()
