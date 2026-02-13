from internet import siteProcura
from time import time
import shelve
import requests
import bs4
import re


def print_elapsed_time(seconds: float) -> None:
    if seconds < 0:
        seconds = -seconds
        sign = "-"
    else:
        sign = ""
    total_ms = int(round(seconds * 1000))
    ms = total_ms % 1000
    total_s = total_ms // 1000
    s = total_s % 60
    total_min = total_s // 60
    m = total_min % 60
    total_h = total_min // 60
    h = total_h % 24
    d = total_h // 24
    parts: list[str] = []

    def add(value: int, singular: str, plural: str) -> None:
        if value:
            parts.append(f"{value} {singular if value == 1 else plural}")

    add(d, "day", "days")
    add(h, "hour", "hours")
    add(m, "minute", "minutes")
    add(s, "second", "seconds")
    if ms or not parts:
        parts.append(f"{ms} millisecond" if ms == 1 else f"{ms} milliseconds")
    print(f"{sign}{', '.join(parts)}")


def procuraTipo(informacao, alolan, mega=False):
    if not (mega):
        trInfo = informacao.select("tr")
        if trInfo:
            if alolan:
                informacao = trInfo[1]
            else:
                informacao = trInfo[0]
        imgTags = informacao.select("img")
        tipos = []
        for info in imgTags:
            tipo = info.get("alt")
            tipos.append(tipo[:-5])
    else:
        imgTags = informacao
        tipos = []
        for info in imgTags:
            tipo = info.get("src")
            tipos.append(tipo[17:-4].title())
    return tipos


def tiraEspaçoBranco(texto: str) -> str:
    for espaco in [" ", "\n", "\t"]:
        if espaco in texto:
            texto = texto.replace(espaco, "")
    return texto


def limpaInfo(informacao):
    informacao.pop(1)
    informacao.pop(1)
    informacao.pop(2)
    for index in range(6):
        informacao[index] = tiraEspaçoBranco(informacao[index].getText())
    return informacao


def procuraMegaIndex(info, nome):
    indexes = []
    for index in range(len(info)):
        if info[index].getText().find(nome) != -1:
            indexes.append(index)
    return indexes


def capturaDados(info, alolan=False):
    dados = {"name": info[0]}
    if info[1].find("Genderless") != -1:
        dados["male rate"] = -1
        dados["female rate"] = -1
    else:
        rate = info[1].split()
        porcento = rate[1].index("%")
        dados["male rate"] = float(rate[1][2:porcento])
        porcento = rate[2].index("%")
        dados["female rate"] = float(rate[2][2:porcento])
    height = info[2].split()
    if alolan:
        dados["height"] = float(height[-1][:-1])
    else:
        if info[2].find("/") == -1:
            dados["height"] = float(height[1][:-1])
        else:
            dados["height"] = float(height[-3][:-1])
    weight = info[3].split()
    if alolan:
        dados["weight lbs"] = float(weight[2][:-3])
        dados["weight kg"] = float(weight[-1][:-2])
    else:
        dados["weight lbs"] = float(weight[0][:-3])
        if info[2].find("/") == -1:
            dados["weight kg"] = float(weight[1][:-2])
        else:
            dados["weight kg"] = float(weight[-3][:-2])
    try:
        dados["capture rate"] = int(info[4])
    except:
        dados["capture rate"] = int(info[4].split()[0])
    egg = list(info[5])
    while "," in egg:
        egg.pop(egg.index(","))
    egg = "".join(egg)
    dados["base egg steps"] = int(egg)
    dados["alola"] = False
    dados["mega"] = False
    return dados


def debugImprime(dados, numero):
    print(f"pokemon : {numero:03d}")
    for item in dados:
        print(f"{item} : {dados[item]}")
    print("")



def main() -> None:
    with shelve.open("BDPokemonNoDetails") as BD:
        serebiiSite = "https://www.serebii.net/pokedex-sm/{0:03d}.shtml"
        TOTAL = 809
        try:
            for a in range(799, TOTAL + 1):
                inicio = time()
                siteDestino = serebiiSite.format(a)
                siteBagunca = requests.get(siteDestino)
                while siteBagunca.status_code != requests.codes.ok:
                    siteBagunca = requests.get(siteDestino)
                siteSoup = bs4.BeautifulSoup(siteBagunca.text, features="html.parser")
                siteBagunca = None
                informacaoBruta = siteSoup.select(".fooinfo")
                informacaoTipo = siteSoup.select(".cen")
                informacaoTipo = [informacaoTipo[a] for a in [0, -2, -1]]
                mega = [informacaoTipo[-1].select("img"), informacaoTipo[-2].select("img")]
                tipo = procuraTipo(informacaoTipo[0], False)
                informacao = limpaInfo(informacaoBruta[1:10])
                pokemonDados = capturaDados(informacao)
                pokemonDados["tipo"] = tipo
                if a < 150:
                    alolan = informacao[2].find("/") != -1
                else:
                    alolan = False
                BD[f"{a:03d}"] = pokemonDados
                debugImprime(pokemonDados, a)
                if alolan:
                    pokemonDados = capturaDados(informacao, alolan=alolan)
                    informacaoTipo = siteSoup.select(".cen")[0]
                    tipo = procuraTipo(informacaoTipo, True)
                    pokemonDados["name"] = f"Alolan {pokemonDados['name']}"
                    pokemonDados["tipo"] = tipo
                    pokemonDados["alola"] = alolan
                    BD[f"{a:03d}Alolan"] = pokemonDados
                    debugImprime(pokemonDados, a)
                else:
                    if (mega[0]) or (mega[1]):
                        if (a != 383) and (a != 382) and (a != 800):
                            add = "Mega"
                        elif a == 800:
                            add = "Ultra"
                            mega[1] = []
                        else:
                            add = "Primal"
                        nome = f"{add} {pokemonDados['name']}"
                        indexMega = procuraMegaIndex(informacaoBruta, nome)
                        if (len(indexMega) % 2) and (len(indexMega) > 1):
                            indexMega.pop(0)
                        elif (a > 300) and (len(indexMega) % 2 == 0):
                            indexMega.pop(0)
                        for index in range(2):
                            imgTag = mega[index]
                            if imgTag:
                                informacao = informacaoBruta[
                                    indexMega[index] : indexMega[index] + 9
                                ]
                                informacao = limpaInfo(informacao)
                                pokemonDados = capturaDados(informacao)
                                tipo = procuraTipo(imgTag, False, mega=True)
                                pokemonDados["tipo"] = tipo
                                pokemonDados["mega"] = True
                                BD[f"{a:03d}{add}"] = pokemonDados
                                debugImprime(pokemonDados, a)
                duracao = time() - inicio
                print_elapsed_time(duracao)
                print("falta = ")
                print_elapsed_time(duracao * (TOTAL - a))
        except Exception as e:
            print(e)


if __name__ == "__main__":
    main()