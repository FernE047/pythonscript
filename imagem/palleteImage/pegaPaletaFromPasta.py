from PIL import Image
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
    imagens = get_image_from_folder("pokedex sem fundo")
    paleta = []
    for img in imagens:
        imagem = open_image_as_rgba(img)
        largura, altura = imagem.size
        for x in range(largura):
            for y in range(altura):
                pixel = imagem.getpixel((x, y))
                if pixel not in paleta:
                    paleta.append(pixel)
    altura = int(len(paleta) / 256) + 1
    if altura > 1:
        paletaImg = Image.new("RGBA", (256, altura), (0, 0, 0, 0))
    else:
        paletaImg = Image.new("RGBA", (len(paleta), altura), (0, 0, 0, 0))
    m = 0
    for index in range(len(paleta)):
        if m % 256 == 0:
            m = 0
        paletaImg.putpixel((m, int(index / 256)), paleta[index])
        m += 1
    paletaImg.save(os.path.join("paleta", "paletaPokemons.png"))


if __name__ == "__main__":
    main()
