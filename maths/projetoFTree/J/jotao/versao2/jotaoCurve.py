from PIL import Image

vermelho=(255,0,0,255)
azul=(0,0,255,255)
preto=(0,0,0,255)
cores=(vermelho,azul,preto)
fracaoPerfeita=64/32

def acharCor(img,cor,excluir=False):
    global preto
    tamanho=img.size
    larg,alt=tamanho
    if(excluir):
        for x in range(larg):
            for y in range(alt):
                if(img.getpixel((x,y))==cor):
                    img.putpixel((x,y),(0,0,0,255))
        return(img)
    else:
        for x in range(larg):
            for y in range(alt):
                if(img.getpixel((x,y))==cor):
                   return((x,y))
    return(0)
               
def captarSalvar(nome,img):
    global cores
    tamanho=img.size
    larg,alt=tamanho
    down=0
    right=0
    up=alt
    left=larg
    for x in range(larg):
        for y in range(alt):
            if(img.getpixel((x,y))in(cores)):
                if(y<up):
                    up=y
                if(y>down):
                    down=y
                if(x<left):
                    left=x
                if(x>right):
                    right=x
    img=img.crop((left, up, right+1, down+1))
    print(str(img.size))
    img.save(nome)
    return(((left,up),(right,down)))

newTamanho=5
meio=int(newTamanho/2+1)
curvaNova=Image.new('RGBA',(newTamanho,newTamanho))
curvaNova.putpixel((meio,meio-1),azul)
curvaNova.putpixel((meio,meio),preto)
curvaNova.putpixel((meio,meio+1),vermelho)
captarSalvar('curva0.png',curvaNova)
for numeroCurva in range(0,15):
    nome='curva'+str(numeroCurva)+'.png'
    curvaAtual=Image.open(nome)
    larg,alt=curvaAtual.size
    newTamanho=int(newTamanho*fracaoPerfeita)
    meio=int(newTamanho/2+1)
    carimbo=curvaAtual.copy()
    carimbo=carimbo.convert('RGBA')
    curvaNova=Image.new('RGBA', (newTamanho,newTamanho))
    print(str(newTamanho))
    curvaNova.paste(carimbo, (meio,meio))
    ultimaPos=acharCor(curvaNova,azul)
    carimboRotate=carimbo.rotate(90, expand=True)
    carimboRotate2=carimbo.rotate(180, expand=True)
    carimboRotate3=carimbo.rotate(270, expand=True)
    carimboRotate=carimboRotate.convert('RGBA')
    carimboRotate2=carimboRotate2.convert('RGBA')
    carimboRotate3=carimboRotate3.convert('RGBA')
    azulComprimento,azulAltura=acharCor(carimbo,azul)
    azulComprimentoRotate,azulAlturaRotate=acharCor(carimboRotate,azul)
    azulComprimentoRotate2,azulAlturaRotate2=acharCor(carimboRotate2,azul)
    azulComprimentoRotate3,azulAlturaRotate3=acharCor(carimboRotate3,azul)
    carimbo=acharCor(carimbo,azul,excluir=True)
    carimboRotate=acharCor(carimboRotate,azul,excluir=True)
    carimboRotate2=acharCor(carimboRotate2,azul,excluir=True)
    carimboRotate3=acharCor(carimboRotate3,azul,excluir=True)
    posicao=acharCor(curvaNova,vermelho)
    curvaNova.paste(carimboRotate, (posicao[0]-azulComprimentoRotate,posicao[1]-azulAlturaRotate), carimboRotate)
    posicao=acharCor(curvaNova,vermelho)
    curvaNova.paste(carimboRotate2, (posicao[0]-azulComprimentoRotate2,posicao[1]-azulAlturaRotate2), carimboRotate2)
    posicao=acharCor(curvaNova,vermelho)
    curvaNova.paste(carimboRotate2, (posicao[0]-azulComprimentoRotate2,posicao[1]-azulAlturaRotate2), carimboRotate2)
    posicao=acharCor(curvaNova,vermelho)
    carimboRotate=acharCor(carimboRotate,vermelho,excluir=True)
    curvaNova.paste(carimboRotate, (posicao[0]-azulComprimentoRotate,posicao[1]-azulAlturaRotate), carimboRotate)
    curvaNova.paste(carimboRotate3, (posicao[0]-azulComprimentoRotate3,posicao[1]-azulAlturaRotate3), carimboRotate3)
    curvaNova.putpixel(ultimaPos,(0,0,255,255))
    captarSalvar('curva'+str(numeroCurva+1)+'.png',curvaNova)
    print(str('curva'+str(numeroCurva+1)+'.png'))


