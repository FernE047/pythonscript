from PIL import Image
from morpher import funcaoCor
from corrigeFrames import fixTrappedPixels
import os

def makeBackground(nome):
    print("back iniciado")
    imagem = Image.open("C:\\pythonscript\\imagem\\morphManual\\" + nome + ".png")
    if nome == "inicial":
        directory = "C:\\pythonscript\\imagem\\morphManual\\partes\\iniciais"
    else:
        directory = "C:\\pythonscript\\imagem\\morphManual\\partes\\finais"
    for partsName in [directory + "\\" + fileName for fileName in os.listdir(directory)]:
        parte = Image.open(partsName)
        largura, altura = parte.size
        firstOcorrence = True
        for x in range(largura):
            alterations = 0
            for y in range(altura):
                if parte.getpixel((x,y))[3] == 255:
                    imagem.putpixel((x,y),(255,255,255,0))
                    alterations += 1
            if firstOcorrence and (alterations > 0):
                firstOcorrence = False
            if not firstOcorrence and (alterations == 0):
                break
    fixTrappedPixels(imagem,[])
    imagem.save("C:\\pythonscript\\imagem\\morphManual\\background" + nome + ".png")
    print("back terminado")
    return imagem

if __name__ == "__main__":
    backInicial = makeBackground("inicial")#Image.open("C:\\pythonscript\\imagem\\morphManual\\backgroundinicial.png")#
    backFinal = makeBackground("final")#Image.open("C:\\pythonscript\\imagem\\morphManual\\backgroundfinal.png")#
    frames = ["C:\\pythonscript\\imagem\\morphManual\\frames\\"+a for a in os.listdir("C:\\pythonscript\\imagem\\morphManual\\frames")]
    frames.pop(0)
    frames.pop(-1)
    frames.pop(-1)
    total = len(frames)
    for n,frameName in enumerate(frames):
        frame = Image.open(frameName)
        largura, altura = backInicial.size
        for x in range(largura):
            for y in range(altura):
                if frame.getpixel((x,y))[3] == 0:
                    inicio = backInicial.getpixel((x,y))
                    final = backFinal.getpixel((x,y))
                    frame.putpixel((x,y),funcaoCor(inicio,final,total,n))
        print(n)
        frame.save(frameName)
        frame.close()