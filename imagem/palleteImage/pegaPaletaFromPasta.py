from PIL import Image
import os
from pastaImagens import pegaAssunto as pA


def main() -> None:
    imagens=pA("pokedex sem fundo")
    paleta=[]
    for img in imagens:
        imagem=Image.open(img)
        largura,altura=imagem.size
        for x in range(largura):
            for y in range(altura):
                pixel=imagem.getpixel((x,y))
                if(pixel not in paleta):
                    paleta.append(pixel)
    altura=int(len(paleta)/256)+1
    if(altura>1):
        paletaImg=Image.new("RGBA",(256,altura),(0,0,0,0))
    else:
        paletaImg=Image.new("RGBA",(len(paleta),altura),(0,0,0,0))
    m=0
    for index in range(len(paleta)):
        if(m%256==0):
            m=0
        paletaImg.putpixel((m,int(index/256)),paleta[index])
        m+=1
    paletaImg.save(os.path.join("paleta","paletaPokemons.png"))


if __name__ == "__main__":
    main()