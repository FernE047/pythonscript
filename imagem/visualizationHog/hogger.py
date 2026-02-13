from colorsys import rgb_to_hsv
from colorsys import hsv_to_rgb
import os
from PIL import Image


def open_image_as_rgba(image_path: str) -> Image.Image:
    with Image.open(image_path) as image:
        image_in_memory = image.copy()
        if image.mode != "RGBA":
            return image_in_memory.convert("RGBA")
        return image_in_memory


def count_images_on_folder(image_category: str) -> int:
    folder = f"imagens/{image_category}"
    quantity = 0
    if os.path.exists(folder):
        for filename in os.listdir(folder):
            if filename.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif")):
                quantity += 1
    return quantity


def get_image(image_category: str, index_chosen: int = 1) -> str:
    folder = f"imagens/{image_category}"
    if os.path.exists(folder):
        index = 0
        for filename in os.listdir(folder):
            if filename.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif")):
                index += 1
                if index == index_chosen:
                    return os.path.join(folder, filename)
    return ""


def coordDirecao(coord, n):
    if n > 7:
        n = n % 8
    x, y = coord
    if n == 0:
        return (x + 1, y + 1)
    if n == 1:
        return (x, y + 1)
    if n == 2:
        return (x - 1, y + 1)
    if n == 3:
        return (x - 1, y)
    if n == 4:
        return (x - 1, y - 1)
    if n == 5:
        return (x, y - 1)
    if n == 6:
        return (x + 1, y - 1)
    if n == 7:
        return (x + 1, y)
    return (x, y)


def makeBlackAndWhite(imagem):
    largura, altura = imagem.size
    for x in range(largura):
        for y in range(altura):
            coord = (x, y)
            pixel = imagem.getpixel(coord)
            if pixel[3] == 0:
                imagem.putpixel(coord, (0, 0, 0, 0))
                continue
            pixel = tuple(3 * [int(sum(pixel[:3]) / 3)] + [255])
            imagem.putpixel(coord, pixel)


def discoverDirectionPixel(inicial, coord):
    lista = [inicial.getpixel(coordDirecao(coord, direction)) for direction in range(8)]
    pesoDirection = []
    for n in range(8):
        peso = [a[0] for a in [lista[(n - 1) % 8]] + [lista[n]] + [lista[(n + 1) % 8]]]
        pesoDirection.append(sum(peso))
    diferenca = [abs(pesoDirection[n] - pesoDirection[(n + 4) % 8]) for n in range(4)]
    maiorDiferenca = max(diferenca)
    quantia = 0
    maioresDiferencas = []
    for n in range(4):
        if diferenca[n] == maiorDiferenca:
            maioresDiferencas.append(n)
    """if(coord == (54,49)):
        print(diferenca)
        print(pesoDirection)
        print(maiorDiferenca)
        print(maioresDiferencas)"""
    if len(maioresDiferencas) == 1:
        direction = maioresDiferencas[0]
        if pesoDirection[direction] > pesoDirection[(direction + 4) % 8]:
            return direction
        else:
            return (direction + 4) % 8
    else:
        return 8


def hogify(inicial, final):
    largura, altura = imagem.size
    for c in range(8):
        cor = hsv_to_rgb(c * 0.125, 1, 255)
        cor = tuple([int(a) for a in cor])
        final.putpixel((c, 0), cor)
    for x in range(1, largura - 1):
        for y in range(1, altura - 1):
            coord = (x, y)
            direction = discoverDirectionPixel(inicial, coord)
            if direction == 8:
                cor = (0, 0, 0, 255)
            else:
                cor = hsv_to_rgb(direction * 0.125, 1, 255)
                cor = tuple([int(a) for a in cor])
            final.putpixel(coord, cor)


totalDeImagens = count_images_on_folder("PokedexSemFundo")
nome = "output//pokemon{0:03d}.png"
imagem = open_image_as_rgba(get_image("PokedexSemFundo", 1))
imagemHog = Image.new("RGBA", imagem.size, tuple(4 * [0]))
makeBlackAndWhite(imagem)
hogify(imagem, imagemHog)
imagem.save(nome.format(1))
imagemHog.save(nome.format(0))
