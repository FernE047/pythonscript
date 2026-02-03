import os
from PIL import Image


def main() -> None:
    diretorio = os.getcwd()
    base = os.path.join(diretorio, "imagensBase")
    imagens = os.listdir(base)
    imagensCaminho = [os.path.join(base, imagem) for imagem in imagens]
    imageNumber = 0
    for imagemCaminho in imagensCaminho:
        print(imagemCaminho)
        imagem = Image.open(imagemCaminho)
        largura, altura = imagem.size
        for y in range(int(altura / 103)):
            for x in range(int(largura / 96)):
                pokemon = imagem.crop((96 * x, 103 * y, 96 * (x + 1), 103 * y + 96))
                pokemon.save(
                    os.path.join(diretorio, "pokemon", f"pokemon{imageNumber:03d}.png")
                )
                imageNumber += 1


if __name__ == "__main__":
    main()