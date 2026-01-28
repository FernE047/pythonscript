from PIL import Image
import requests, bs4, re
from typing import cast
import os


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

def ondeComecaHttp(palavra:str) -> int:
    for index in range(len(palavra)):
        if (
            (palavra[index] == "h")
            and (palavra[index + 1] == "t")
            and (palavra[index + 2] == "t")
            and (palavra[index + 3] == "p")
        ):
            return index
    raise ValueError("no https found")


def encontraSite(palavra:str) -> str:
    site = ""
    comeco = ondeComecaHttp(palavra)
    for a in range(comeco, len(palavra)):
        if palavra[a] != "&":
            site += palavra[a]
        else:
            return site
    raise ValueError("no & finish found")

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
        site = encontraSite(bomResultado)
        nomeSite = qualSite(site)
        print(site)
        print(nomeSite+"\n")
        if nomeSite=='genius':
            if(tem=="album"):
                complemento=procuraComplemento(site)
                if(tem==complemento):
                    return(site)
            else:
                return(site)


def siteProcura(site: str, html: str) -> bs4.ResultSet[bs4.element.Tag]:
    siteBaguncado = conecta(site)
    siteSoup = bs4.BeautifulSoup(siteBaguncado.text, features="html.parser")
    informacao = siteSoup.select(html)
    return informacao


def fazImagem(site,pasta="imagens/"):
    titulo = siteProcura(site,'.header_with_cover_art-primary_info-title')
    titulo = textos.limpaSopa(titulo)
    print(titulo+"\n")
    informacao = siteProcura(site,'.lyrics')
    musica = textos.limpaSopa(informacao)
    print(musica+"\n")
    musicaSeparada=musica.split(" ")
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

def pegaTodosSites(informacao: bs4.ResultSet[bs4.element.Tag]) -> list[str]:
    sites:list[str] = []
    for info in informacao:
        try:
            bomResultado = cast(str,info.select('a')[0].get('href'))
        except Exception as _:
            continue
        site = encontraSite(bomResultado)
        nomeSite = qualSite(site)
        print(site)
        print(nomeSite+"\n")
        if nomeSite=='genius':
            sites.append(site)
    return(sites)

def albumImagens(site,album):
    fazDiretorio('album/'+album)
    faixa=1
    informacao = siteProcura(site,'.u-display_block')
    musicasSites = pegaTodosSites(informacao)
    for site in musicasSites:
        fazImagem(site,pasta=f'album/{album}/{faixa:03d}-')
        faixa+=1

def artistImagens(site,artist):
    fazDiretorio(f'artist/{artist}')
    faixa=1
    informacao = siteProcura(site,'.mini_card')
    musicasSites = pegaTodosSites(informacao)
    for site in musicasSites:
        fazImagem(site,pasta=f'artist/{artist}/{faixa:03d}-')
        faixa+=1

def fazDiretorio(diretorio):
    diretorio=f'C:/pythonscript/EARWORM/{diretorio}'
    os.mkdir(diretorio)

def novoSite(site):
    informacao=siteProcura(site,'.header_with_cover_art-primary_info-primary_artist')
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
        informacao = pesquisaGoogle(tituloFormatada,adicao="%20albums+site%3Ahttps%3A%2F%2Fgenius.com%2F")
        site = achaGenius(informacao,tem="album")
        nome = titulo[6:]
        albumImagens(site,nome)
    elif(artist):
        informacao = pesquisaGoogle(tituloFormatada,adicao="%20artist+site%3Ahttps%3A%2F%2Fgenius.com%2F")
        site = achaGenius(informacao,tem="artist")
        if(procuraComplemento(site)!="artist"):
            site=novoSite(site)
        nome = titulo[7:]
        artistImagens(site,nome)
    else:
        informacao = pesquisaGoogle(tituloFormatada,adicao="+site%3Ahttps%3A%2F%2Fgenius.com%2F")
        site = achaGenius(informacao)
        fazImagem(site)
