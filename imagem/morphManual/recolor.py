from PIL import Image
import os

SOURCE_IMAGE = "./inicial.png"
TARGET_IMAGE = "./final.png"
CONFIG_FOLDER = "./partes/config/"


def main() -> None:

    source_image = Image.open(SOURCE_IMAGE)
    target_image = Image.open(TARGET_IMAGE)
    print("recoloring...")

    source_recolor = source_image.copy()
    target_recolor = target_image.copy()
    for fileName in os.listdir(CONFIG_FOLDER):
        with open(os.path.join(CONFIG_FOLDER, fileName), "r", encoding="utf-8") as file:
            lines = file.readlines()
        for line in lines:
            coords_str = line.split(" ")
            source_coords_str = coords_str[0].split(",")
            target_coords_str = coords_str[1].split(",")
            coord_source = (int(source_coords_str[0]), int(source_coords_str[1]))
            coord_target = (int(target_coords_str[0]), int(target_coords_str[1]))
            pixel_target = target_image.getpixel(coord_target)
            if pixel_target is None:
                continue
            pixel_source = source_image.getpixel(coord_source)
            if pixel_source is None:
                continue
            source_recolor.putpixel(coord_source, pixel_target)
            target_recolor.putpixel(coord_target, pixel_source)

    source_recolor_name = SOURCE_IMAGE.replace(".png", "_colored.png")
    target_recolor_name = TARGET_IMAGE.replace(".png", "_colored.png")
    source_recolor.save(source_recolor_name)
    target_recolor.save(target_recolor_name)
    for image in (source_recolor, target_recolor, source_image, target_image):
        image.close()
    print("R E C O L O R E D   :D")


if __name__ == "__main__":
    main()
