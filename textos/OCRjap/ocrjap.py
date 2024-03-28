import pytesseract as ocr
import time
import textos
import os

from PIL import Image

def descobre(nome):
    imagem = Image.open(nome)
    larg,alt = imagem.size
    for x in range(larg):
        for y in range(alt):
            pixel=imagem.getpixel((x,y))
            if(pixel==(100,191,96)):
                print((x,y))

start=time.time()
nome=os.path.join('jap','1.png')
print('\n'+nome)
imagem = Image.open(nome)
imagemCut = imagem.crop((34,909,671,1072))
imagemCut.save('cut.png')
#phrase = ocr.image_to_string(imagemCut, lang='jp')
#print(phrase)
final=time.time()
print("demorou "+textos.embelezeTempo(final-start))
