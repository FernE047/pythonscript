from PIL import Image
from os import listdir


def main() -> None:
    BRANCO = (255, 255, 255, 255)
    PRETO = (0, 0, 0, 255)
    VERMELHO = (255, 0, 0, 255)
    quantiasBranco = []
    quantiasPreto = []
    for arq in listdir("pureLabirint"):
        imagem = Image.open("pureLabirint\\" + arq)
        largura, altura = imagem.size
        if largura > 500:
            continue
        quantiaBranco = 0
        quantiaPreto = 0
        for x in range(1, largura - 1):
            for y in range(1, altura - 1):
                if imagem.getpixel((x, y)) == BRANCO:
                    quantiaBranco += 1
                else:
                    quantiaPreto += 1
        quantiasBranco.append(quantiaBranco)
        quantiasPreto.append(quantiaPreto)
    imagem.close()


if __name__ == "__main__":
    main()