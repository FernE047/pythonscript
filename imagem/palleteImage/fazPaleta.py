from PIL import Image
import os


def main() -> None:
    imagem=Image.new("RGBA",(16,16),(0,0,0,0))
    imagem.save(os.path.join("paleta","paletaBW4.png"))
    for x in range(256):
        y=int(x/16)
        cor=tuple([x for a in range(3)]+[255])
        print(cor)
        imagem.putpixel((x%16,y),cor)
    imagem.save(os.path.join("paleta","paletaBW4.png"))


if __name__ == "__main__":
    main()