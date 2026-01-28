from textos import limpaSopa
import requests, bs4, re
import time
import os


def conecta(site: str) -> requests.Response:
    siteBaguncado = requests.get(site)
    while siteBaguncado.status_code != requests.codes.ok:
        siteBaguncado = requests.get(site)
    return siteBaguncado

generos = ["naruto",
           "boku-no-hero-academia-my-hero-academia",
           "fairy-tail",
           "shingeki-no-kyojin-attack-on-titan",
           "haikyuu",
           "outros",
           "one-piece",
           "saint-seiya",
           "pokemon",
           "dragon-ball",
           "demon-slayer-kimetsu-no-yaiba",
           "the-seven-deadly-sins-nanatsu-no-taizai", #100
           "death-note",
           "jojo-no-kimyou-na-bouken-jojos-bizarre-adventure",
           "jujutsu-kaisen",
           "kuroko-no-basuke",
           "hunter-x-hunter",
           "tokyo-ghoul",
           "yuri-on-ice",
           "yakusoku-no-neverland-the-promised-neverland",
           "high-school-dxd",
           "sword-art-online"]
nomeFile = "historias\\fanfic{0:04d}.txt"
for genero in generos:
    site = "https://www.spiritfanfiction.com/categorias/" + genero + "?pagina="
    for pagina in range(1,101):
        siteBagunca = conecta(site + str(pagina))
        siteSoup = bs4.BeautifulSoup(siteBagunca.text,features = "html.parser")
        resumos = siteSoup.select(".limit_height")
        resumos = [limpaSopa(resumo.getText()) for resumo in resumos]
        links = siteSoup.select(".link")
        titulos = []
        for link in links:
            titulo = link.get("title")
            if titulo.find("Fanfic ") != -1:
                titulos.append(titulo[20:])
        for indice in range(10):
            file = open(nomeFile.format(len(os.listdir("historias"))),'w')
            try:
                file.write(titulos[indice]+" : "+resumos[indice])
                print(titulos[indice],end='\n\n')
                file.close()
            except:
                file.close()
        time.sleep(10)
