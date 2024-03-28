import pypdn
from PIL import Image
import os

def limpaPasta(pasta):
    arquivos = [pasta+'\\'+a for a in os.listdir(pasta)]
    if('C:\\pythonscript\\imagem\\morphManual\\frames\\resized' in arquivos):
        arquivos.pop(arquivos.index('C:\\pythonscript\\imagem\\morphManual\\frames\\resized'))
    for arquivo in arquivos:
        os.remove(arquivo)

def salvaLayers(nome,pasta):
    fundo = False
    layeredImage = pypdn.read('C:\\pythonscript\\imagem\\morphManual\\' + nome)
    new_im = Image.fromarray(layeredImage.layers[0].image)
    new_im.save('C:\\pythonscript\\imagem\\morphManual\\' + nome[:-4]+".png")
    new_im.close()
    for n in range(1,len(layeredImage.layers)):
        new_im = Image.fromarray(layeredImage.layers[n].image)
        new_im.save(pasta + "\\{0:03d}".format(n-1) + ".png")
        new_im.close()

limpaPasta('C:\\pythonscript\\imagem\\morphManual\\partes\\iniciais')
limpaPasta('C:\\pythonscript\\imagem\\morphManual\\partes\\finais')
limpaPasta('C:\\pythonscript\\imagem\\morphManual\\partes\\config')
limpaPasta('C:\\pythonscript\\imagem\\morphManual\\debug')
limpaPasta('C:\\pythonscript\\imagem\\morphManual\\frames')
limpaPasta('C:\\pythonscript\\imagem\\morphManual\\frames\\resized')
salvaLayers('inicial.pdn','C:\\pythonscript\\imagem\\morphManual\\partes\\iniciais')
salvaLayers('final.pdn','C:\\pythonscript\\imagem\\morphManual\\partes\\finais')
