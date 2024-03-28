import pastaImagens as pI
import random

from time import time
from textos import embelezeTempo
from PIL import Image

def salva(nome,img):
    try:
        img.save(nome+'.png')
    except:
        img.save(nome+'1.png')

def procuraMaiorSize(imagens):
    largura=0
    altura=0
    for img in imagens:
        tamanho=Image.open(img).size
        if(tamanho[0]>=largura):
            largura=tamanho[0]
        if(tamanho[1]>=altura):
            altura=tamanho[1]
    tamanho=(largura,altura)
    return(tamanho)

def mergeTwoImages(img1,img2):
    tamanho=procuraMaiorSize([img1,img2])
    largura,altura=tamanho
    total=largura*altura
    novaImagem=Image.new('RGBA',tamanho,(0,0,0,0))
    imagem1=Image.open(img1).convert('RGBA')
    imagem2=Image.open(img2).convert('RGBA')
    firstImageToUse=Image.new('RGBA',tamanho,(0,0,0,0))
    secondImageToUse=Image.new('RGBA',tamanho,(0,0,0,0))
    firstImageToUse.paste(imagem1)
    secondImageToUse.paste(imagem2)
    #momento=0
    #porcentagem=0
    #ultimo=time()
    for y in range(altura):
        for x in range(largura):
            #momento+=1
            firstPixel=firstImageToUse.getpixel((x,y))
            secondPixel=secondImageToUse.getpixel((x,y))
            novaCor=[0,0,0,0]
            if(firstPixel[3]==0):
                if(secondPixel[3]!=0):
                    novaCor=list(secondPixel)
            elif(secondPixel[3]==0):
                novaCor=list(firstPixel)
            else:
                for index in range(4):
                    novaCor[index]=int((firstPixel[index]+secondPixel[index])/2.0)
            novaImagem.putpixel((x,y),tuple(novaCor))
            #if(int(momento*100/total)!=porcentagem):
            #    final=time()
            #    porcentagem=int(momento*100/total)
            #    pI.salva(nome,novaImagem,pasta='media',extensao='.png')
            #    print(str(porcentagem)+'%')
            #    print('você esperou: '+embelezeTempo(final-ultimo))
            #    ultimo=final
    return(novaImagem)
    
print('diga um assunto')
assunto=input()
imagens=pI.pegaAssunto(assunto)
quantia=len(imagens)
nome=assunto
numeroPossivel=0
while(2**numeroPossivel<quantia):
    numeroPossivel+=1
numeroPossivel-=1
print('modo de exclusão')
print('4-maiores')
print('3-primeiras')
print('2-ultimas')
print('1-aleatorio')
print('0-seleção')
modo=input()
print('com exclusão ou sem?[1/0]')
exc=input()
delete=(exc=='1')
inicio=time()
while(len(imagens)>2**numeroPossivel):
    if(modo=='1'):
        imagens.pop(random.randint(0,len(imagens)-1))
    elif(modo=='2'):
        imagens.pop(-1)
    elif(modo=='3'):
        imagens.pop(0)
    elif(modo=='4'):
        maior=0
        tamanho=0
        for index in range(len(imagens)):
            tamanhoTeste=Image.open(imagens[index]).size
            tamanhoTeste=tamanhoTeste[0]*tamanhoTeste[1]
            if(tamanhoTeste>=tamanho):
                tamanho=tamanhoTeste
                maior=index
        imagens.pop(maior)
    else:
        for index in range(len(imagens)):
            print('{0:04d} - '.format(index)+imagens[index])
        print('\ndigite qual ou quais excluir')
        exclusao=input()
        if(exclusao.find(',')==-1):
            imagens.pop(int(exclusao))
        else:
            exclusoes=exclusao.split(',')
            for item in exclusoes:
                if(len(imagens)>2**numeroPossivel):
                    if(int(item)<len(imagens)):
                        imagens.pop(int(item))
                else:
                    break
print(2**numeroPossivel)
print(len(imagens))
for potencia in range(numeroPossivel):
    metade=int(len(imagens)/2)
    nomeMedio=nome+' medio'
    pasta=[nomeMedio,nomeMedio+' '+str(metade)]
    newImages=[]
    for index in range(metade):
        img1=imagens[index]
        img2=imagens[index+metade]
        imagem=mergeTwoImages(img1,img2)
        img=pI.salva(nomeMedio+str(index),imagem,pasta=pasta,extensao='.png')
        newImages.append(img)
    imagens=newImages
if(delete):
    pI.delete(nomeMedio,pastaOutput=True)
imagem.save('mediaFinal.png')
pI.salva(nomeMedio,imagem,pasta='media',extensao='.png')
fim=time()
print('tempo gasto: '+embelezeTempo(fim-inicio))
