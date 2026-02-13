from PIL import Image
import pastaImagens
import os


def get_image_from_folder(image_category: str) -> list[str]:
    folder = f"imagens/{image_category}"
    images: list[str] = []
    if os.path.exists(folder):
        for filename in os.listdir(folder):
            if filename.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif")):
                images.append(os.path.join(folder, filename))
    return images


def open_image_as_rgba(image_path: str) -> Image.Image:
    with Image.open(image_path) as image:
        image_in_memory = image.copy()
        if image.mode != "RGBA":
            return image_in_memory.convert("RGBA")
        return image_in_memory


def main() -> None:
    casos = [3, 4, 5]
    divisor = 50
    assunto = "DsRom"
    imagens = get_image_from_folder(assunto)
    for numero, imgName in enumerate(imagens):
        print(imgName)
        imagem = open_image_as_rgba(imgName)
        tamanho = imagem.size
        for x in range(tamanho[0]):
            for y in range(tamanho[1]):
                if (x % divisor not in casos) and (y % divisor not in casos):
                    cor = imagem.getpixel((x, y))
                    cor = tuple(3 * [int((cor[0] + cor[1] + cor[2]) / 3)] + [255])
                    imagem.putpixel((x, y), cor)
        pastaImagens.salva(
            f"{numero:03d}-" + assunto,
            imagem,
            pasta=["Pbillusion", assunto],
            extensao=".png",
        )
        print(f"{numero:03d}-" + assunto + " imagem concluida")


if __name__ == "__main__":
    main()
