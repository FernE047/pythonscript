import pypdn  # type: ignore

# pypdn doesn't have type hints, so we ignore it. tyhe library is very small and the code is simple, it's easy to infer types if you need to.
from PIL import Image
import os

SOURCE_FOLDER = "./parts/sources"
TARGET_FOLDER = "./parts/targets"
RESIZED_FOLDER = "./frames/resized"
SOURCE_PDN = "inicial.pdn"
TARGET_PDN = "final.pdn"
FOLDERS_TO_CLEAN = [
    SOURCE_FOLDER,
    TARGET_FOLDER,
    "./parts/config",
    "./debug",
    "./frames",
    RESIZED_FOLDER,
]


def clean_folder(folder: str) -> None:
    # dangerous function, be careful with it
    files = [f"{folder}/{a}" for a in os.listdir(folder)]
    if RESIZED_FOLDER in files:
        files.pop(files.index(RESIZED_FOLDER))
    for file in files:
        os.remove(file)


def save_layers(name: str, folder: str) -> None:
    layeredImage = pypdn.read(f"./{name}")
    new_image = Image.fromarray(layeredImage.layers[0].image)
    image_name, _ = os.path.splitext(name)
    new_image.save(f"./{image_name}.png")
    new_image.close()
    layers_count = len(layeredImage.layers)
    for layer_index in range(layers_count):
        layer = layeredImage.layers[layer_index + 1]
        image_array = layer.image
        new_image = Image.fromarray(image_array)
        layer_name = f"{folder}/{layer_index:03d}.png"
        new_image.save(layer_name)
        new_image.close()


def main() -> None:
    for folder in FOLDERS_TO_CLEAN:
        clean_folder(folder)
    save_layers(SOURCE_PDN, SOURCE_FOLDER)
    save_layers(TARGET_PDN, TARGET_FOLDER)


if __name__ == "__main__":
    main()
