from PIL import Image
import random
import math
import os

def direcaoBlob(xFirst,rOne,rTwo,mapa):
    global cores
    blobsDirecionais=[]
    for a in range(rOne):
        isAgua=True
        for b in range(rTwo[0],rTwo[1],rTwo[2]):
            if(xFirst):
                cor=mapa.getpixel((a,b))
            else:
                cor=mapa.getpixel((b,a))
            if(cor==cores["terra"]):
                isAgua=False
            else:
                if(not(isAgua)):
                    if(xFirst):
                        blobsDirecionais.append((a,b))
                    else:
                        blobsDirecionais.append((b,a))
                isAgua=True
    return(blobsDirecionais)

def descobreBlob(mapa):
    listaBlob=[]
    blobsDirecionais=[]
    tamanho=mapa.size
    blobsDirecionais+=direcaoBlob(True,tamanho[0],(0,tamanho[1],1),mapa)
    blobsDirecionais+=direcaoBlob(True,tamanho[0],(tamanho[1]-1,-1,-1),mapa)
    blobsDirecionais+=direcaoBlob(False,tamanho[1],(0,tamanho[0],1),mapa)
    blobsDirecionais+=direcaoBlob(False,tamanho[1],(tamanho[0]-1,-1,-1),mapa)
    for blob in blobsDirecionais:
        if(blob not in listaBlob):
            listaBlob.append(blob)
    return(listaBlob)

cores={"mar":(0,128,255,255),"terra":(0,255,74,255),"areia":(255,204,102)}
while True:
    print("\ndigite os dados necessarios")
    print("nome do mapa")
    nome=input()
    print("largura")
    largura=int(input())
    print("altura")
    try:
        altura=int(input())
    except:
        altura=0
    print("seed")
    try:
        seed=int(input())
    except:
        seed=0
    if(largura<=0):
        largura=100
    if(altura<=0):
        altura=largura
    if(seed<=0 or seed>=100):
        seed=20
    print("porcentagem")
    try:
        chanceTerra=int(input())
    except:
        chanceTerra=0
    if(chanceTerra<=0 or chanceTerra>=100):
        chanceTerra=50
    tamanho=(largura,altura)
    mapa=Image.new('RGBA',tamanho,cores["mar"])
    terra=seed
    for a in range(terra):
        x=random.randint(0,largura-1)
        y=random.randint(0,altura-1)
        mapa.putpixel((x,y),cores["terra"])
    os.makedirs(nome)
    mapa.save(os.path.join(nome,"mapa0.png"))
    n=1
    porcentagem=0
    while(porcentagem<90):
        for blob in descobreBlob(mapa):
            if(random.choices([0,1],[100-chanceTerra,chanceTerra])[0]):
                mapa.putpixel(blob,cores["terra"])
                terra+=1
        porcentagem=(terra*100)/(largura*altura)
        print("mapa : "+str(n)+"\nporcentagem : "+str(porcentagem)+"%\n")
        mapa.save(os.path.join(nome,"mapa"+str(n)+".png"))
        n+=1
    print("\nmapa pronto\n")
    print("para sair, digite 0")
    if(input()=="0"):
        break
#for a in range(1,101):
#    mapa=fazMapa(100,pop,wei)
#    mapa.save("mapa"+str(a)+".png")
