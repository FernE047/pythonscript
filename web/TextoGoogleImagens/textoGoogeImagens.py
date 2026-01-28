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

def baixaImagens(lyrics,titulo):
    total=len(lyrics)
    titulo=textos.fazNomeArquivo(titulo)
    pasta=os.path.join('C:\\','pythonscript','web','TextoGoogleImagens',titulo)
    palavras={}
    for number,palavra in enumerate(lyrics):
        if(textos.isBadList(palavra)):
            palavra=textos.trocaBadForSafe(palavra)
        if(palavra not in palavras):
            palavras[palavra]=[]
            palavras[palavra]+=[number]
        else:
            palavras[palavra]+=[number]
    for palavra,lista in palavras.items():
        print(palavra+" : "+str(len(lista)))
    total=len(palavras)
    for n,(palavra,lista) in enumerate(palavras.items()):
        print("palavra "+str(n+1)+" de "+str(total)+" :")
        print(palavra)
        quantia=len(lista)
        os.system('google_images_download.py -o "'+pasta+'" -k "'+palavra+'" -l '+str(quantia))
        imagens=os.listdir(os.path.join(pasta,palavra))
        for numero,nome in enumerate(imagens):
            nomeOriginal = os.path.join(os.path.join(pasta,palavra),nome)
            nomeNovo = os.path.join(pasta,f'{lista[numero]+1:03d}-{palavra}.png')
            os.rename(nomeOriginal,nomeNovo)
        os.rmdir(os.path.join(pasta,palavra))
        
        

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
    baixaImagens(lyrics,titulo)

