from PIL import Image
import os
import math
import numpy

BACKGROUND_COLOR = (255, 255, 255)

CoordData = tuple[int, int]
ColorData = tuple[int, int, int, int]


def save_image(image: Image.Image, path: str) -> None:
    try:
        image.save(path)
    except PermissionError:
        image_name, extension = os.path.splitext(path)
        index_attempt = 0
        while True:
            try:
                image.save(f"{image_name}_{index_attempt}.{extension}")
                break
            except PermissionError:
                index_attempt += 1


def get_pixel(imagem: Image.Image, coord: tuple[int, int]) -> tuple[int, ...]:
    pixel = imagem.getpixel(coord)
    if pixel is None:
        return BACKGROUND_COLOR
    if not isinstance(pixel, tuple):
        pixel_int = int(pixel)
        return (pixel_int, pixel_int, pixel_int)
    return pixel


def coordenadasPregos(nail_count: int, img: Image.Image) -> list[CoordData]:
    largura, altura = img.size
    hip = int(math.sqrt((largura / 2) ** 2 + (altura / 2) ** 2)) + 1
    print(hip)
    pregosAngulo = 360 / nail_count
    pregos: list[CoordData] = []
    for angulo in numpy.arange(0, 360, pregosAngulo):
        radiano = angulo * math.pi / 180
        pregos.append(
            (int(hip * math.cos(radiano)) + hip, int(hip * math.sin(radiano) + hip))
        )
    return pregos


def dimensoesPorPregos(pregos: list[CoordData]) -> tuple[int, int]:
    maiorX = 0
    maiorY = 0
    for prego in pregos:
        if prego[0] >= maiorX:
            maiorX = prego[0]
        if prego[1] >= maiorY:
            maiorY = prego[1]
    tamanho = (maiorX + 2, maiorY + 2)
    return tamanho


def ehMaior(
    pregoProximo: CoordData,
    pregoAtual: CoordData,
    menorValor: float,
    imagemPregos: Image.Image,
) -> tuple[float, bool]:
    menorValorOriginal = menorValor
    totalValor = 0.0
    totalLinha = 0
    if pregoAtual == pregoProximo:
        return (menorValor, False)
    auxB = 0.0
    if pregoAtual[0] != pregoProximo[0]:
        auxA = (pregoAtual[1] - pregoProximo[1]) / (pregoAtual[0] - pregoProximo[0])
        auxB = pregoProximo[1] - pregoProximo[0] * auxA
    else:
        auxA = 2.0
    if (auxA <= 1) and (auxA >= -1):
        if pregoAtual[0] > pregoProximo[0]:
            flow = -1
        else:
            flow = 1
        for x in range(pregoAtual[0], pregoProximo[0], flow):
            pixel = get_pixel(imagemPregos, (x, int(auxA * x + auxB)))
            if pixel[3] == 255:
                valor = 0
                valor += pixel[0]
                valor += pixel[1]
                valor += pixel[2]
                totalValor += valor / (3 * 255)
                totalLinha += 1
        if totalLinha == 0:
            totalLinha = 1
        if (totalValor / totalLinha) <= menorValor:
            menorValor = totalValor / totalLinha
    else:
        auxA = (pregoAtual[0] - pregoProximo[0]) / (pregoAtual[1] - pregoProximo[1])
        auxB = pregoProximo[0] - pregoProximo[1] * auxA
        if pregoAtual[1] > pregoProximo[1]:
            flow = -1
        else:
            flow = 1
        for y in range(pregoAtual[1], pregoProximo[1], flow):
            pixel = get_pixel(imagemPregos, (int(auxA * y + auxB), y))
            if pixel[3] == 255:
                valor = 0
                valor += pixel[0]
                valor += pixel[1]
                valor += pixel[2]
                totalValor += valor / (3 * 255)
                totalLinha += 1
        if totalLinha == 0:
            totalLinha = 1
        if (totalValor / totalLinha) <= menorValor:
            menorValor = totalValor / totalLinha
    return (menorValor, (menorValor != menorValorOriginal))


def draw_line(
    initial_coordinate: CoordData,
    final_coordinate: CoordData,
    image: Image.Image,
    color: ColorData,
) -> Image.Image:
    slope = 2.0
    line_offset = 0.0
    start_x, start_y = initial_coordinate
    final_x, final_y = final_coordinate
    if start_x != final_x:
        slope = (start_y - final_y) / (start_x - final_x)
        line_offset = final_y - final_x * slope
    if (slope <= 1) and (slope >= -1):
        flow = -1 if start_x > final_x else 1
        for x in range(start_x, final_x, flow):
            y = int(slope * x + line_offset)
            image.putpixel((x, y), color)
        return image
    slope = (start_x - final_x) / (start_y - final_y)
    line_offset = final_x - final_y * slope
    flow = -1 if start_y > final_y else 1
    for y in range(start_y, final_y, flow):
        x = int(slope * y + line_offset)
        image.putpixel((x, y), color)
    return image


def main() -> None:
    quantiaPregos = 400
    imagemPasta = os.path.join("C:\\", "pythonscript", "lineImage", "imagens")
    imagens = [os.path.join(imagemPasta, imagem) for imagem in os.listdir(imagemPasta)]
    imagem = Image.open(imagens[5])
    pregos = coordenadasPregos(quantiaPregos, imagem)
    largura, altura = imagem.size
    larguraFinal, alturaFinal = dimensoesPorPregos(pregos)
    imagemFinal = Image.new("RGBA", (larguraFinal, alturaFinal), (255, 255, 255, 255))
    imagemPregos = imagemFinal.copy()
    offset = ((larguraFinal - largura) // 2, (alturaFinal - altura) // 2)
    imagemPregos.paste(imagem, offset)
    pregoAtual = pregos[0]
    imagemExemplo = imagemPregos.copy()
    for prego in pregos:
        imagemExemplo.putpixel(prego, (255, 0, 0, 255))
    imagemExemplo.save(os.path.join(imagemPasta, "valCroche400Exemplo.png"))
    while True:
        menorPrego = pregos[0]
        menorValor = 1.0
        for prego in pregos:
            menorValor, alterou = ehMaior(prego, pregoAtual, menorValor, imagemPregos)
            if alterou:
                menorPrego = prego
        if menorValor != 1.0:
            print(
                "do prego "
                + str(pregos.index(pregoAtual))
                + " para o prego "
                + str(pregos.index(menorPrego))
            )
            imagemPregos = draw_line(
                pregoAtual, menorPrego, imagemPregos, (255, 255, 255, 255)
            )
            imagemFinal = draw_line(pregoAtual, menorPrego, imagemFinal, (0, 0, 0, 255))
            pregoAtual = menorPrego
        else:
            break
        save_image(imagemFinal, os.path.join(imagemPasta, "out.png"))
    save_image(imagemFinal, os.path.join(imagemPasta, "final.png"))


if __name__ == "__main__":
    main()
