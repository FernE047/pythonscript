from PIL import Image
from pathlib import Path


def open_image_as_rgb(image_path: Path) -> Image.Image:
    with Image.open(image_path) as image:
        image_in_memory = image.copy()
        if image.mode != "RGB":
            return image_in_memory.convert("RGB")
        return image_in_memory


def main() -> None:
    pic_1_path = Path("pic0001.png")
    pic_2 = Path("pic0002")
    jpg_path = pic_2.with_suffix(".jpg")
    png_path = pic_2.with_suffix(".png")
    imagem = open_image_as_rgb(pic_1_path)
    for a in range(1000):
        print(a)
        imagem.save(jpg_path)
        imagem = open_image_as_rgb(jpg_path)
        imagem.save(png_path)
        imagem = open_image_as_rgb(png_path)


if __name__ == "__main__":
    main()
