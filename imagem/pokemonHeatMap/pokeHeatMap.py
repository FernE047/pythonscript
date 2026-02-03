import os
from PIL import Image


def main() -> None:
    diretorio = os.getcwd()
    base = os.path.join(diretorio, "pokemon", "pokedexSemFundo")
    imagens = os.listdir(base)
    imagensCaminho = [os.path.join(base, imagem) for imagem in imagens]
    imageNumber = 0
    heatMap = Image.new("RGBA", (96, 96), (0, 255, 255, 255))
    for imagemCaminho in imagensCaminho:
        print(imagemCaminho)
        pokemon = Image.open(imagemCaminho)
        for y in range(96):
            for x in range(96):
                if pokemon.getpixel((x, y)) != (0, 0, 0, 0):
                    cor = heatMap.getpixel((x, y))
                    if cor[2] > 0:
                        heatMap.putpixel((x, y), (0, 255, cor[2] - 1, 255))
                    elif cor[0] < 255:
                        heatMap.putpixel((x, y), (cor[0] + 1, 255, 0, 255))
                    elif cor[1] > 0:
                        heatMap.putpixel((x, y), (255, cor[1] - 1, 0, 255))
    heatMap.save(os.path.join(diretorio, "heatMap.png"))


if __name__ == "__main__":
    main()