from PIL import Image
import pastaImagens
import os


def get_image_from_folder(image_category: str) -> list[str]:
    folder = f"imagens/{image_category}"
    images: list[str] = []
    if os.path.exists(folder):
        for file_name in os.listdir(folder):
            if file_name.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif")):
                images.append(os.path.join(folder, file_name))
    return images


def main() -> None:
    casos=[3,4,5]
    divisor=50
    assunto="DsRom"
    imagens=get_image_from_folder(assunto)
    for numero,imgName in enumerate(imagens):
        print(imgName)
        imagem=Image.open(imgName)
        tamanho=imagem.size
        for x in range(tamanho[0]):
            for y in range(tamanho[1]):
                if((x%divisor not in casos)and(y%divisor not in casos)):
                    cor=imagem.getpixel((x,y))
                    cor=tuple(3*[int((cor[0]+cor[1]+cor[2])/3)]+[255])
                    imagem.putpixel((x,y),cor)
        pastaImagens.salva(f"{numero:03d}-"+assunto,imagem,pasta=["Pbillusion",assunto],extensao=".png")
        print(f"{numero:03d}-"+assunto+" imagem concluida")


if __name__ == "__main__":
    main()