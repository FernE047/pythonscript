from userUtil import pegaString
from textos import fazAudio


def invertePorPalavra(texto):
    novoTexto=[]
    for linha in (texto.split("\n")):
        for palavra in linha.split(" "):
            novoTexto+=[inverte(palavra)]
        novoTexto+="\n"
    novoTexto=" ".join(novoTexto)
    return(novoTexto)

def ninvertePorPalavra(texto):
    novoTexto=[];
    for palavra in texto.split(" "):
        novoTexto+=[inverte(palavra)]
    novoTexto=" ".join(novoTexto)
    fazAudio("invertidoPorPalavra",novoTexto)
    return(novoTexto)

def inverte(texto):
    novoTexto=""
    for a in reversed(list(texto)):
        novoTexto+=a
    return(novoTexto)

while True:
    nomeArquivo=pegaString("digite o nome do arquivo")
    texto=pegaString("digite alguma coisa e inverteremos")
    if(not(texto)):
        break
    print("simples:\n")
    simples=inverte(texto)
    if(nomeArquivo):
        fazAudio(nomeArquivo+"Invertido",simples)
    print(simples)
    print("\npor palavra:\n")
    complexo=invertePorPalavra(texto)
    if(nomeArquivo):
        fazAudio(nomeArquivo+"InvertidoPorPalavra",complexo)
    print(complexo)
