from PIL import Image


def open_image_as_rgba(image_path: str) -> Image.Image:
    with Image.open(image_path) as image:
        image_in_memory = image.copy()
        if image.mode != "RGBA":
            return image_in_memory.convert("RGBA")
        return image_in_memory


def main() -> None:
    vermelho = (255, 0, 0, 255)
    azul = (0, 0, 255, 255)
    preto = (0, 0, 0, 255)
    cores = (vermelho, azul, preto)

    for numeroCurva in range(0, 11):
        nome = "curva" + str(numeroCurva) + ".png"
        img = open_image_as_rgba(nome)
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