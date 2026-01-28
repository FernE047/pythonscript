from PIL import Image
import os

def vetorParaImagem(vetor):
    altura=len(vetor)
    largura=max([len(a) for a in vetor])
    print('\naltura: '+str(altura)+'\nlargura: '+str(largura))
    for a in range(altura):
        while(len(vetor[a])<largura):
            vetor[a].append(0)
    imagem=Image.new('RGBA',(largura,altura),(255,255,255,255))
    for y in range(altura):
        for x in range(largura):
            if(vetor[y][x]):
                imagem.putpixel((x,y),(0,0,0,255))
    return(imagem)

def proximoFractal(brick,guide):
    larguraGuide,alturaGuide=guide.size
    larguraBrick,alturaBrick=brick.size
    largura=larguraGuide*larguraBrick
    altura=alturaGuide*alturaBrick
    fractal=Image.new('RGBA',(largura,altura),(255,255,255,255))
    if((largura>5000)or(altura>5000)):
       return('')
    for x in range(larguraGuide):
        for y in range(alturaGuide):
            if(guide.getpixel((x,y))==(0,0,0,255)):
               fractal.paste(brick,(x*larguraBrick,y*alturaBrick))
    return(fractal)

def fazNFractais(vetor,nome):
    novaPasta=os.path.join(os.getcwd(),nome.proper())
    os.makedirs(novaPasta)
    guia=vetorParaImagem(vetor)
    bloco=guia
    pastaSalvar=os.path.join(novaPasta,f'{nome.proper()}{1:02d}.png')
    bloco.save(pastaSalvar)
    a=2
    while True:
        bloco=proximoFractal(bloco,guia)
        if(bloco==''):
            print('feito '+str(a)+' fractais\n')
            return()
        pastaSalvar=os.path.join(novaPasta,f'{nome.proper()}{a:02d}.png')
        bloco.save(pastaSalvar)
        a+=1

def ehInt(num):
    try:
        num=int(num)
        return(True)
    except:
        return(False)
        

def leVetores():
    randomIndex=29
    vetor=[[]]
    indice=0
    print('"0" para nada\n"1" para valor\n"vazio" para nova linha\noutro para salvar\n"apg" no fim para salvar apagando')
    while True:
        print(vetor)
        entrada=input()
        if(entrada==''):
            indice+=1
            vetor.append([])            
        elif((ehInt(entrada[0]))and(len(entrada)>=2)):
            vetor[indice]=[int(a) for a in list(entrada)]
            indice+=1
            vetor.append([]) 
        elif(entrada=='0'):
            vetor[indice].append(0)
        elif(entrada=='1'):
            vetor[indice].append(1)            
        else:
            if(entrada[-3:]=='apg'):
                vetor=vetor[:-1]
                entrada=entrada[:-3]
            if(entrada=='random'):
                entrada+=str(randomIndex)
                randomIndex+=1
            fazNFractais(vetor,entrada)
            vetor=[[]]
            indice=0
    
leVetores()
