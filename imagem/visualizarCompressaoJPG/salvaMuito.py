from PIL import Image


def main() -> None:
    imagem = Image.open("C:\\pythonscript\\imagem\\visualizarCompressaoJPG\\pic0001.png")
    for a in range(1000):
        print(a)
        imagem = imagem.convert("RGB")
        imagem.save("C:\\pythonscript\\imagem\\visualizarCompressaoJPG\\pic0002.jpg")
        imagem.close()
        imagem = Image.open("C:\\pythonscript\\imagem\\visualizarCompressaoJPG\\pic0002.jpg")
        imagem.save("C:\\pythonscript\\imagem\\visualizarCompressaoJPG\\pic0002.png")
        imagem.close()
        imagem = Image.open("C:\\pythonscript\\imagem\\visualizarCompressaoJPG\\pic0002.png")
    imagem.close()


if __name__ == "__main__":
    main()