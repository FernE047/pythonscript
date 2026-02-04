from PIL import Image
import os


def get_image_from_folder(image_category: str, quantity: int = 1) -> list[str]:
    folder = f"imagens/{image_category}"
    images: list[str] = []
    if os.path.exists(folder):
        for file_name in os.listdir(folder):
            if file_name.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif")):
                images.append(os.path.join(folder, file_name))
                if len(images) >= quantity:
                    break
    return images


def main() -> None:
    print("digite um assunto")
    assunto = input()
    print("quantia")
    quantia = input()
    if quantia == "":
        imagens = get_image_from_folder(assunto)
    else:
        quantia = int(quantia)
        imagens = get_image_from_folder(assunto, quantia)
    niveis = [" ", "`", ".", ",", "+", "%", "@", "#"]
    print("tamanho")
    print("165 - max")
    print("075 - min")
    print("060 - terminal")
    print("026 - whats")
    tamanho = input()
    if tamanho == "whats":
        showLargura = 26
    elif tamanho == "max":
        showLargura = 165
    elif tamanho == "min":
        showLargura = 75
    elif tamanho == "terminal":
        showLargura = 60
    else:
        showLargura = int(tamanho)
    for imagem in imagens:
        print("\n" + imagem + "\n")
        imagemColor = Image.open(imagem)
        imagemBW = imagemColor.convert("L")
        largura, altura = imagemBW.size
        if largura > showLargura:
            aspectRatio = showLargura / largura
            showAltura = int(altura * aspectRatio)
            imagemShow = imagemBW.resize((showLargura, showAltura))
        else:
            imagemShow = imagemBW
        largura, altura = imagemShow.size
        for y in range(altura):
            linha = ""
            for x in range(largura):
                pixel = imagemShow.getpixel((x, y))
                linha += niveis[int(pixel / 32) - 1]
            print(linha)
        tamanho = input()


if __name__ == "__main__":
    main()
