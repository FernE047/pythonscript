from pathlib import Path
import pypdn  # type: ignore

# pypdn doesn't have type hints, so we ignore it. the library is very small and the code is simple, it's easy to infer types if you need to.
from PIL import Image

PARTS_FOLDER = Path("parts")
SOURCE_FOLDER = PARTS_FOLDER / "sources"
TARGET_FOLDER = PARTS_FOLDER / "targets"
RESIZED_FOLDER = Path("frames") / "resized"
SOURCE_PDN = Path("inicial.pdn")
TARGET_PDN = Path("final.pdn")
FOLDERS_TO_CLEAN = [
    SOURCE_FOLDER,
    TARGET_FOLDER,
    PARTS_FOLDER / "config",
    Path("debug"),
    Path("frames"),
    RESIZED_FOLDER,
]


def clean_folder(folder: Path) -> None:
    # dangerous function, be careful with it
    for file in folder.iterdir():
        if file.is_dir():
            continue
        file.unlink()


def save_layers(name: Path, folder: Path) -> None:
    layeredImage = pypdn.read(str(name))
    new_image = Image.fromarray(layeredImage.layers[0].image)
    new_image.save(name.with_suffix(".png"))
    new_image.close()
    layers_count = len(layeredImage.layers)
    for layer_index in range(layers_count):
        layer = layeredImage.layers[layer_index + 1]
        image_array = layer.image
        new_image = Image.fromarray(image_array)
        layer_name = folder / f"{layer_index:03d}.png"
        new_image.save(layer_name)
        new_image.close()


def clean_project_folder() -> None:
    for folder in FOLDERS_TO_CLEAN:
        clean_folder(folder)
    save_layers(SOURCE_PDN, SOURCE_FOLDER)
    save_layers(TARGET_PDN, TARGET_FOLDER)