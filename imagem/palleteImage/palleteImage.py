from PIL import Image
import os
import pastaImagens as pI

def pegaPaleta(img):
    print("pegando paleta, por favor aguarde")
    imagem=Image.open(img).convert("RGBA")
    largura,altura=imagem.size
    paleta=[]
    for x in range(largura):
        for y in range(altura):
            pixel=imagem.getpixel((x,y))
            if(pixel not in paleta):
                paleta.append(pixel)
    return(paleta)

def pegaPaletas(imgs):
    print("pegando paleta, por favor aguarde, pode demorar muito")
    paleta=[]
    for img in imgs:
        print(img)
        imagem=Image.open(img).convert("RGBA")
        largura,altura=imagem.size
        for x in range(largura):
            for y in range(altura):
                pixel=imagem.getpixel((x,y))
                if(pixel not in paleta):
                    paleta.append(pixel)
    return(paleta)

def aplicaPaleta(paleta,img):
    global nome
    imagem=Image.open(img).convert("RGBA")
    largura,altura=imagem.size
    imagemFiltrada=imagem.copy()
    print(largura)
    for x in range(largura):
        if not(x%100):
            print(x)
            try:
                imagemFiltrada.save(nome)
            except:
                imagemFiltrada.save(nome[:-4]+"ToSee.png")
        for y in range(altura):
            pixel=imagemFiltrada.getpixel((x,y))
            if(pixel in paleta):
                imagemFiltrada.putpixel((x,y),pixel)
                continue
            novaCor=paleta[0]
            proximidadeNovaCor=256*3
            for cor in paleta:
                red=abs(cor[0]-pixel[0])
                green=abs(cor[1]-pixel[1])
                blue=abs(cor[2]-pixel[2])
                proximidade=red+green+blue
                if(proximidade<proximidadeNovaCor):
                    novaCor=cor
                    proximidadeNovaCor=proximidade
            imagemFiltrada.putpixel((x,y),novaCor)
    return(imagemFiltrada)


def main() -> None:
    saida="1"
    while(saida!="0"):
        nome=""
        print("digite o assunto da imagem que será paleta")
        assunto=input()
        if(assunto[:7]=="paleta "):
            paletaSample=pegaPaleta(os.path.join("paleta","paleta"+assunto[7:]+".png"))
            nome+=assunto[7:].proper()
        elif(assunto[:6]=="pasta "):
            imagens=pI.pegaAssunto(assunto)
            paletaSample=pegaPaletas(imagens)
            nome+=assunto[6:].proper()+str(numImagem)
        else:
            imagem=pI.umaImagem(assunto)
            paletaSample=pegaPaleta(imagem)
            nome+=assunto.proper()+str(numImagem)
        print("tamanho da paleta:"+str(len(paletaSample)))
        print("\ndigite o assunto da imagem para adaptar")
        assunto=input()
        imagens=pI.pegaAssunto(assunto)
        for indice,imagem_a in enumerate(imagens):
            print(f"{indice}  -  {imagem_a}")
        print("\nqual imagem? 0 a "+str(len(imagens)))
        numImagem=int(input())
        imagem=imagens[numImagem]
        nome=assunto.proper()+nome+str(numImagem)+".png"
        nome=os.path.join("imagens",nome)
        print(imagem)
        imagemPaletada=aplicaPaleta(paletaSample,imagem)
        imagemPaletada.save(nome)
        print("digite 0 para sair")
        saida=input()


if __name__ == "__main__":
    main()