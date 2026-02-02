from PIL import Image
import imageio
from time import time


def pegaInteiro(
    mensagem: str, minimo: int | None = None, maximo: int | None = None
) -> int:
    while True:
        entrada = input(f"{mensagem} : ")
        try:
            valor = int(entrada)
            if (minimo is not None) and (valor < minimo):
                print(f"valor deve ser maior ou igual a {minimo}")
                continue
            if (maximo is not None) and (valor > maximo):
                print(f"valor deve ser menor ou igual a {maximo}")
                continue
            return valor
        except Exception as _:
            print("valor inválido, tente novamente")


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
    print(sign + ", ".join(parts))

def funcaoAfim(inicio,fim,total,n):
    elemento = []
    for elementoInicial, elementoFinal in zip(inicio, fim):
        B = elementoInicial
        A = (elementoFinal-elementoInicial)/(total+1)
        elemento.append(int(A*n+B))
    return tuple(elemento)

def verificaTamanho():
    with open("config.txt", "r", encoding="utf-8") as file:
        linha = file.readline()
        quantia = 0
        while(linha):
            quantia+=1
            linha = file.readline()
    return quantia

nomeFrame = "pokemon002{0:02d}.png"
quantiaFrames = 30#pegaInteiro("quantos frames?")
imagemInicial = Image.open("pokemon000.png")
imagemFinal = Image.open("pokemon001.png")
nomeFile = "partesConfig\\parte{0:02d}Config.txt"
imagemInicial.save(nomeFrame.format(0))
imagemFinal.save(nomeFrame.format(quantiaFrames+1))
print("\n tamanho: "+str(imagemInicial.size),end="\n\n")
for a in range(quantiaFrames):
    frame = Image.new("RGBA",imagemFinal.size,(255,255,255,0))
    frame.save(nomeFrame.format(a+1))
altura,largura = imagemFinal.size
tamanhoFile = verificaTamanho()
with open("config.txt", "r", encoding="utf-8") as file:
    linha = file.readline()
    firstTime = True
    inicioDef = time()
    while(linha):
        if(firstTime):
            inicio = time()
        coords = [tuple([int(b) for b in coord.split(",")]) for coord in linha.split(" ")]
        coordFinal = coords[1]
        pixelFinal = imagemFinal.getpixel(coordFinal)
        coordInicial = coords[0]
        pixelInicial = imagemInicial.getpixel(coordInicial)
        for n in range(quantiaFrames):
            frame = Image.open(nomeFrame.format(n+1))
            novaCoord = funcaoAfim(coordInicial,coordFinal,quantiaFrames,n+1)
            novaCor = funcaoAfim(pixelInicial,pixelFinal,quantiaFrames,n+1)
            frame.putpixel(novaCoord,novaCor)
            frame.save(nomeFrame.format(n+1))
            frame.close()
        linha = file.readline()
        if(firstTime):
            fim = time()
            duracao = fim-inicio
            print("são "+str(tamanhoFile)+" transformações")
            print_elapsed_time(duracao)
            print_elapsed_time(duracao*tamanhoFile)
            fim,inicio,duracao,tamanhoFile = [None,None,None,None]
            firstTime = False
with imageio.get_writer("bulbasaurEvolve.gif", mode="I") as writer:
    for n in range(quantiaFrames):
        imagem = imageio.imread(nomeFrame.format(n))
        writer.append_data(imagem)
fimDef = time()
imagemInicial.close()
imagemFinal.close()
print("\nfinalizado")
print_elapsed_time(fimDef-inicioDef)
