from PIL import Image
import requests, bs4, re
import os


def ondeComecaHttp(palavra):
    for index in range(len(palavra)):
        if (
            (palavra[index] == "h")
            and (palavra[index + 1] == "t")
            and (palavra[index + 2] == "t")
            and (palavra[index + 3] == "p")
        ):
            return index
    print("no https found")
    return "ERROR01"


def encontraSite(palavra):
    site = ""
    comeco = ondeComecaHttp(palavra)
    for a in range(comeco, len(palavra)):
        if palavra[a] != "&":
            site += palavra[a]
        else:
            return site
    print("no & finish found")
    return "ERROR 02"


def qualSite(site):
    if site[4] == "s":
        if site[8] == "w":
            a = 12
        else:
            a = 8
    else:
        if site[7] == "w":
            a = 11
        else:
            a = 7
    nome = ""
    while site[a] != ".":
        nome += site[a]
        a += 1
    return nome


def tudoMinuscula(musicaMixed):
    maiusculas = [
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
        "H",
        "I",
        "J",
        "K",
        "L",
        "M",
        "N",
        "O",
        "P",
        "Q",
        "R",
        "S",
        "T",
        "U",
        "V",
        "W",
        "X",
        "Y",
        "Z",
        "É",
        "À",
    ]
    minusculas = [
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "q",
        "r",
        "s",
        "t",
        "u",
        "v",
        "w",
        "x",
        "y",
        "z",
        "é",
        "à",
    ]
    musicaMinuscula = ""
    for letra in musicaMixed:
        if letra in maiusculas:
            for maiuscula, minuscula in zip(maiusculas, minusculas):
                if maiuscula == letra:
                    musicaMinuscula += minuscula
        else:
            musicaMinuscula += letra
    return musicaMinuscula


def tiraEspaco(musicaEspacada):
    charac = 0
    musicaLimpa = ""
    while charac < len(musicaEspacada):
        if musicaEspacada[charac] == " ":
            musicaLimpa += " "
            while (musicaEspacada[charac] == " ") and (
                charac < len(musicaEspacada) - 1
            ):
                charac += 1
            if charac == len(musicaEspacada) - 1:
                musicaLista = list(musicaLimpa)
                if musicaLista[0] == " ":
                    del musicaLista[0]
                musicaLimpa = ""
                for a in musicaLista:
                    musicaLimpa += str(a)
                charac += 1
            continue
        else:
            musicaLimpa += musicaEspacada[charac]
        charac += 1
    return tudoMinuscula(musicaLimpa)


def limpa(sopa):
    global alfabeto
    codigo = False
    musica = ""
    sopona = ""
    for pedaco in sopa:
        sopona += str(pedaco)
    for letra in sopona:
        if (letra == "<") or (letra == "["):
            codigo = True
            musica += " "
            continue
        if (letra == ">") or (letra == "]"):
            codigo = False
            continue
        if not (codigo):
            if letra in alfabeto:
                musica += letra
    return tiraEspaco(musica)


def separaPalavras(musica):
    palavras = musica.split(" ")
    return palavras


def conecta(site):
    siteBaguncado = requests.get(site)
    while siteBaguncado.status_code != requests.codes.ok:
        siteBaguncado = requests.get(site)
    return siteBaguncado


def pesquisaGoogle(search, adicao="%20full%20lyrics"):
    musicaSearch = conecta("https://www.google.com.br/search?q=" + search + adicao)
    musicaSearchSoup = bs4.BeautifulSoup(musicaSearch.text, features="html.parser")
    informacao = musicaSearchSoup.select(".r")
    return informacao


def procuraComplemento(site):
    if site[20] == "r":
        return "artist"
    else:
        return "album"


def achaGenius(informacao, tem=""):
    for info in informacao:
        bomResultado = info.select("a")[0].get("href")
        site = encontraSite(bomResultado)
        nomeSite = qualSite(site)
        print(site)
        print(nomeSite + "\n")
        if nomeSite == "genius":
            if tem == "album":
                complemento = procuraComplemento(site)
                if tem == complemento:
                    return site
            else:
                return site


def fazImagem(site, pasta="imagens/"):
    musicaSite = conecta(site)
    musicaSoup = bs4.BeautifulSoup(musicaSite.text, features="html.parser")
    titulo = musicaSoup.select(".header_with_cover_art-primary_info-title")
    titulo = limpa(titulo)
    print(titulo + "\n")
    informacao = musicaSoup.select(".lyrics")
    musica = limpa(informacao)
    print(musica + "\n")
    musicaSeparada = separaPalavras(musica)
    quantPalavras = len(musicaSeparada)
    print("quantidade de palavras: " + str(quantPalavras) + "\n")
    if quantPalavras:
        imagem = Image.new("RGBA", (quantPalavras, quantPalavras), (0, 0, 0, 255))
        for coordX in range(quantPalavras):
            for coordY in range(quantPalavras):
                if musicaSeparada[coordX] == musicaSeparada[coordY]:
                    imagem.putpixel((coordX, coordY), (255, 0, 0, 255))
        imagem.save("C:/pythonscript/EARWORM/" + pasta + str(titulo) + ".png")
    print("feita com sucesso\n\n")


def albumImagens(site, album):
    fazDiretorio("album/" + album)
    faixa = 1
    albumSite = conecta(site)
    albumSoup = bs4.BeautifulSoup(albumSite.text, features="html.parser")
    informacao = albumSoup.select(".u-display_block")
    musicasSites = []
    for info in informacao:
        musicasSites.append(info.get("href"))
    for site in musicasSites:
        fazImagem(site, pasta="album/" + album + "/{0:03d}-".format(faixa))
        faixa += 1


def artistImagens(site, artist):
    fazDiretorio("artist/" + artist)
    faixa = 1
    artistSite = conecta(site)
    artistSoup = bs4.BeautifulSoup(artistSite.text, features="html.parser")
    informacao = artistSoup.select(".mini_card")
    musicasSites = []
    for info in informacao:
        musicasSites.append(info.get("href"))
    for site in musicasSites:
        fazImagem(site, pasta="artist/" + artist + "/{0:03d}-".format(faixa))
        faixa += 1


def fazDiretorio(diretorio):
    diretorio = "C:/pythonscript/EARWORM/" + diretorio
    os.mkdir(diretorio)


def novoSite(site):
    artistSite = conecta(site)
    artistSoup = bs4.BeautifulSoup(artistSite.text, features="html.parser")
    informacao = artistSoup.select(".header_with_cover_art-primary_info-primary_artist")
    return informacao[0].get("href")


album = False
artist = False
alfabeto = [
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "W",
    "X",
    "Y",
    "Z",
    " ",
    "é",
    "á",
    "í",
    "ó",
    "ú",
    "ã",
    "à",
    "ê",
    "É",
    "À",
    "ç",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "0",
]
while True:
    print("\ndigite o titulo da música")
    titulo = input()
    if titulo == "0":
        break
    tituloList = list(titulo)
    if tituloList[:5] == ["a", "l", "b", "u", "m"]:
        tituloList = tituloList[6:]
        album = True
    if tituloList[:6] == ["a", "r", "t", "i", "s", "t"]:
        tituloList = tituloList[7:]
        artist = True
    tituloFormatada = ""
    for index, letra in enumerate(tituloList):
        if letra == " ":
            tituloList[index] = "%20"
        tituloFormatada += tituloList[index]
    if album:
        informacao = pesquisaGoogle(tituloFormatada, adicao="%20albums%20genius")
        site = achaGenius(informacao, tem="album")
        nome = titulo[6:]
        albumImagens(site, nome)
    elif artist:
        informacao = pesquisaGoogle(tituloFormatada, adicao="%20artist%20genius")
        site = achaGenius(informacao, tem="artist")
        if procuraComplemento(site) != "artist":
            site = novoSite(site)
        nome = titulo[7:]
        artistImagens(site, nome)
    else:
        informacao = pesquisaGoogle(tituloFormatada)
        site = achaGenius(informacao)
        fazImagem(site)
