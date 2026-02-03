from PIL import Image,ImageGrab


def main() -> None:
    im = ImageGrab.grabclipboard()
    im.save("screen.png")
    im.close()
    img = Image.open("screen.png")
    print("0 - 9X9")
    print("1 - 16X16")
    print("2 - 16X30")
    modo = input()
    if modo == "0":
        inicio = (436,133)
        multX = 9
        multY = 9
        add = 55
    elif modo == "1":
        inicio = (400, 99)
        multX = 16
        multY = 16
        add = 35
    else:
        inicio = (154, 99)
        multX = 30
        multY = 16
        add = 35
    matrix = []
    for linha in range(multX):
        matrix.append([])
        for coluna in range(multY):
            matrix[linha].append(9)
    for a,X in enumerate(range(inicio[0],inicio[0]+multX*add,add)):
        for b,Y in enumerate(range(inicio[1],inicio[1]+multY*add,add)):
            soma = [0,0,0]
            for x in range(X,X+add):
                for y in range(Y,Y+add):
                    pixel = img.getpixel((x,y))
                    for i in range(3):
                        soma[i] += pixel[i]
            pixelMedio = []
            for i in range(3):
                pixelMedio.append(soma[i]/(add**2))
            matrix[a][b] = pixelMedio
            print(matrix[a][b])
        print()


if __name__ == "__main__":
    main()