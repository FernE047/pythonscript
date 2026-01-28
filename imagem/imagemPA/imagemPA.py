from PIL import Image
from userUtil import pegaImagem as pImg
from userUtil import pegaInteiro as pInt

def processaImagemPorImagem(imagemInicial,imagemFinal,frames):
    tamanho=imagemInicial.size
    largura,altura=tamanho
    for frame in range(frames):
        imagem=Image.new('RGBA',tamanho,(255,255,255,255))
        for x in range(largura):
            for y in range(altura):
                coord=(x,y)
                pixelInicial=imagemInicial.getpixel(coord)
                pixelFinal=imagemFinal.getpixel(coord)
                cor=[]
                for index in range(4):
                    cor.append(int(pixelInicial[index]+((frame+1)*(pixelFinal[index]-pixelInicial[index]))/(frames+1)))
                cor=tuple(cor)
                imagem.putpixel(coord,cor)
        imagem.save(f'output{frame+1:02d}.png')

def processaPixelPorPixel(imagemInicial,imagemFinal,frames):
    pass

imagemInicial = pImg(texto='\ndigite o assunto da primeira imagem',infoAdicional=1)
imagemFinal = pImg(texto='\ndigite o assunto da última imagem',infoAdicional=1)
frames = pInt('\ndigite a quantidade de frames do meio')
larg1,alt1=imagemInicial.size
larg2,alt2=imagemFinal.size
tamanho1=larg1*alt1
tamanho2=larg2*alt2
if(tamanho1>tamanho2):
    imagemInicial=imagemInicial.resize((larg2,alt2))
else:
    imagemFinal=imagemFinal.resize((larg1,alt1))
imagemInicial.save(f'output{0:02d}.png')
imagemFinal.save(f'output{frames+1:02d}.png')
processaImagemPorImagem(imagemInicial,imagemFinal,frames)
