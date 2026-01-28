import requests, bs4, re
import os
import limpaSopa
import internet
import textos
import pyperclip


def conecta(site: str) -> requests.Response:
    siteBaguncado = requests.get(site)
    while siteBaguncado.status_code != requests.codes.ok:
        siteBaguncado = requests.get(site)
    return siteBaguncado


def pesquisaGoogle(
    search: str, adicao: str = "%20full%20lyrics"
) -> bs4.ResultSet[bs4.element.Tag]:
    musicaSearch = conecta(f"https://www.google.com.br/search?q={search}{adicao}")
    musicaSearchSoup = bs4.BeautifulSoup(musicaSearch.text, features="html.parser")
    informacao = musicaSearchSoup.select(".r")
    return informacao


def qualSite(site: str) -> str:
    dot_com_index = site.find(".com")
    if dot_com_index == -1:
        raise ValueError("no .com found")
    if site[:12] == "https://www.":
        return site[12:dot_com_index]
    if site[:11] == "http://www.":
        return site[11:dot_com_index]
    if site[:8] == "https://":
        return site[8:dot_com_index]
    if site[:7] == "http://":
        return site[7:dot_com_index]
    return site[:dot_com_index]

def ondeComecaHttp(palavra: str) -> int:
    for index in range(len(palavra)):
        if (
            (palavra[index] == "h")
            and (palavra[index + 1] == "t")
            and (palavra[index + 2] == "t")
            and (palavra[index + 3] == "p")
        ):
            return index
    raise ValueError("no https found")


def encontraSite(palavra: str) -> str:
    site = ""
    comeco = ondeComecaHttp(palavra)
    for a in range(comeco, len(palavra)):
        if palavra[a] != "&":
            site += palavra[a]
        else:
            return site
    raise ValueError("no & finish found")

def achaGenius(informacao):
    for info in informacao:
        try:
            bomResultado = info.select('a')[0].get('href')
        except:
            continue
        site = encontraSite(bomResultado)
        nomeSite = qualSite(site)
        if nomeSite=='genius':
            return(site)
        
def achaLetra(site):
    titulo = internet.siteProcura(site,'.header_with_cover_art-primary_info-title')
    titulo = limpaSopa.limpa(titulo)
    print(titulo+"\n")
    informacao = internet.siteProcura(site,'.lyrics')
    musica = limpaSopa.limpa(informacao)
    print(musica+"\n")
    musicaSeparada=musica.split(" ")
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
        nomeNovo = os.path.join(pasta,f'{n+1:03d}-'+textos.fazNomeArquivo(frase)+".png")
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
        lyrics = musica.split(" ")
        titulo = titulo[-10:]
    elif(titulo[:4]=="cola"):
        lyricsSuja = pyperclip.paste()
        musica = limpaSopa.limpa(lyricsSuja)
        print(musica+"\n")
        lyrics = musica.split(" ")
        titulo = titulo[5:]
    else:
        tituloList = list(titulo)
        tituloFormatada = ""
        for letra in range(len(tituloList)):
            if(tituloList[letra] == " "):
                tituloList[letra] = "%20"
            tituloFormatada += tituloList[letra]
        print()
        informacao = pesquisaGoogle(tituloFormatada,adicao="%20full%20lyrics")
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
