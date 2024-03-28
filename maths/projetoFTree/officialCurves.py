from PIL import Image

vermelho=(255,0,0,255)
azul=(0,0,255,255)
preto=(0,0,0,255)
cores=(vermelho,azul,preto)

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
    img.save(nome)
    return(((left,up),(right,down)))

newTamanho=11
meio=int(newTamanho/2+1)
curvaNova=Image.new('RGBA',(newTamanho,newTamanho))
curvaNova.putpixel((meio,meio-1),azul)
curvaNova.putpixel((meio,meio),preto)
curvaNova.putpixel((meio,meio+1),vermelho)
captarSalvar('curva0.png',curvaNova)
for numeroCurva in range(0,10):
    nome='curva'+str(numeroCurva)+'.png'
    curvaAtual=Image.open(nome)
    larg,alt=curvaAtual.size
    newTamanho=newTamanho*2-1
    meio=int(newTamanho/2+1)
    azulComprimento,azulAltura=acharCor(curvaAtual,azul)
    print(str((azulAltura,azulComprimento)))
    carimbo=curvaAtual.copy()
    carimbo=carimbo.convert('RGBA')
    curvaNova=Image.new('RGBA', (newTamanho,newTamanho))
    curvaNova.paste(carimbo, (meio,meio))
    carimboRotate=carimbo.rotate(90, expand=True)
    carimboRotate=carimboRotate.convert('RGBA')
    azulComprimentoRotate,azulAlturaRotate=acharCor(carimboRotate,azul)
    print(str((azulComprimentoRotate,azulAlturaRotate)))
    carimbo=acharCor(carimbo,azul,excluir=True)
    carimboRotate=acharCor(carimboRotate,azul,excluir=True)
    posicao=acharCor(curvaNova,vermelho)
    curvaNova.paste(carimboRotate, (posicao[0]-azulComprimentoRotate,posicao[1]-azulAlturaRotate), carimboRotate)
    curvaNova=acharCor(curvaNova,vermelho,excluir=True)
    curvaNova.paste(carimbo, (posicao[0]-azulComprimento,posicao[1]-azulAltura), carimbo)
    posicao=acharCor(curvaNova,vermelho)
    curvaNova=acharCor(curvaNova,vermelho,excluir=True)
    curvaNova.paste(carimboRotate, (posicao[0]-azulComprimentoRotate,posicao[1]-azulAlturaRotate), carimboRotate)
    captarSalvar('curva'+str(numeroCurva+1)+'.png',curvaNova)
    print(str('curva'+str(numeroCurva+1)+'.png'))


