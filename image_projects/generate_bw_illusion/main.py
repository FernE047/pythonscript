from PIL import Image
import os

IMAGES_FOLDER = "imagens"
ALLOWED_IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".bmp", ".gif")
EXCLUDED_DIVISORS = (3, 4, 5)
STEP = 50

PixelData = tuple[int, ...]
CoordData = tuple[int, int]


def get_pixel(image: Image.Image, coord: CoordData) -> PixelData:
    pixel = image.getpixel(coord)
    if pixel is None:
        raise ValueError("Pixel not found")
    if isinstance(pixel, int):
        raise ValueError("Image is not in RGB mode")
    if isinstance(pixel, float):
        raise ValueError("Image is not in RGB mode")
    if len(pixel) < 4:
        raise ValueError("Image is not in RGB mode")
    return pixel


def get_image_from_folder(sub_folder: str) -> list[str]:
    folder = f"{IMAGES_FOLDER}/{sub_folder}"
    images: list[str] = []
    if os.path.exists(folder):
        for filename in os.listdir(folder):
            if filename.lower().endswith(ALLOWED_IMAGE_EXTENSIONS):
                images.append(os.path.join(folder, filename))
    return images


def open_image_as_rgba(image_path: str) -> Image.Image:
    with Image.open(image_path) as image:
        image_in_memory = image.copy()
        if image.mode != "RGBA":
            return image_in_memory.convert("RGBA")
        return image_in_memory


def main() -> None:
    sub_folder = "Luigi_Mansion_3"
    images = get_image_from_folder(sub_folder)
    for image_index, image_name in enumerate(images):
        print(image_name)
        image = open_image_as_rgba(image_name)
        image_size = image.size
        for x in range(image_size[0]):
            for y in range(image_size[1]):
                if x % STEP in EXCLUDED_DIVISORS:
                    continue
                if y % STEP in EXCLUDED_DIVISORS:
                    continue
                color = get_pixel(image, (x, y))
                average_color = tuple(3 * [int((color[0] + color[1] + color[2]) / 3)] + [255])
                image.putpixel((x, y), average_color)
        new_name = f"pbi_{image_index:03d}.png"
        image.save(new_name)
        print(f"{new_name} done")


if __name__ == "__main__":
    main()
