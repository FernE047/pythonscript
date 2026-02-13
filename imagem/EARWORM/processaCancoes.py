import shelve
import os
from PIL import Image

BLACK = (0, 0, 0, 255)


def open_image_as_rgba(image_path: str) -> Image.Image:
    with Image.open(image_path) as image:
        image_in_memory = image.copy()
        if image.mode != "RGBA":
            return image_in_memory.convert("RGBA")
        return image_in_memory


def get_images_from_folder(folder: str) -> list[str]:
    images = os.listdir(folder)
    images_path = [os.path.join(folder, image) for image in images]
    return images_path


def get_images_average_size(images_path: list[str]) -> int:
    length_total = 0
    for image_path in images_path:
        image = open_image_as_rgba(image_path)
        length, _ = image.size
        length_total += length
    return int(length_total / len(images_path))


def main() -> None:
    diretory = os.getcwd()
    folder = os.path.join(diretory, "imagens")
    images_path = get_images_from_folder(folder)
    for category_folder in ["artist", "album"]:
        folder = os.path.join(diretory, category_folder)
        folders = os.listdir(folder)
        folders_path = [os.path.join(folder, folder_name) for folder_name in folders]
        for folder_path in folders_path:
            images_path += get_images_from_folder(folder_path)
    average_length = get_images_average_size(images_path)
    x_heat: list[int] = []
    y_heat: list[int] = []
    z_heat: list[int] = []
    for x in range(average_length):
        for y in range(average_length):
            x_heat.append(x)
            y_heat.append(y)
            z_heat.append(0)
    for image_path in images_path:
        print(image_path)
        image = open_image_as_rgba(image_path)
        length, _ = image.size
        if length <= average_length:
            average_length = length
        for y in range(average_length):
            for x in range(average_length):
                if x == y:
                    continue
                if image.getpixel((x, y)) == BLACK:
                    continue
                z_heat[average_length * x + y] += 1

    with shelve.open(os.path.join(diretory, "dadosPreProcessados")) as database:
        database["x"] = x_heat
        database["y"] = y_heat
        database["z"] = z_heat
        database["maximum"] = max(z_heat)


if __name__ == "__main__":
    main()
