from typing import TypeVar, cast
from PIL import Image
from os import cpu_count
import multiprocessing

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


R = TypeVar("R", bound=tuple[int, ...])


def interpolate_tuples(tuple_source: R, tuple_target: R, frame_index: int) -> R:
    interpolated_values: list[int] = []
    for source_value, target_value in zip(tuple_source, tuple_target):
        difference = target_value - source_value
        interpolation_step = difference / FINAL_FRAME
        interpolated_value = int(interpolation_step * frame_index + source_value)
        interpolated_values.append(interpolated_value)
    return cast(R, tuple(interpolated_values))


def open_image_as_rgba(image_path: str) -> Image.Image:
    with Image.open(image_path) as image:
        image_in_memory = image.copy()
        if image.mode != "RGBA":
            return image_in_memory.convert("RGBA")
        return image_in_memory


def makeFrame(n: int) -> None:
    imagemInicial = open_image_as_rgba("./inicial.png")
    imagemFinal = open_image_as_rgba("./final.png")
    print(n)
    frame = Image.new("RGBA", imagemFinal.size, (255, 255, 255, 0))
    with open("./config.txt", "r", encoding="utf-8") as file:
        linha = file.readline()
        while linha:
            if linha.find("fundo") != -1:
                coord = (int(linha[:-6].split(",")[0]), int(linha[:-6].split(",")[1]))
                frame.putpixel(coord, get_pixel(imagemInicial, coord))
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
        frame.save(f"./frames/frame{n + 1:03d}.png")


def main() -> None:
    nomeFrame = "./frames/frame{0:03d}.png"
    imagemInicial = open_image_as_rgba("./inicial.png")
    imagemFinal = open_image_as_rgba("./final.png")
    imagemInicial.save(nomeFrame.format(0))
    imagemFinal.save(nomeFrame.format(FINAL_FRAME + 1))
    print("\n tamanho: " + str(imagemInicial.size), end="\n\n")
    with multiprocessing.Pool(cpu_count()) as cpu_pool:
        cpu_pool.map(makeFrame, range(FINAL_FRAME))


if __name__ == "__main__":
    main()
