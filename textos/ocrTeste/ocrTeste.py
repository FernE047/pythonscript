import pytesseract as ocr
import time
import textos
import os

from PIL import Image

start=time.time()
nome=os.path.join('jap','1.png')
print('\n'+nome)
imagem = Image.open(nome)
largura,altura = imagem.size()
#phrase = ocr.image_to_string(Image.open(nome), lang='jp')
#print(phrase)
#final=time.time()
#print("demorou "+textos.embelezeTempo(final-start))
