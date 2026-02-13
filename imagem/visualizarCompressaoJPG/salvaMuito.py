from PIL import Image


def open_image_as_rgb(image_path: str) -> Image.Image:
    with Image.open(image_path) as image:
        image_in_memory = image.copy()
        if image.mode != "RGB":
            return image_in_memory.convert("RGB")
        return image_in_memory


def main() -> None:
    imagem = open_image_as_rgb("./pic0001.png")
    for a in range(1000):
        print(a)
        imagem.save("./pic0002.jpg")
        imagem = open_image_as_rgb("./pic0002.jpg")
        imagem.save("./pic0002.png")
        imagem = open_image_as_rgb("./pic0002.png")


if __name__ == "__main__":
    main()
