from typing import Literal, overload

from PIL import Image

RED = (255, 0, 0, 255)
BLUE = (0, 0, 255, 255)
BLACK = (0, 0, 0, 255)
COLORS = (RED, BLUE, BLACK)


@overload
def find_color(
    image: Image.Image, cor: tuple[int, ...], should_exclude: Literal[True]
) -> Image.Image: ...


@overload
def find_color(
    image: Image.Image, cor: tuple[int, ...], should_exclude: Literal[False] = False
) -> tuple[int, int]: ...


def find_color(
    image: Image.Image, cor: tuple[int, ...], should_exclude: bool = False
) -> Image.Image | tuple[int, int]:
    global BLACK
    width, height = image.size
    if should_exclude:
        for x in range(width):
            for y in range(height):
                if image.getpixel((x, y)) != cor:
                    continue
                image.putpixel((x, y), BLACK)
        return image
    for x in range(width):
        for y in range(height):
            if image.getpixel((x, y)) == cor:
                return (x, y)
    return (0, 0)


def captarSalvar(
    name: str, image: Image.Image
) -> tuple[tuple[int, int], tuple[int, int]]:
    global COLORS
    tamanho = image.size
    larg, alt = tamanho
    down = 0
    right = 0
    up = alt
    left = larg
    for x in range(larg):
        for y in range(alt):
            if image.getpixel((x, y)) in (COLORS):
                if y < up:
                    up = y
                if y > down:
                    down = y
                if x < left:
                    left = x
                if x > right:
                    right = x
    image = image.crop((left, up, right + 1, down + 1))
    image.save(name)
    return ((left, up), (right, down))


def open_image_as_rgba(image_path: str) -> Image.Image:
    with Image.open(image_path) as image:
        image_in_memory = image.copy()
        if image.mode != "RGBA":
            return image_in_memory.convert("RGBA")
        return image_in_memory


def main() -> None:
    newTamanho = 11
    meio = int(newTamanho / 2 + 1)
    curvaNova = Image.new("RGBA", (newTamanho, newTamanho))
    curvaNova.putpixel((meio, meio - 1), BLUE)
    curvaNova.putpixel((meio, meio), BLACK)
    curvaNova.putpixel((meio, meio + 1), RED)
    captarSalvar("curva0.png", curvaNova)
    for numeroCurva in range(0, 10):
        nome = f"curva{numeroCurva}.png"
        curvaAtual = open_image_as_rgba(nome)
        newTamanho = newTamanho * 2 - 1
        meio = int(newTamanho / 2 + 1)
        azulComprimento, azulAltura = find_color(curvaAtual, BLUE)
        print(f"{(azulAltura, azulComprimento)}")
        carimbo = curvaAtual.copy()
        carimbo = carimbo.convert("RGBA")
        curvaNova = Image.new("RGBA", (newTamanho, newTamanho))
        curvaNova.paste(carimbo, (meio, meio))
        carimboRotate = carimbo.rotate(90, expand=True)
        carimboRotate = carimboRotate.convert("RGBA")
        azulComprimentoRotate, azulAlturaRotate = find_color(carimboRotate, BLUE)
        print(f"{(azulComprimentoRotate, azulAlturaRotate)}")
        carimbo = find_color(carimbo, BLUE, should_exclude=True)
        carimboRotate = find_color(carimboRotate, BLUE, should_exclude=True)
        posicao = find_color(curvaNova, RED)
        curvaNova.paste(
            carimboRotate,
            (posicao[0] - azulComprimentoRotate, posicao[1] - azulAlturaRotate),
            carimboRotate,
        )
        curvaNova = find_color(curvaNova, RED, should_exclude=True)
        curvaNova.paste(
            carimbo, (posicao[0] - azulComprimento, posicao[1] - azulAltura), carimbo
        )
        posicao = find_color(curvaNova, RED)
        curvaNova = find_color(curvaNova, RED, should_exclude=True)
        curvaNova.paste(
            carimboRotate,
            (posicao[0] - azulComprimentoRotate, posicao[1] - azulAlturaRotate),
            carimboRotate,
        )
        captarSalvar(f"curva{numeroCurva + 1}.png", curvaNova)
        print(f"curva{numeroCurva + 1}.png")


if __name__ == "__main__":
    main()
