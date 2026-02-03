from PIL import Image
import os


def main() -> None:
    aImage = Image.open("b.jpg")
    width, height = aImage.size
    faixa = Image.new("RGB", (width, height), "white")
    for x in range(width):
        for y in range(height):
            pixelA = aImage.getpixel((x, y))
            vermelho = pixelA[0]
            verde = pixelA[1]
            azul = pixelA[2]
            if vermelho == verde:
                if vermelho == azul:
                    faixa.putpixel((x, y), (255, 255, 255))
                elif vermelho > azul:
                    faixa.putpixel((x, y), (255, 255, 0))
                else:
                    faixa.putpixel((x, y), (0, 0, 255))
            elif vermelho == azul:
                if vermelho > verde:
                    faixa.putpixel((x, y), (255, 0, 255))
                else:
                    faixa.putpixel((x, y), (0, 255, 0))
            elif verde == azul:
                if verde > vermelho:
                    faixa.putpixel((x, y), (0, 255, 255))
                else:
                    faixa.putpixel((x, y), (255, 0, 0))
            elif verde > azul:
                if verde > vermelho:
                    faixa.putpixel((x, y), (0, 255, 0))
                else:
                    faixa.putpixel((x, y), (255, 0, 0))
            elif azul > verde:
                if azul > vermelho:
                    faixa.putpixel((x, y), (0, 0, 255))
                else:
                    faixa.putpixel((x, y), (255, 0, 0))
            else:
                faixa.putpixel((x, y), (0, 0, 0))
    faixa.save("bContraste.jpg")
    print("veja")


if __name__ == "__main__":
    main()