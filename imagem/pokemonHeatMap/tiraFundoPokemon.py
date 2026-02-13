import os
from PIL import Image


def open_image_as_rgba(image_path: str) -> Image.Image:
    with Image.open(image_path) as image:
        image_in_memory = image.copy()
        if image.mode != "RGBA":
            return image_in_memory.convert("RGBA")
        return image_in_memory


def main() -> None:
    diretorio = os.getcwd()
    base = os.path.join(diretorio, "pokemon", "pokedexFeijao")
    imagens = os.listdir(base)
    imagensCaminho = [os.path.join(base, imagem) for imagem in imagens]
    imageNumber = 0
    for imagemCaminho in imagensCaminho:
        print(imagemCaminho)
        pokemon = open_image_as_rgba(imagemCaminho)
        largura, altura = pokemon.size
        corTransparente = pokemon.getpixel((0, 0))
        for y in range(96):
            for x in range(96):
                if pokemon.getpixel((x, y)) == corTransparente:
                    pokemon.putpixel((x, y), (0, 0, 0, 0))
        pokemon.save(
            os.path.join(
                diretorio, "pokemon", "pokedexSemFundo", f"pokemon{imageNumber:03d}.png"
            )
        )
        imageNumber += 1


if __name__ == "__main__":
    main()