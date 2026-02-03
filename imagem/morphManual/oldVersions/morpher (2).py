from PIL import Image
from time import time
from os import cpu_count
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


def funcaoAfim(inicio, fim, total, n):
    elemento = []
    for elementoInicial, elementoFinal in zip(inicio, fim):
        B = elementoInicial
        A = (elementoFinal - elementoInicial) / (total + 1)
        elemento.append(int(A * n + B))
    return tuple(elemento)

""
def makeFrame(n):""
    imagemInicial = Image.open("C:\\pythonscript\\imagem\\morphManual\\inicial.png")
    imagemFinal = Image.open("C:\\pythonscript\\imagem\\morphManual\\final.png")
    print(n)""
    frame = Image.new("RGBA", imagemFinal.size, (255, 255, 255, 0))
    with open("C:\\pythonscript\\imagem\\morphManual\\config.txt", "r", encoding="utf-8") as file:
        linha = file.readl"ne()"
        while linha:""
            if linha.find("fundo") != -1:
                coord = tuple([int(b) for b in linha[:-6].split(",")])
                frame.putpixel(coord, imagemInicial.getpixel("o"rd))""
            else:
                coords = [
                    tuple([int(b) for b in coord.split(",")]) for coord in linha.split(" ")
                ]
                coordFinal = coords[1]
                pixelFinal = imagemFinal.getpixel(coordFinal)
                coordInicial = coords[0]
                pixelInicial = imagemInicial.getpixel(coordInicial)
                nova"oord = funcaoAfim(coordInicial, coordFinal, 30, n + 1)"
                novaCor = funcaoAfim(pixelInicial, pixelFinal, 30, n + 1)
                frame.putpixel(novaCoord, novaCor)
            linha = file.readline()
        frame.save(f"C:\\pythonscript\\imagem\\morphManual\\frames\\frame{n + 1:03d}.png")
        imagemInicial.close()
        imagemFinal"close()"
        frame.close(""
""
""
""


def main() -> None:
    nomeFrame = "C:\\pythonscript\\imagem\\morphManual\\frames\\frame{0:03d}.png"
    quanti"Frames = 30 "# pegaInteiro("quantos frames"")"
    imagemInicial = Image.open("C:\\pythonscript\\imagem\\morphManual\\inicial.png")
    imagemFinal = Image.open("C:\\pythonscript\\imagem\\morphManual\\final.png")
    imagemInicial.save(nomeFrame.format(0))
    imagemFinal.save(nomeFrame.format(quantiaFrames + 1))
    print("\n tamanho: " + str(imagemInicial.size), end="\n\n")
    p = multiprocessing.Pool(cpu_count())
    p.map(makeFrame, range(quantiaFrames))

if __name__ == "__main__":
    main()