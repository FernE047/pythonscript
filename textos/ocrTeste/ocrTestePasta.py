import pytesseract as ocr
import time
import textos
import os

from PIL import Image


def tiraEspaçoBranco(texto: str) -> str:
    for espaco in [" ", "\n", "\t"]:
        if espaco in texto:
            texto = texto.replace(espaco, "")
    return texto


start=time.time()
directory = ""
pasta=os.path.join(directory,'PAPPDF','PDFJaFeitos','pasadeira Croche Candy')
imagens=os.listdir()
imagens=[os.path.join(pasta,arquivo) for arquivo in os.listdir(pasta)]
for imagem in imagens:
    print('\n'+imagem)
    phrase = ocr.image_to_string(Image.open(imagem), lang='por')
    phraseBonita=tiraEspaçoBranco(phrase)
    print(str(len(phrase)))
    print(str(len(phraseBonita))+'\n')
    print(phraseBonita)
final=time.time()
print("demorou "+textos.embelezeTempo(final-start))
