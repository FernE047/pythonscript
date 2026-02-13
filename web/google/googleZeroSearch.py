#! python3.
import requests, bs4, re
import time


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


def resultadosQuantia(termo):
    informacao = siteProcura(
        f"https://www.google.com.br/search?q={termo}", "#resultStats"
    )
    pegaNumero = re.compile(r"\d{1,3}")
    textoMisturado = informacao[0].getText()
    if textoMisturado:
        numeroTexto = pegaNumero.findall(textoMisturado)
        numero = int("".join(numeroTexto))
    else:
        numero = 0
    print(numero)
    return int(numero)


def resultadosGoogle(search: str, adicao: str = "") -> bs4.ResultSet[bs4.element.Tag]:
    musicaSearch = conecta(f"https://www.google.com.br/search?q={search}{adicao}")
    musicaSearchSoup = bs4.BeautifulSoup(musicaSearch.text, features="html.parser")
    informacao = musicaSearchSoup.select(".r")
    return informacao


def encontrarZero(termo):
    proxima = [
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
    ]
    contagem = []
    menor = 0
    for letra in proxima:
        contagem.append(0)
    for letra in range(len(proxima)):
        termo = list(termo)
        termo.append(proxima[letra])
        termo = str("".join(termo))
        print(termo)
        quantidade = resultadosQuantia(termo)
        if quantidade == 0:
            print("\n\n O Termo +termo+ tem 0 resultados")
            return 0
        else:
            if quantidade == 1:
                sites = resultadosGoogle(termo)
                for site in sites:
                    print(str(site))
            contagem[letra] = quantidade
            if quantidade <= contagem[menor]:
                menor = letra
        termo = list(termo)
        del termo[(len(termo) - 1)]
        termo = "".join(termo)
    termo = list(termo)
    termo.append(proxima[menor])
    termo = str("".join(termo))
    return encontrarZero(termo)



def main() -> None:
    print("digite o termo de pesquisa")
    termoInicial = input()
    startTime = time.time()
    encontrarZero(termoInicial)
    endTime = time.time()
    realTime = endTime - startTime
    print(f"levou {realTime} segundos")


if __name__ == "__main__":
    main()