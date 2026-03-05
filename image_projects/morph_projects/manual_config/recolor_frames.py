from pathlib import Path

from PIL import Image

SOURCE_IMAGE = Path("inicial.png")
TARGET_IMAGE = Path("final.png")
CONFIG_FOLDER = Path("partes") / "config"


def open_image_as_rgba(image_path: Path) -> Image.Image:
    with Image.open(image_path) as image:
        image_in_memory = image.copy()
        if image.mode != "RGBA":
            return image_in_memory.convert("RGBA")
        return image_in_memory


def recolor_frames() -> None:

    source_image = open_image_as_rgba(SOURCE_IMAGE)
    target_image = open_image_as_rgba(TARGET_IMAGE)
    print("recoloring...")

    source_recolor = source_image.copy()
    target_recolor = target_image.copy()
    for fileName in CONFIG_FOLDER.iterdir():
        with open(fileName, "r", encoding="utf-8") as file:
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

    source_recolor_name = SOURCE_IMAGE.with_suffix("_colored.png")
    target_recolor_name = TARGET_IMAGE.with_suffix("_colored.png")
    source_recolor.save(source_recolor_name)
    target_recolor.save(target_recolor_name)
    print("R E C O L O R E D   :D")