from typing import TypeVar, cast
from PIL import Image
import imageio
#imageio doesn't have type hints, so all type ignore on this file is from imageio
from time import time

CoordData = tuple[int, int]

FINAL_FRAME = 30


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
    print(f"{sign}{', '.join(parts)}")


R = TypeVar("R", bound=tuple[int, ...])


def interpolate_tuples(tuple_source: R, tuple_target: R, frame_index: int) -> R:
    interpolated_values: list[int] = []
    for source_value, target_value in zip(tuple_source, tuple_target):
        difference = target_value - source_value
        interpolation_step = difference / FINAL_FRAME
        interpolated_value = int(interpolation_step * frame_index + source_value)
        interpolated_values.append(interpolated_value)
    return cast(R, tuple(interpolated_values))


def verificaTamanho() -> int:
    with open("config.txt", "r", encoding="utf-8") as file:
        linha = file.readline()
        quantia = 0
        while linha:
            quantia += 1
            linha = file.readline()
    return quantia


def open_image_as_rgba(image_path: str) -> Image.Image:
    with Image.open(image_path) as image:
        image_in_memory = image.copy()
        if image.mode != "RGBA":
            return image_in_memory.convert("RGBA")
        return image_in_memory


def main() -> None:
    inicio = time()
    nomeFrame = "pokemon002{0:02d}.png"
    quantiaFrames = FINAL_FRAME
    imagemInicial = open_image_as_rgba("pokemon000.png")
    imagemFinal = open_image_as_rgba("pokemon001.png")
    imagemInicial.save(nomeFrame.format(0))
    imagemFinal.save(nomeFrame.format(quantiaFrames + 1))
    print(f"\n tamanho: {imagemInicial.size}", end="\n\n")
    for a in range(quantiaFrames):
        frame = Image.new("RGBA", imagemFinal.size, (255, 255, 255, 0))
        frame.save(nomeFrame.format(a + 1))
    tamanhoFile = verificaTamanho()
    with open("config.txt", "r", encoding="utf-8") as file:
        linha = file.readline()
        firstTime = True
        inicioDef = time()
        while linha:
            if firstTime:
                inicio = time()
            coords = [
                (int(coord.split(",")[0]), int(coord.split(",")[1]))
                for coord in linha.split(" ")
            ]
            coordFinal = coords[1]
            pixelFinal = get_pixel(imagemFinal, coordFinal)
            coordInicial = coords[0]
            pixelInicial = get_pixel(imagemInicial, coordInicial)
            for n in range(quantiaFrames):
                frame = open_image_as_rgba(nomeFrame.format(n + 1))
                novaCoord = interpolate_tuples(coordInicial, coordFinal, n + 1)
                novaCor = interpolate_tuples(pixelInicial, pixelFinal, n + 1)
                frame.putpixel(novaCoord, novaCor)
                frame.save(nomeFrame.format(n + 1))
            linha = file.readline()
            if firstTime:
                fim = time()
                duracao = fim - inicio
                print(f"são {tamanhoFile} transformações")
                print_elapsed_time(duracao)
                print_elapsed_time(duracao * tamanhoFile)
                firstTime = False
    with imageio.get_writer("bulbasaurEvolve.gif", mode="I") as writer:  # type: ignore
        for n in range(quantiaFrames):
            imagem = imageio.imread(nomeFrame.format(n))  # type: ignore
            writer.append_data(imagem)  # type: ignore
    fimDef = time()
    print("\nfinalizado")
    print_elapsed_time(fimDef - inicioDef)


if __name__ == "__main__":
    main()
