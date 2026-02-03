from PIL import Image


def compara(pixelA, pixelB):
    soma = 0
    for a in range(3):
        soma += abs(pixelA[a] - pixelB[a]) ** 2
    return soma**0.5



def main() -> None:
    nomeOpen = "A{0:03d}0.jpg"
    nomeSave = "A{0:03d}{1:01d}.png"
    for a in range(2):
        imagem = Image.open(nomeOpen.format(a))
        altura, largura = imagem.size
        print(
            "\nimagem " + nomeOpen.format(a) + " tamanho: " + str(imagem.size), end="\n\n"
        )
        imagemTransform = Image.new("RGBA", imagem.size, (255, 255, 255, 255))
        for y in range(altura):
            for x in range(largura):
                pixelAtual = imagem.getpixel((y, x))
                soma = []
                if x > 0:
                    soma.append(compara(imagem.getpixel((y, x - 1)), pixelAtual))
                if x < largura - 1:
                    soma.append(compara(imagem.getpixel((y, x + 1)), pixelAtual))
                if y > 0:
                    soma.append(compara(imagem.getpixel((y - 1, x)), pixelAtual))
                if y < altura - 1:
                    soma.append(compara(imagem.getpixel((y + 1, x)), pixelAtual))
                cor = int(sum(soma) / len(soma) * -255 / 442 + 255)
                imagemTransform.putpixel((y, x), (cor, cor, cor, 255))
        imagemTransform.save(nomeSave.format(a, 6))
        imagemTransform.close()
        print("finalizado " + nomeSave.format(a, 6))
        imagem.close()


if __name__ == "__main__":
    main()