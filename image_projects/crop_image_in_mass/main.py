from pathlib import Path
from PIL import Image


def open_image(image_path: Path) -> Image.Image:
    with Image.open(image_path) as image:
        image_in_memory = image.copy()
        return image_in_memory


def main() -> None:
    diretorio = Path.cwd()
    base = diretorio / "imagensBase"
    imagensCaminho = [imagem for imagem in base.iterdir() if imagem.is_file()]
    imageNumber = 0
    output_folder = diretorio / "pokemon"
    output_folder.mkdir(exist_ok=True)
    for imagemCaminho in imagensCaminho:
        print(imagemCaminho)
        imagem = open_image(imagemCaminho)
        largura, altura = imagem.size
        for y in range(int(altura / 103)):
            for x in range(int(largura / 96)):
                pokemon = imagem.crop((96 * x, 103 * y, 96 * (x + 1), 103 * y + 96))
                pokemon.save(output_folder / f"pokemon{imageNumber:03d}.png")
                imageNumber += 1


if __name__ == "__main__":
    main()
