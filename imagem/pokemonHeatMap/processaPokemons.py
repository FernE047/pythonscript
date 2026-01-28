import os
from PIL import Image
import shelve

diretorio = os.getcwd()
base = os.path.join(diretorio, "pokemon", "pokedexSemFundo")
imagens = os.listdir(base)
imagensCaminho = [os.path.join(base, imagem) for imagem in imagens]
imageNumber = 0
xHeat = []
yHeat = []
zHeat = []
for xIndex in range(96):
    for yIndex in range(96):
        xHeat.append(xIndex)
        yHeat.append(yIndex)
        zHeat.append(0)
for imagemCaminho in imagensCaminho:
    print(imagemCaminho)
    pokemon = Image.open(imagemCaminho)
    for y in range(96):
        for x in range(96):
            if pokemon.getpixel((x, y)) != (0, 0, 0, 0):
                zHeat[96 * x + y] += 1
BD = shelve.open(os.path.join(diretorio, "dadosPreProcessados"))
BD["x"] = xHeat
BD["y"] = yHeat
BD["z"] = zHeat
BD.close()
