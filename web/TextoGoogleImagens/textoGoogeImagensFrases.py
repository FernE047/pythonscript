import requests, bs4, re
import os
import limpaSopa
import internet
import textos
import pyperclip

def achaGenius(informacao):
    for info in informacao:
        try:
            bomResultado = info.select('a')[0].get('href')
        except:
            continue
        site = internet.encontraSite(bomResultado)
        nomeSite = internet.qualSite(site)
        if nomeSite=='genius':
            return(site)
        
def achaLetra(site):
    titulo = internet.siteProcura(site,'.header_with_cover_art-primary_info-title')
    titulo = limpaSopa.limpa(titulo)
    print(titulo+"\n")
    informacao = internet.siteProcura(site,'.lyrics')
    musica = limpaSopa.limpa(informacao)
    print(musica+"\n")
    musicaSeparada=textos.separaPalavras(musica)
    return(musicaSeparada)

def baixaImagens(lyrics,titulo,adicao,tamanho):
    titulo=textos.fazNomeArquivo(adicao[0]+" "+titulo+" "+str(tamanho)+" "+adicao[1])
    pasta=os.path.join('C:\\','pythonscript','web','TextoGoogleImagens',titulo)
    newLyrics=[]
    frase=""
    for number,palavra in enumerate(lyrics):
        if(textos.isBadList(palavra)):
            palavra=textos.trocaBadForSafe(palavra)
        if(number%tamanho==0):
            if(adicao[0]!=""):
                frase+=adicao[0]+" "+palavra
            else:
                frase+=palavra
            if(tamanho==1):
                if(adicao[1]!=""):
                    frase+=" "+adicao[1]
                newLyrics+=[frase]
                frase=""
        elif(number%tamanho==tamanho-1):
            if(adicao[1]!=""):
                frase+=" "+palavra+" "+adicao[1]
            else:
                frase+=" "+palavra
            newLyrics+=[frase]
            frase=""
        else:
            frase+=" "+palavra
    if(frase!=""):
        if(len(lyrics)<tamanho):
            if(adicao[1]!=""):
                frase+=" "+adicao[1]
            newLyrics+=[frase]
        elif(newLyrics[-1]!=frase):
            if(adicao[1]!=""):
                frase+=" "+adicao[1]
            newLyrics+=[frase]
    print()
    for frase in newLyrics:
        print(frase+".")
    total=len(newLyrics)
    print()
    for n,frase in enumerate(newLyrics):
        print("frase "+str(n+1)+" de "+str(total)+" :")
        print(frase)
        os.system('google_images_download.py -o "'+pasta+'" -k "'+frase+'" -l 1')
        caminho=os.path.join(pasta,frase)
        nome=os.listdir(caminho)[0]
        nomeOriginal = os.path.join(caminho,nome)
        nomeNovo = os.path.join(pasta,'{0:03d}-'.format(n+1)+textos.fazNomeArquivo(frase)+".png")
        os.rename(nomeOriginal,nomeNovo)
        os.rmdir(caminho)
        
        

def fazDiretorio(diretorio):
    diretorio='C:/pythonscript/EARWORM/'+diretorio
    os.mkdir(diretorio)

def novoSite(site):
    informacao=internet.siteProcura(site,'.header_with_cover_art-primary_info-primary_artist')
    return(informacao[0].get('href'))
    
while True:
    print("\ndigite o titulo da música")
    titulo = input()
    if(titulo=="teste"):
        titulo="have faith saint pepsi"
    if(titulo=="0"):
        break
    elif(titulo[:5]=="texto"):
        lyricsSuja = titulo[6:]
        musica = limpaSopa.limpa(lyricsSuja)
        print(musica+"\n")
        lyrics = textos.separaPalavras(musica)
        titulo = titulo[-10:]
    elif(titulo[:4]=="cola"):
        lyricsSuja = pyperclip.paste()
        musica = limpaSopa.limpa(lyricsSuja)
        print(musica+"\n")
        lyrics = textos.separaPalavras(musica)
        titulo = titulo[5:]
    else:
        tituloList = list(titulo)
        tituloFormatada = ""
        for letra in range(len(tituloList)):
            if(tituloList[letra] == " "):
                tituloList[letra] = "%20"
            tituloFormatada += tituloList[letra]
        print()
        informacao = internet.pesquisaGoogle(tituloFormatada,adicao="%20full%20lyrics")
        site = achaGenius(informacao)
        print(site)
        lyrics = achaLetra(site)
    print("\nesse texto possui "+str(len(lyrics))+" palavras")
    print("\ntamanho")
    tamanho = int(input())
    print("\nprefixo")
    prefixo = input()
    print("\nsufixo")
    sufixo = input()
    adicao=[prefixo,sufixo]
    baixaImagens(lyrics,titulo,adicao,tamanho)
