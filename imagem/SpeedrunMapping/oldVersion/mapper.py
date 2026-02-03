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
    return Image.open(frame).crop((40,70,1039,479))

def comparaPixel(pixelA,pixelB):
    total = 1
    for i in range(3):
        total *= 1-abs(pixelA[i]-pixelB[i])/255
    return total

def comparaFrames(frameA,frameB):
    tamanho = frameA.size
    aprovados = [[0 for a in range(DT)] for b in range(DT)]
    totais = [[0 for a in range(DT)] for b in range(DT)]
    for y in range(0,tamanho[1],DT):
        for x in range(0,tamanho[0],DT):
            pixelA = frameA.getpixel((x,y))
            if pixelA[2] == max(pixelA):
                continue
            for yAdd in range(-DDP,DDP+1):
                for xAdd in range(-DDP,DDP+1):
                    if x+xAdd < 0:
                        continue
                    if x+xAdd >= tamanho[0]:
                        break
                    if y+yAdd < 0:
                        continue
                    if y+yAdd >= tamanho[1]:
                        break
                    pixelB = frameB.getpixel((x+xAdd,y+yAdd))
                    if pixelB[2] == max(pixelB):
                        continue
                    aprovados[xAdd+DDP][yAdd+DDP] += comparaPixel(pixelA,pixelB)
                    totais[xAdd+DDP][yAdd+DDP] += 1
                if y+yAdd >= tamanho[1]:
                    break
    probabilidades = [[aprovados[x][y]/totais[x][y] for y in range(DT)] for x in range(DT)]
    firstIndice = [max(probabilidades[x]) for x in range(DT)]
    maximo = max(firstIndice)
    teste = sum([probabilidades[x].count(maximo) for x in range(DT)])
    print(teste)
    indiceX = firstIndice.index(maximo)
    yAdd = probabilidades[indiceX].index(maximo)-DDP
    xAdd = indiceX - DDP
    return [-xAdd,-yAdd]

def ampliaMapa(mapa,ampliacao,posicao,adds):
    tamanhoMapa = mapa.size
    tamanhoAmpliacao = ampliacao.size
    novaPosicao = [posicao[a]+adds[a] for a in range(2)]
    if min(novaPosicao) < 0:
        print("a")
        novoTamanho = list(tamanhoMapa).copy()
        for a in range(2):
            if novaPosicao[a] < 0:
                novoTamanho[a] = tamanhoMapa[a] - novaPosicao[a]
            else:
                novoTamanho[a] = novaPosicao[a] + tamanhoAmpliacao[a]
        novoMapa = Image.new("RGBA",tuple(novoTamanho),(255,255,255,0))
        for a in range(2):
            if novaPosicao[a] < 0:
                novaPosicao[a] = 0
        novissimaPosicao = novaPosicao.copy()
        for a in range(2):
            if novissimaPosicao[a] > 0:
                novissimaPosicao[a] = 0
            else:
                novissimaPosicao[a] -= adds[a]
        novoMapa.paste(mapa,tuple(novissimaPosicao))
        novoMapa.paste(ampliacao,tuple(novaPosicao))
    else:
        teste = [novaPosicao[a] + tamanhoAmpliacao[a] > tamanhoMapa[a] for a in range(2)]
        if True in teste:
            print("b")
            novoTamanho = list(tamanhoMapa).copy()
            for a in range(2):
                if teste[a]:
                    novoTamanho[a] = novaPosicao[a] + tamanhoAmpliacao[a]
            novoMapa = Image.new("RGBA",tuple(novoTamanho),(255,255,255,0))
        else:
            print("c")
            novoMapa = mapa
        novoMapa.paste(mapa,(0,0))
        novoMapa.paste(ampliacao,novaPosicao)
    return novoMapa,novaPosicao



def main() -> None:
    PY = 20 #PASSOSY             menor mais lento e melhor
    PX = 60 #PASSOSX             menor mais lento e melhor
    DDP = 15 #DISTANCIADEPROCURA maior mais lento e melhor
    DT = DDP*2+1 #DISTANCIATOTAL

    #Argumentos do FFMPEG
    diretorioVideo = "C:\\pythonscript\\imagem\\SpeedrunMapping\\video"
    origemVideo = "-i C:\pythonscript\\imagem\\SpeedrunMapping\\level.mp4"#"-i C:\\pythonscript\\videos\\videos\\video0002.mp4"
    destinoTemp = diretorioVideo + "\\frame%04d.png"
    extraArguments = "-r {0:02d}/1"
    processoArgs = ["ffmpeg",origemVideo,extraArguments,destinoTemp]

    fps = 30

    processoArgs[2] = extraArguments.format(fps)
    #subprocess.call (" ".join(processoArgs))

    diretorioFrames = diretorioVideo+"\\frame{0:04d}.png"

    ultimoFrame = openFrame(diretorioFrames.format(1))
    mapa = openFrame(diretorioFrames.format(1))
    posicao = [0,0]
    framesTotais = len(listdir(diretorioVideo))
    inicio = time()
    inicioTotal = time()
    for n in range(150,framesTotais):
        frameAtual = openFrame(diretorioFrames.format(n))
        adds = comparaFrames(ultimoFrame,frameAtual)
        mapa,posicao = ampliaMapa(mapa,frameAtual,posicao,adds)
        ultimoFrame,_ = ampliaMapa(ultimoFrame,frameAtual,[0,0],adds)
        ultimoFrame.save(f"results\\frame{n:04d}.png")
        ultimoFrame.close()
        ultimoFrame = frameAtual
        fim = time()
        duracao = fim-inicio
        inicio = time()
        print()
        print(f"{n} : ")
        print_elapsed_time(duracao)
        print_elapsed_time(duracao*(framesTotais-n))
        mapa.save("mapa.png")
    mapa.save("mapa.png")
    frameAtual.close()
    ultimoFrame.close()
    mapa.save("mapa.png")
    fimTotal = time()
    duracao = fimTotal-inicioTotal
    print_elapsed_time(duracao)


if __name__ == "__main__":
    main()