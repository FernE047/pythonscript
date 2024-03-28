import os
from PIL import Image

diretorio=os.getcwd()
base=os.path.join(diretorio,'pokemon','pokedexFeijao')
imagens=os.listdir(base)
imagensCaminho=[os.path.join(base,imagem)for imagem in imagens]
imageNumber=0
for imagemCaminho in imagensCaminho:
    print(imagemCaminho)
    pokemon=Image.open(imagemCaminho)
    largura,altura=pokemon.size
    corTransparente=pokemon.getpixel((0,0))
    for y in range(96):
        for x in range(96):
            if(pokemon.getpixel((x,y))==corTransparente):
                pokemon.putpixel((x,y),(0,0,0,0))
    pokemon.save(os.path.join(diretorio,'pokemon','pokedexSemFundo','pokemon{0:03d}.png'.format(imageNumber)))
    imageNumber+=1
