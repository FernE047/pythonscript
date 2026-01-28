import os
from PIL import Image
import random

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
    pokemon = Image.open(imagemCaminho)
    for y in range(96):
        for x in range(96):
            cor = pokemon.getpixel((x, y))
            if cor != (0, 0, 0, 0):
                heatMap.putpixel((x, y), cor)
heatMap.save(os.path.join(diretorio, "paçocaRandom02.png"))
