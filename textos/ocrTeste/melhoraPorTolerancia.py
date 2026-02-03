from PIL import Image
import os


def main() -> None:
    nome = "PAPPDF\\PDFJaFeitos\\pasadeira Croche Candy\\2016-12-07-10-11-54.jpg"
    print(nome)
    imagem = Image.open(nome)
    width, height = imagem.size
    imagemNew = imagem.copy()
    tolerancia = 20
    for x in range(width):
        for y in range(height):
            pixel = imagem.getpixel((x, y))
            teste = pixel[0] + pixel[1] + pixel[2]
            if teste >= (255 * 3 - tolerancia):
                imagemNew.putpixel((x, y), (0, 0, 0))
            else:
                imagemNew.putpixel((x, y), (255, 255, 255))
    imagemNew.save("pictureTolerancia.jpg")


if __name__ == "__main__":
    main()