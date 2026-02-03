from PIL import Image


def main() -> None:
    vermelho = (255, 0, 0, 255)
    azul = (0, 0, 255, 255)
    preto = (0, 0, 0, 255)
    cores = (vermelho, azul, preto)

    for numeroCurva in range(0, 11):
        nome = "curva" + str(numeroCurva) + ".png"
        img = Image.open(nome)
        larg, alt = img.size
        cont = 0
        area = larg * alt
        for x in range(larg):
            for y in range(alt):
                if img.getpixel((x, y)) in cores:
                    cont += 1
        print(
            "\nnivel:"
            + str(numeroCurva)
            + "\ntotal:"
            + str(area)
            + "\nquant:"
            + str(cont)
            + "\nporcentagem:"
            + str(cont * 100 / area)
            + "%\n"
        )


if __name__ == "__main__":
    main()