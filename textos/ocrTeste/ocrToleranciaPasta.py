from PIL import Image
import os
import pytesseract as ocr
import time
import textos

def applyTolerancia(img,tolerancia):
    imagem=Image.open(img)
    width,height=imagem.size
    imagemNew=imagem.copy()
    for x in range(width):
        for y in range(height):
            pixel=imagem.getpixel((x,y))
            teste=pixel[0]+pixel[1]+pixel[2]
            if(teste>=(255*3-tolerancia)):
                imagemNew.putpixel((x,y),(0,0,0))
            else:
                imagemNew.putpixel((x,y),(255,255,255))
    return(imagemNew)
    

start=time.time()
curso = open("passadeira Candy.txt", "w")
directory = ""
pasta=os.path.join(directory,'PAPPDF','PDFJaFeitos','pasadeira Croche Candy')
imagens=[os.path.join(pasta,arquivo) for arquivo in os.listdir(pasta)]
for imagem in imagens:
    print('\n'+imagem)
    startProcessing=time.time()
    phrase = ocr.image_to_string(applyTolerancia(imagem,20), lang='por')
    phraseBonita=textos.tiraEspacoBranco(phrase)
    endProcessing=time.time()
    print(str(len(phraseBonita)))
    print("procesamento: "+textos.embelezeTempo(endProcessing-startProcessing))
    print(phraseBonita)
    curso.write(phraseBonita+'\n\n')
final=time.time()
curso.close()
print("demorou "+textos.embelezeTempo(final-start))
