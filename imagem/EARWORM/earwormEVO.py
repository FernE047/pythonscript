from PIL import Image
import requests, bs4, re
import os
import internet
import textos

def procuraComplemento(site):
    if(site[20]=="r"):
        return("artist")
    else:
        return("album")

def achaGenius(informacao,tem=""):
    for info in informacao:
        try:
            bomResultado = info.select('a')[0].get('href')
        except:
            continue
        site = internet.encontraSite(bomResultado)
        nomeSite = internet.qualSite(site)
        print(site)
        print(nomeSite+"\n")
        if nomeSite=='genius':
            if(tem=="album"):
                complemento=procuraComplemento(site)
                if(tem==complemento):
                    return(site)
            else:
                return(site)
        
def fazImagem(site,pasta="imagens/"):
    titulo = internet.siteProcura(site,'.header_with_cover_art-primary_info-title')
    titulo = textos.limpaSopa(titulo)
    print(titulo+"\n")
    informacao = internet.siteProcura(site,'.lyrics')
    musica = textos.limpaSopa(informacao)
    print(musica+"\n")
    musicaSeparada=textos.separaPalavras(musica)
    quantPalavras=len(musicaSeparada)
    print("quantidade de palavras: "+str(quantPalavras)+"\n")
    if(quantPalavras):
        imagem=Image.new('RGBA',(quantPalavras,quantPalavras),(0,0,0,255))
        for coordX in range(quantPalavras):
            for coordY in range(quantPalavras):
                if(musicaSeparada[coordX]==musicaSeparada[coordY]):
                    imagem.putpixel((coordX,coordY),(255,0,0,255))
        imagem.save('C:/pythonscript/EARWORM/'+pasta+str(titulo)+".png")
    print("feita com sucesso\n\n")

def albumImagens(site,album):
    fazDiretorio('album/'+album)
    faixa=1
    informacao = internet.siteProcura(site,'.u-display_block')
    musicasSites = internet.pegaTodosSites(informacao)
    for site in musicasSites:
        fazImagem(site,pasta=f'album/{album}/{faixa:03d}-')
        faixa+=1

def artistImagens(site,artist):
    fazDiretorio(f'artist/{artist}')
    faixa=1
    informacao = internet.siteProcura(site,'.mini_card')
    musicasSites = internet.pegaTodosSites(informacao)
    for site in musicasSites:
        fazImagem(site,pasta=f'artist/{artist}/{faixa:03d}-')
        faixa+=1

def fazDiretorio(diretorio):
    diretorio=f'C:/pythonscript/EARWORM/{diretorio}'
    os.mkdir(diretorio)

def novoSite(site):
    informacao=internet.siteProcura(site,'.header_with_cover_art-primary_info-primary_artist')
    return(informacao[0].get('href'))
    
album=False
artist=False
while True:
    print("\ndigite o titulo da música")
    titulo = input()
    if(titulo=="0"):
        break
    tituloList = list(titulo)
    if tituloList[:5]==['a','l','b','u','m']:
        tituloList=tituloList[6:]
        album=True
    if tituloList[:6]==['a','r','t','i','s','t']:
        tituloList=tituloList[7:]
        artist=True
    tituloFormatada = ""
    for index,letra in enumerate(tituloList):
        if(letra == " "):
            tituloList[index] = "%20"
        tituloFormatada += tituloList[index]
    if(album):
        informacao = internet.pesquisaGoogle(tituloFormatada,adicao="%20albums+site%3Ahttps%3A%2F%2Fgenius.com%2F")
        site = achaGenius(informacao,tem="album")
        nome = titulo[6:]
        albumImagens(site,nome)
    elif(artist):
        informacao = internet.pesquisaGoogle(tituloFormatada,adicao="%20artist+site%3Ahttps%3A%2F%2Fgenius.com%2F")
        site = achaGenius(informacao,tem="artist")
        if(procuraComplemento(site)!="artist"):
            site=novoSite(site)
        nome = titulo[7:]
        artistImagens(site,nome)
    else:
        informacao = internet.pesquisaGoogle(tituloFormatada,adicao="+site%3Ahttps%3A%2F%2Fgenius.com%2F")
        site = achaGenius(informacao)
        fazImagem(site)
