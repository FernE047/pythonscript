from PIL import Image, ImageDraw
import os
import gc


def quaoBranco(img, tenta=1):
    imagem = Image.open(img)
    width, height = imagem.size
    tamanho = width * height
    print(tamanho)
    grafico = False
    while not (grafico):
        try:
            grafico = Image.new(
                "RGBA", (int(tamanho / tenta), 255 * 3), (255, 255, 255, 255)
            )
        except:
            grafico = False
            tenta *= 10
    momento = 0
    tolerancias = [0 for i in range(255 * 3)]
    for x in range(width):
        for y in range(height):
            pixel = imagem.getpixel((x, y))
            teste = pixel[0] + pixel[1] + pixel[2]
            if momento % 1000 == 0:
                print(str(momento))
            for index in range(255 * 3):
                if teste >= 255 * 3 - index:
                    tolerancias[255 * 3 - index] += 1
            momento += 1
    for index in range(len(tolerancias)):
        if index % 10 == 0:
            print(str(index))
        tolerancia = tolerancias[index]
        for x in range(tolerancia):
            grafico.putpixel((x, index), (0, 0, 0, 255))
    return grafico



def main() -> None:
    assunto = "ds rom"
    pastaImagens = os.path.join("C:\\", "pythonscript", "Imagens", assunto)
    print(pastaImagens)
    imagens = os.listdir(pastaImagens)
    try:
        pastaSalva = os.path.join(os.getcwd(), assunto + "Grafico")
        os.makedirs(pastaSalva)
    except:
        True
    for imagem in imagens:
        grafico = quaoBranco(
            os.path.join("C:\\", "pythonscript", "Imagens", assunto, imagem)
        )
        grafico.save(os.path.join(pastaSalva, imagem[:-4] + "Graf" + imagem[-4:]))
    print(gc.collect())

    # implementar rotação, corte, e resize


if __name__ == "__main__":
    main()