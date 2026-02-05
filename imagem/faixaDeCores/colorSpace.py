from PIL import Image

MAXIMUM_COLOR_VALUE = 256
MAXIMUM_COLOR_SIZE = (MAXIMUM_COLOR_VALUE, MAXIMUM_COLOR_VALUE)


def main() -> None:
    for z in range(MAXIMUM_COLOR_VALUE):
        red_layer = Image.new("RGB", MAXIMUM_COLOR_SIZE, "white")
        green_layer = Image.new("RGB", MAXIMUM_COLOR_SIZE, "white")
        blue_layer = Image.new("RGB", MAXIMUM_COLOR_SIZE, "white")
        for x in range(MAXIMUM_COLOR_VALUE):
            for y in range(MAXIMUM_COLOR_VALUE):
                coord = (x, y)
                red_layer.putpixel(coord, (z, x, y))
                green_layer.putpixel(coord, (y, z, x))
                blue_layer.putpixel(coord, (x, y, z))
        red_layer.save(f"out/red/rgb_layer_{z:03d}.jpg")
        green_layer.save(f"out/green/rgb_layer_{z:03d}.jpg")
        blue_layer.save(f"out/blue/rgb_layer_{z:03d}.jpg")
        print(z)
    print("Done!!!")


if __name__ == "__main__":
    main()
