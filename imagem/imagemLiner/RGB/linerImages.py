from PIL import Image

def compara(pixelA,pixelB):
    soma = 0
    for a in range(3):
        soma += abs(pixelA[a]-pixelB[a])**2
    return soma**0.5
    

nomeOpen = 'A{0:03d}0.jpg'
nomeSave = 'A{0:03d}{1:01d}.png'
for a in range(1,2):
    imagem = Image.open(nomeOpen.format(a))
    altura,largura = imagem.size
    print('\nimagem '+nomeOpen.format(a)+' tamanho: '+str(imagem.size),end='\n\n')
    for b in range(1,6):
        imagemTransform = Image.new('RGBA',imagem.size,(255,255,255,255))
        for y in range(altura):
            for x in range(largura):
                pixelAtual = imagem.getpixel((y,x))
                arredores = []
                if(x>0):
                    arredores.append(imagem.getpixel((y,x-1)))
                if(x<largura-1):
                    arredores.append(imagem.getpixel((y,x+1)))
                if(y>0):
                    arredores.append(imagem.getpixel((y-1,x)))
                if(y<altura-1):
                    arredores.append(imagem.getpixel((y+1,x)))
                for pixel in arredores:
                    if(compara(pixel,pixelAtual)>10*b):
                        imagemTransform.putpixel((y,x),(0,0,0,255))
                pixelVelho = pixelAtual
        imagemTransform.save(nomeSave.format(a,b))
        imagemTransform.close()
        print('finalizado '+nomeSave.format(a,b))
    imagem.close()
