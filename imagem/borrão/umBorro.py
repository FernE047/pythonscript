from PIL import Image


def naoTemZero(lista):
    for a in lista:
        if a != 0:
            return 1
    return 0


def somaLista(lista):
    soma = 0
    for a in lista:
        soma = soma + a
    return soma


def quaisTemVizinhos(img):
    tamanho = img.size[0]
    temVizinhos = []
    for x in range(tamanho):
        for y in range(tamanho):
            if img.getpixel((x, y))[1] == 255:
                direcoes = [0, 0, 0, 0]
                if x == 0:
                    direcoes[0] = 0
                else:
                    direcoes[0] = 255 - img.getpixel((x - 1, y))[1]
                if x == tamanho - 1:
                    direcoes[1] = 0
                else:
                    direcoes[1] = 255 - img.getpixel((x + 1, y))[1]
                if y == 0:
                    direcoes[2] = 0
                else:
                    direcoes[2] = 255 - img.getpixel((x, y - 1))[1]
                if y == tamanho - 1:
                    direcoes[3] = 0
                else:
                    direcoes[3] = 255 - img.getpixel((x, y + 1))[1]
                if naoTemZero(direcoes):
                    valor = 255 - somaLista(direcoes)
                    temVizinhos.append(((x, y), valor))
    return temVizinhos



def main() -> None:
    borro = Image.new("RGBA", (11, 11), (255, 255, 255, 255))
    borro.putpixel((5, 5), (254, 254, 254, 255))
    while borro.getpixel((0, 0))[1] == 255:
        informacoes = quaisTemVizinhos(borro)
        for infoImportante in informacoes:
            posicao, cor = infoImportante
            borro.putpixel(posicao, (cor, cor, cor, 255))
    borro.save("borro.png")


if __name__ == "__main__":
    main()