from PIL import Image
import cv2
import os


def main() -> None:
    os.chdir("camadas")
    for z in range(256):
        camadaR = Image.new("RGB", (256, 256), "white")
        camadaG = Image.new("RGB", (256, 256), "white")
        camadaB = Image.new("RGB", (256, 256), "white")
        for x in range(256):
            for y in range(256):
                camadaR.putpixel((x, y), (z, x, y))
                camadaG.putpixel((x, y), (y, z, x))
                camadaB.putpixel((x, y), (x, y, z))
        camadaR.save("R\\a" + str(z) + ".jpg")
        camadaG.save("G\\a" + str(z) + ".jpg")
        camadaB.save("B\\a" + str(z) + ".jpg")
        print(z)
    print("veja")


if __name__ == "__main__":
    main()