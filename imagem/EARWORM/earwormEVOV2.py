from userUtil import cadaMusicaFaca
from PIL import Image
import os
        
def fazImagem(info):
    titulo,musica = info
    musicaSeparada = musica.split(" ")
    quantPalavras=len(musicaSeparada)
    print("quantidade de palavras: "+str(quantPalavras)+"\n")
    if(quantPalavras):
        imagem = Image.new('RGBA',(quantPalavras,quantPalavras),(0,0,0,255))
        for coordX in range(quantPalavras):
            for coordY in range(quantPalavras):
                if(musicaSeparada[coordX] == musicaSeparada[coordY]):
                    imagem.putpixel((coordX,coordY),(255,0,0,255))
        return(imagem)

cadaMusicaFaca(fazImagem)
