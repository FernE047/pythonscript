from PIL import Image
from time import time
import os
import subprocess

CoordData = tuple[int, int]


def get_pixel(image: Image.Image, coord: CoordData) -> tuple[int, ...]:
    pixel = image.getpixel(coord)
    if pixel is None:
        raise ValueError("Pixel not found")
    if isinstance(pixel, int):
        raise ValueError("Image is not in RGBA mode")
    if isinstance(pixel, float):
        raise ValueError("Image is not in RGBA mode")
    if len(pixel) < 4:
        raise ValueError("Image is not in RGBA mode")
    return pixel


def pegaInteiro(
    mensagem: str, minimo: int | None = None, maximo: int | None = None
) -> int:
    while True:
        entrada = input(f"{mensagem} : ")
        try:
            valor = int(entrada)
            if (minimo is not None) and (valor < minimo):
                print(f"valor deve ser maior ou igual a {minimo}")
                continue
            if (maximo is not None) and (valor > maximo):
                print(f"valor deve ser menor ou igual a {maximo}")
                continue
            return valor
        except Exception as _:
            print("valor inválido, tente novamente")


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


def funcaoAfim(inicio, fim, total, n):
    elemento = []
    for elementoInicial, elementoFinal in zip(inicio, fim):
        B = elementoInicial
        A = (elementoFinal - elementoInicial) / (total + 1)
        elemento.append(int(A * n + B))
    return tuple(elemento)


def main() -> None:
    nomeFrame = "frames/frame{0:03d}.png"
    quantiaFrames = 30  # pegaInteiro("quantos frames?")
    imagemInicial = Image.open("inicial.png")
    imagemFinal = Image.open("final.png")
    nomeFile = "partesConfig/parte{0:02d}Config.txt"
    imagemInicial.save(nomeFrame.format(0))
    imagemFinal.save(nomeFrame.format(quantiaFrames + 1))
    print("\n tamanho: " + str(imagemInicial.size), end="\n\n")
    partes = os.listdir("partesIniciais")
    quantiaPartes = len(partes)
    partes = None
    for a in range(quantiaFrames):
        frame = Image.new("RGBA", imagemFinal.size, (255, 255, 255, 0))
        frame.save(nomeFrame.format(a + 1))
    firstTime = True
    for nParte in range(quantiaPartes):
        for n in range(quantiaFrames):
            if firstTime:
                inicio = time()
            frame = Image.open(nomeFrame.format(n + 1))
            with open(nomeFile.format(nParte), "r", encoding="utf-8") as file:
                linha = file.readline()
                while linha:
                    if linha[0] in ["a", "v"]:
                        linha = file.readline()
                        continue
                    coords = [
                        tuple([int(b) for b in coord.split(",")])
                        for coord in linha.split(" ")
                    ]
                    coordFinal = coords[1]
                    pixelFinal = imagemFinal.getpixel(coordFinal)
                    coordInicial = coords[0]
                    pixelInicial = imagemInicial.getpixel(coordInicial)
                    novaCoord = funcaoAfim(
                        coordInicial, coordFinal, quantiaFrames, n + 1
                    )
                    novaCor = funcaoAfim(pixelInicial, pixelFinal, quantiaFrames, n + 1)
                    frame.putpixel(novaCoord, novaCor)
                    linha = file.readline()
                frame.save(nomeFrame.format(n + 1))
                frame.close()
                if firstTime:
                    fim = time()
                    duracao = fim - inicio
                    print("são " + str(quantiaFrames) + " frames")
                    print_elapsed_time(duracao)
                    print_elapsed_time(duracao * quantiaFrames)
                    fim, inicio, duracao, tamanhoFile = [None, None, None, None]
                    firstTime = False
        subprocess.call("python fazGif.py ")
    imagemInicial.close()
    imagemFinal.close()


if __name__ == "__main__":
    main()
