from PIL import Image
from time import time
import os
import multiprocessing


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


def funcaoCor(inicio, fim, total, n):
    elemento = []
    for elementoInicial, elementoFinal in zip(inicio, fim):
        B = elementoInicial
        A = (elementoFinal - elementoInicial) / (total + 1)
        elemento.append(int(A * n + B))
    return tuple(elemento)


def funcaoCoord(inicio, fim, total, n):
    elemento = []
    for elementoInicial, elementoFinal in zip(inicio, fim):
        B = elementoInicial
        A = (elementoFinal - elementoInicial) / (total + 1)
        elemento.append(int(A * n + B))
    return tuple(elemento)


def makeFrame(args):
    n, total = args
    imagemInicial = Image.open("C:\\pythonscript\\imagem\\evoluiPokemon\\inicial.png")
    imagemFinal = Image.open("C:\\pythonscript\\imagem\\evoluiPokemon\\final.png")
    print("Fazendo Frame : " + str(n))
    frame = Image.new("RGBA", imagemFinal.size, (255, 255, 255, 0))
    with open("C:\\pythonscript\\imagem\\evoluiPokemon\\config.txt", "r", encoding="utf-8") as file:
        linha = file.readline()
        while linha:
            if linha.find("fundo") != -1:
                coord = tuple([int(b) for b in linha[:-6].split(",")])
                frame.putpixel(coord, imagemInicial.getpixel(coord))
            else:
                coords = [
                    tuple([int(b) for b in coord.split(",")]) for coord in linha.split(" ")
                ]
                coordFinal = coords[1]
                pixelFinal = imagemFinal.getpixel(coordFinal)
                coordInicial = coords[0]
                pixelInicial = imagemInicial.getpixel(coordInicial)
                novaCoord = funcaoCoord(coordInicial, coordFinal, total, n + 1)
                novaCor = funcaoCor(pixelInicial, pixelFinal, total, n + 1)
                frame.putpixel(novaCoord, novaCor)
            linha = file.readline()
    print("\tFrame Terminado : " + str(n))
    frame.save(f"C:\\pythonscript\\imagem\\evoluiPokemon\\frames\\frame{n + 1:03d}.png")
    imagemInicial.close()
    imagemFinal.close()
    frame.close()


if __name__ == "__main__":
    quantiaFrames = 30  # pegaInteiro("quantos frames?")
    nomeFrame = "C:\\pythonscript\\imagem\\evoluiPokemon\\frames\\frame{0:03d}.png"

    imagemInicial = Image.open("C:\\pythonscript\\imagem\\evoluiPokemon\\inicial.png")
    imagemFinal = Image.open("C:\\pythonscript\\imagem\\evoluiPokemon\\final.png")
    imagemInicial.save(nomeFrame.format(0))
    imagemFinal.save(nomeFrame.format(quantiaFrames + 1))
    imagemInicial.close()
    imagemFinal.close()

    print("\n tamanho: " + str(imagemInicial.size), end="\n\n")
    p = multiprocessing.Pool(os.cpu_count())
    p.map(makeFrame, [[a, quantiaFrames] for a in range(quantiaFrames)])
