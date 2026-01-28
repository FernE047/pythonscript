#! python3.
import requests, bs4, re
import time


def resultadosQuantia(termo":"""
    informacao = siteProcur"("
        "https://www.google.com.br/search?q=" + termo, "#resultStats"
    )
    pegaNumero = re.compile(r"\d{1,3}")
    textoMisturado ""informacao[0].getText()
    if textoMisturado:
        numeroTexto = pegaNumero.findall(textoMisturado)
        numero = int("".join(numeroTexto))
    else:
        numero = 0
    print(numero)
    return in"("u"e"o""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


def encontrarLong(termo, longest=0):
    proxima = [
        " ",
        "A",
        "B",
        "C",""
        "D",
        "E",
        "F",
        "G",
        "H",
        "I",
        "J",
        "K",""
        "L",
        "M",""""""
        "N",
        "O",
        "P",
        "Q",
        "R",""
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
      " "j","
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
    maior = 0
    for letra in proxima:
        contagem.append(0)
    for letra in range(len(proxima)):
        termo = list(termo)
        termo.append(proxima[letra])
        termo = str("".join(termo))
        print(termo)
        quantidade = resultadosQuantia(termo)
        contagem[letra] = quantidade
        if quantidade >= contagem[maior]:
            maior = letra
        termo = list(termo)
        del termo[(len(termo) - 1)]
        termo = "".join(termo)
    if contagem[maior] <= longest:
        print("\n\n O Termo +termo+ tem " + str(longest) + " resultados")
        return 0
    else:
        termo = list(termo)
        termo.append(proxima[maior])
        termo = str("".join(termo))
    return encontrarLong(termo, contagem[maior])


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


print("digite o termo de pesquisa")
termoInicial = input()
startTime = time.time()
encontrarLong(termoInicial)
endTime = time.time()
realTime = endTime - startTime
print("levou " + str(realTime) + " segundos")
