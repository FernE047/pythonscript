import pypdn
from PIL import Image
import os

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


def limpaPasta(pasta):
    arquivos = [pasta + "/" + a for a in os.listdir(pasta)]
    if "./frames/resized" in arquivos:
        arquivos.pop(arquivos.index("./frames/resized"))
    for arquivo in arquivos:
        os.remove(arquivo)


def salvaLayers(nome, pasta):
    fundo = False
    layeredImage = pypdn.read(nome)
    new_im = Image.fromarray(layeredImage.layers[0].image)
    new_im.save(nome[:-4] + ".png")
    new_im.close()
    for n in range(1, len(layeredImage.layers)):
        new_im = Image.fromarray(layeredImage.layers[n].image)
        largura, altura = new_im.size
        for x in range(largura):
            for y in range(altura):
                pixel = new_im.getpixel((x, y))
                if pixel[3] == 0:
                    pixel = new_im.putpixel((x, y), (0, 0, 0, 0))
        if n == 1:
            if new_im.getpixel((0, 0)) == (255, 255, 255, 255):
                fundo = True
                new_im.save(pasta + "/fundo.png")
                continue
        if fundo:
            n -= 1
        new_im.save(f"{pasta}/parte{n - 1:02d}{nome[:-4]}.png")
        new_im.close()


def main() -> None:
    limpaPasta("./partes/partesIniciais")
    limpaPasta("./partes/partesFinais")
    limpaPasta("./partes/partesConfig")
    limpaPasta("./frames")
    limpaPasta("./frames/resized")
    salvaLayers("inicial.pdn", "partesIniciais")
    salvaLayers("final.pdn", "partesFinais")


if __name__ == "__main__":
    main()
