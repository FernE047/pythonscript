from PIL import Image


def main() -> None:
    nomeOpen = "A{0:03d}.png"
    nomeSave = "A{0:03d}{1:01d}.png"
    for a in range(2):
        imagem = Image.open(nomeOpen.format(a))
        altura, largura = imagem.size
        print(
            "\nimagem " + nomeOpen.format(a) + " tamanho: " + str(imagem.size), end="\n\n"
        )
        for bit in range(1, 8):
            imagemTransform = Image.new("RGBA", imagem.size)
            divisor = 256 / 2**bit
            multiplicador = 255 / ((2**bit) - 1)
            for y in range(altura):
                for x in range(largura):
                    pixelVelho = imagem.getpixel((y, x))
                    pixelNovo = list(pixelVelho)
                    for n in range(3):
                        pixelNovo[n] = int((pixelVelho[n] // divisor) * multiplicador)
                    imagemTransform.putpixel((y, x), tuple(pixelNovo))
            imagemTransform.save(nomeSave.format(a, bit))
            imagemTransform.close()
            print("finalizado " + nomeSave.format(a, bit))
        imagem.close()


if __name__ == "__main__":
    main()