from PIL import Image

SOURCE_IMAGE = "./source.png"
TARGET_IMAGE = "./target.png"
SOURCE_IMAGE_COLORED = "./source_colored.png"
TARGET_IMAGE_COLORED = "./target_colored.png"
CONFIG_FILE = "./config.txt"


def open_image_as_rgba(image_path: str) -> Image.Image:
    with Image.open(image_path) as image:
        image_in_memory = image.copy()
        if image.mode != "RGBA":
            return image_in_memory.convert("RGBA")
        return image_in_memory


def main() -> None:
    source_image = open_image_as_rgba(SOURCE_IMAGE)
    target_image = open_image_as_rgba(TARGET_IMAGE)
    print("recolorindo...")
    source_image_colored = source_image.copy()
    target_image_colored = target_image.copy()
    with open(CONFIG_FILE, "r", encoding="utf-8") as file:
        lines = file.readlines()
    for line in lines:
        line = line.strip()
        if not line:
            continue
        coords: list[tuple[int, ...]] = [
            tuple([int(b) for b in coord.split(",")]) for coord in line.split(" ")
        ]
        coord_source, coord_target = coords
        if len(coord_source) != 2 or len(coord_target) != 2:
            raise ValueError(f"Invalid coordinate format: {line}")
        pixel_target = target_image.getpixel(coord_target)
        if pixel_target is None:
            raise ValueError(f"Pixel not found at coordinate: {coord_target}")
        pixel_source = source_image.getpixel(coord_source)
        if pixel_source is None:
            raise ValueError(f"Pixel not found at coordinate: {coord_source}")
        source_image_colored.putpixel(coord_source, pixel_target)
        target_image_colored.putpixel(coord_target, pixel_source)
    source_image_colored.save(SOURCE_IMAGE_COLORED)
    target_image_colored.save(TARGET_IMAGE_COLORED)
    print("R E C O L O R I D O   :D")


if __name__ == "__main__":
    main()
