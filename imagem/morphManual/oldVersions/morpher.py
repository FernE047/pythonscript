from typing import TypeVar, cast
from PIL import Image

FINAL_FRAME = 30

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


R = TypeVar("R", bound=tuple[int, ...])


def interpolate_tuples(tuple_source: R, tuple_target: R, frame_index: int) -> R:
    interpolated_values: list[int] = []
    for source_value, target_value in zip(tuple_source, tuple_target):
        difference = target_value - source_value
        interpolation_step = difference / FINAL_FRAME
        interpolated_value = int(interpolation_step * frame_index + source_value)
        interpolated_values.append(interpolated_value)
    return cast(R, tuple(interpolated_values))


def main() -> None:
    nomeFrame = "frames/frame{0:03d}.png"
    quantiaFrames = 3  # pegaInteiro("quantos frames?")
    imagemInicial = Image.open("inicial.png")
    imagemFinal = Image.open("final.png")
    imagemInicial.save(nomeFrame.format(0))
    imagemFinal.save(nomeFrame.format(quantiaFrames + 1))
    print("\n tamanho: " + str(imagemInicial.size), end="\n\n")
    for n in range(quantiaFrames):
        print(n)
        frame = Image.new("RGBA", imagemFinal.size, (255, 255, 255, 0))
        with open("config.txt", "r", encoding="utf-8") as file:
            linha = file.readline()
            while linha:
                if linha.find("fundo") != -1:
                    pass
                    # coord = tuple([int(b) for b in linha[:-6].split(",")])
                    # frame.putpixel(coord,imagemInicial.getpixel(coord))
                else:
                    coords = [
                        (int(coord.split(",")[0]), int(coord.split(",")[1]))
                        for coord in linha.split(" ")
                    ]
                    coordFinal = coords[1]
                    pixelFinal = get_pixel(imagemFinal, coordFinal)
                    coordInicial = coords[0]
                    pixelInicial = get_pixel(imagemInicial, coordInicial)
                    novaCoord = interpolate_tuples(coordInicial, coordFinal, n + 1)
                    novaCor = interpolate_tuples(pixelInicial, pixelFinal, n + 1)
                    frame.putpixel(novaCoord, novaCor)
                linha = file.readline()
            frame.save(nomeFrame.format(n + 1))
            frame.close()
    imagemInicial.close()
    imagemFinal.close()


if __name__ == "__main__":
    main()
