from PIL import Image
import os


def main() -> None:
    directory = "C:\\pythonscript\\imagem\\evoluiPokemon\\"

    imagemInicial = Image.open(directory + "inicial.png")
    imagemFinal = Image.open(directory + "final.png")
    print("recolorindo...")

    inicialRecolor = Image.open(directory + "inicial.png")
    finalRecolor = Image.open(directory + "final.png")
    with open(directory + "config.txt", "r", encoding="utf-8") as file:
        linha = file.readline()
        while linha:
            coordInicial, coordFinal = [
                tuple([int(b) for b in coord.split(",")]) for coord in linha.split(" ")
            ]
            pixelFinal = imagemFinal.getpixel(coordFinal)
            pixelInicial = imagemInicial.getpixel(coordInicial)
            inicialRecolor.putpixel(coordInicial, pixelFinal)
            finalRecolor.putpixel(coordFinal, pixelInicial)
            linha = file.readline()

    inicialRecolor.save(directory + "inicialColored.png")
    finalRecolor.save(directory + "finalColored.png")
    inicialRecolor.close()
    finalRecolor.close()
    imagemInicial.close()
    imagemFinal.close()
    print("R E C O L O R I D O   :D")


if __name__ == "__main__":
    main()