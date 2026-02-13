from PIL import Image
from colorsys import rgb_to_hsv
from colorsys import hsv_to_rgb
from os import mkdir


def open_image_as_rgba(image_path: str) -> Image.Image:
    with Image.open(image_path) as image:
        image_in_memory = image.copy()
        if image.mode != "RGBA":
            return image_in_memory.convert("RGBA")
        return image_in_memory


def main() -> None:
    nomeOpen = "pokedexSemFundo\\pokemon{0:03d}.png"
    pasta = "pokedexRecolorPokemons\\pokemon{0:03d}"
    nomeSave = "pokedexRecolorPokemons\\pokemon{0:03d}\\pokemon{0:03d}{1:02d}.png"
    for a in range(762):
        imagem = open_image_as_rgba(nomeOpen.format(a))
        altura, largura = imagem.size
        mkdir(pasta.format(a))
        for b in range(12):
            imagemTransform = Image.new("RGBA", imagem.size, (255, 255, 255, 0))
            for y in range(altura):
                for x in range(largura):
                    pixelRGB = imagem.getpixel((y, x))
                    if pixelRGB[3] == 0:
                        continue
                    pixelHSV = rgb_to_hsv(pixelRGB[0], pixelRGB[1], pixelRGB[2])
                    novoPixelHSV = list(pixelHSV)
                    novoPixelHSV[0] = novoPixelHSV[0] + b / 12
                    novoPixelHSV[0] -= novoPixelHSV[0] // 1
                    novoPixelRGB = hsv_to_rgb(
                        novoPixelHSV[0], novoPixelHSV[1], novoPixelHSV[2]
                    )
                    novoPixelRGB = tuple([int(n) for n in novoPixelRGB])
                    imagemTransform.putpixel((y, x), novoPixelRGB)
            imagemTransform.save(nomeSave.format(a, b))


if __name__ == "__main__":
    main()