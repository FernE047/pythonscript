import requests, bs4, re
import os
import pyperclip


def tiraEspaco(text: str) -> str:
    while text.find("  ") != -1:
        text = text.replace("  ", " ")
    return text.lower().strip()


def limpa(sopa: bs4.ResultSet[bs4.element.Tag]) -> str:
    allowed = set(
        list(
            "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 éáíóúãàêÉÀç"
        )
    )
    raw = " ".join(tag.get_text(" ", strip=False) for tag in sopa)
    filtrado = "".join(ch for ch in raw if ch in allowed or ch.isspace())
    return tiraEspaco(filtrado)

def conecta(site: str) -> requests.Response:
    siteBaguncado = requests.get(site)
    while siteBaguncado.status_code != requests.codes.ok:
        siteBaguncado = requests.get(site)
    return siteBaguncado


def siteProcura(site: str, html: str) -> bs4.ResultSet[bs4.element.Tag]:
    siteBaguncado = conecta(site)
    siteSoup = bs4.BeautifulSoup(siteBaguncado.text, features="html.parser")
    informacao = siteSoup.select(html)
    return informacao


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
            bomResultado = info.select("a")[0].get("href")
        except:
            continue
        site = encontraSite(bomResultado)
        nomeSite = qualSite(site)
        if nomeSite=="genius":
            return(site)
        
def achaLetra(site):
    titulo = siteProcura(site,".header_with_cover_art-primary_info-title")
    titulo = limpa(titulo)
    print(f"{titulo}\n")
    informacao = siteProcura(site,".lyrics")
    musica = limpa(informacao)
    print(f"{musica}\n")
    musicaSeparada=musica.split(" ")
    return(musicaSeparada)

def baixaImagens(lyrics,titulo):
    total=len(lyrics)
    titulo=titulo.proper()
    pasta=os.path.join("./",titulo)
    palavras={}
    for number,palavra in enumerate(lyrics):
        if(palavra not in palavras):
            palavras[palavra]=[]
            palavras[palavra]+=[number]
        else:
            palavras[palavra]+=[number]
    for palavra,lista in palavras.items():
        print(f"{palavra} : {len(lista)}")
    total=len(palavras)
    for n,(palavra,lista) in enumerate(palavras.items()):
        print(f"palavra {n+1} de {total} :")
        print(palavra)
        quantia=len(lista)
        os.system(f"google_images_download.py -o {pasta} -k {palavra} -l {quantia}")
        imagens=os.listdir(os.path.join(pasta,palavra))
        for numero,nome in enumerate(imagens):
            nomeOriginal = os.path.join(os.path.join(pasta,palavra),nome)
            nomeNovo = os.path.join(pasta,f"{lista[numero]+1:03d}-{palavra}.png")
            os.rename(nomeOriginal,nomeNovo)
        os.rmdir(os.path.join(pasta,palavra))
        
        

def fazDiretorio(diretorio):
    diretorio=os.path.join("./",diretorio)
    os.mkdir(diretorio)

def novoSite(site):
    informacao=siteProcura(site,".header_with_cover_art-primary_info-primary_artist")
    return(informacao[0].get("href"))


def main() -> None:
    while True:
        print("\ndigite o titulo da música")
        titulo = input()
        if(titulo=="teste"):
            titulo="have faith saint pepsi"
        if(titulo=="0"):
            break
        elif(titulo[:5]=="texto"):
            lyricsSuja = titulo[6:]
            musica = limpa(lyricsSuja)
            print(f"{musica}\n")
            lyrics = musica.split(" ")
            titulo = titulo[-10:]
        elif(titulo[:4]=="cola"):
            lyricsSuja = pyperclip.paste()
            musica = limpa(lyricsSuja)
            print(f"{musica}\n")
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
        baixaImagens(lyrics,titulo)


if __name__ == "__main__":
    main()