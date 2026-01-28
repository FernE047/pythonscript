import pytesseract as ocr
import numpy as np
import cv2
import time
import textos
import os
import pastaImagens as pI

from PIL import Image

def melhora(img):
    imagem = Image.open(img).convert('RGB')
    npimagem = np.asarray(imagem).astype(np.uint8)
    npimagem[:, :, 0] = 0 
    npimagem[:, :, 2] = 0
    im = cv2.cvtColor(npimagem, cv2.COLOR_RGB2GRAY) 
    ret, thresh = cv2.threshold(im, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    binimagem = Image.fromarray(thresh)
    return(binimagem)


def tiraEspaçoBranco(texto: str) -> str:
    for espaco in [" ", "\n", "\t"]:
        if espaco in texto:
            texto = texto.replace(espaco, "")
    return texto


start=time.time()
print('digite um assunto')
assunto=input()
print('quantas imagens ler?')
leitura=input()
try:
    leitura=int(leitura)
    imagens=pI.pegaAssunto(assunto,leitura)
except:
    imagens=pI.pegaAssunto(assunto)
for imagem in imagens:
    print('\n'+imagem)
    imagem=melhora(imagem)
    phrase = ocr.image_to_string(imagem, lang='eng')
    phraseBonita=tiraEspaçoBranco(phrase)
    print(str(len(phraseBonita))+'\n')
    print(phraseBonita)
final=time.time()
print("demorou "+textos.embelezeTempo(final-start))
