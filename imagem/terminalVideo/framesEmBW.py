from PIL import Image
import os

def imagemToText(imagem):
    global showAltura
    global niveis
    global showLargura
    imagemColor = Image.open(imagem)
    imagemBW = imagemColor.convert('L')
    largura,altura = imagemBW.size
    if(showAltura == 0):
        if (largura>showLargura):
            aspectRatio = showLargura/largura
            showAltura = int(altura*aspectRatio)
        else:
            showAltura = altura  
    imagemShow = imagemBW.resize((showLargura,showAltura))  
    largura,altura = imagemShow.size
    for y in range(altura):
        for x in range(largura):
            pixel = imagemShow.getpixel((x,y))
            imagemShow.putpixel((x,y),int(pixel/32)*32-1)
    imagemShow.save(imagem)
    
showAltura=0
niveis=[' ','`','.',',','+','%','@','#']
showLargura=80
diretorio='C:\\Users\\DELL\\Desktop\\antigo_PC\\pythonscript\\imagem\\terminalVideo\\video'
imagens=[os.path.join(diretorio,imagem)for imagem in os.listdir(diretorio)]
for imagem in imagens:
    imagemToText(imagem)
