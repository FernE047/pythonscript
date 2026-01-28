from time import time
from time import sleep
import os


def embelezeTempo(segundos: float) -> str:
    if segundos < 0:
        segundos = -segundos
        sign = "-"
    else:
        sign = ""
    total_ms = int(round(segundos * 1000))
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
    return sign + ", ".join(parts)

def renome(origemName,destinoName):
    origem = open(origemName,'r')
    destino = open(destinoName,'w')
    linha = origem.readline()
    while linha:
        destino.write(linha)
        linha = origem.readline()
    origem.close()
    destino.close()

def alteraChainFile(termos, isTitulo):
    if isTitulo:
        diretorio = DIRECTORY + "chainTitle//" + str(TAMANHO)
    else:
        diretorio = DIRECTORY + "chainStory//" + str(TAMANHO)
    nomeTemp = diretorio + "//c.txt"
    nomeReal = diretorio + "//chain.txt"
    fileWrite = open(nomeTemp,'w')
    if "chain.txt" in os.listdir(diretorio):
        fileRead = open(nomeReal,'r')
        linha = fileRead.readline()
        while linha:
            palavras = linha.split()
            termoTestando = " ".join(palavras[:-1])
            while termoTestando in termos:
                palavras[-1] = str(int(palavras[-1])+1)
                termos.remove(termoTestando)
            fileWrite.write(" ".join(palavras) + "\n")
            if not termos:
                break
            linha = fileRead.readline()
        fileRead.close()
        if termos:
            for termo in termos:
                fileWrite.write(termo + " 1\n")
    else :
        for termo in termos:
            fileWrite.write(termo + " 1\n")
    fileWrite.close()
    renome(nomeTemp,nomeReal)

def fazChain(texto):
    texto = texto.replace('\n',' ')
    texto = texto.replace('\t',' ')
    texto = texto.replace('“', ' " ')
    texto = texto.replace('”', ' " ')
    for spaced in ['.','-',',','!','?','(','—',')',':','...','..','/','\\']:
        texto = texto.replace(spaced, f' {spaced} ')
    palavras = texto.split()
    tamanhoTexto = len(palavras)
    listaDePares = []
    termo = " ".join(["¨" for a in range(TAMANHO)]+[palavras[0]])
    listaDePares.append(termo)
    for n in range(tamanhoTexto):
        termos = palavras[n : n + TAMANHO + 1]
        if len(termos) <= TAMANHO :
            while len(termos) <= TAMANHO :
                termos.append("¨")
            termo = " ".join(termos)
            listaDePares.append(termo)
            break
        termo = " ".join(termos)
        listaDePares.append(termo)
    return listaDePares

DIRECTORY = 'C:\\pythonscript\\artificialInteligence\\MarkovChainChat\\storying\\FanficAnime\\'
OVERFLOWLIMIT = 50000
TAMANHO = 1
termosTitulos = []
termosHistorias = []
total = len(os.listdir(DIRECTORY + "historias"))
quantia = 0
inicio = time()
for name in os.listdir(DIRECTORY + "historias"):
    quantia += 1
    file = open(DIRECTORY + 'historias//' + name)
    elementos = file.readline().split(" : ")
    if elementos[:-1]:
        titulo = " : ".join(elementos[:-1])
        termosTitulos += fazChain(titulo)
    if elementos[-1:][0]:
        historia = elementos[-1:][0]
        termosHistorias += fazChain(historia)
    file.close()
    if len(termosHistorias) > OVERFLOWLIMIT:
        alteraChainFile(termosTitulos,True)
        termosTitulos = []
        alteraChainFile(termosHistorias,False)
        termosHistorias = []
        final = time()
        duracao = (final - inicio)/quantia
        print(name)
        print("duração média : " + embelezeTempo(duracao))
        print("tempo Passado : " + embelezeTempo(final-inicio))
        print("falta : " + embelezeTempo(duracao*(total-quantia)))
        print()
print("concluindo...")
if len(termosTitulos) > OVERFLOWLIMIT:
    alteraChainFile(termosTitulos,True)
    termosTitulos = []
if len(termosHistorias) > OVERFLOWLIMIT:
    alteraChainFile(termosHistorias,False)
    termosHistorias = []
    final = time()
    duracao = (final - inicio)/total
    print("falta : " + embelezeTempo(duracao*(total-quantia)))
print()
