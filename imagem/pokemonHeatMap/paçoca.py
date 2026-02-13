import os
from PIL import Image
import random


def open_image_as_rgba(image_path: str) -> Image.Image:
    with Image.open(image_path) as image:
        image_in_memory = image.copy()
        if image.mode != "RGBA":
            return image_in_memory.convert("RGBA")
        return image_in_memory


def main() -> None:
    diretorio = os.getcwd()
    base = os.path.join(diretorio, "pokemon", "pokedexSemFundo")
    imagens = os.listdir(base)
    imagensCaminho = [os.path.join(base, imagem) for imagem in imagens]
    imageNumber = 0
    heatMap = Image.new("RGBA", (96, 96), (0, 255, 255, 255))
    random.shuffle(imagensCaminho)
    for imagemCaminho in imagensCaminho:
        print(imageNumber, end=",")
        imageNumber += 1
        pokemon = open_image_as_rgba(imagemCaminho)
        for y in range(96):
            for x in range(96):
                cor = pokemon.getpixel((x, y))
                if cor != (0, 0, 0, 0):
                    heatMap.putpixel((x, y), cor)
    heatMap.save(os.path.join(diretorio, "paçocaRandom02.png"))


if __name__ == "__main__":
    main()
