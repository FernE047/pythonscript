from PIL import Image
import send2trash
import os

FRAMES_FOLDER = "./frames"
RESIZED_FOLDER = "./frames/resized"
POKEMON_COUNT = 761
POKEMON_FOLDER = "./imagens/PokedexSemFundo"
ALLOWED_FILE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".bmp", ".gif")


def get_image(index_chosen: int = 1) -> str:
    if not os.path.exists(POKEMON_FOLDER):
        raise FileNotFoundError(f"Folder not found: {POKEMON_FOLDER}")
    index = 0
    for filename in os.listdir(POKEMON_FOLDER):
        if not filename.lower().endswith(ALLOWED_FILE_EXTENSIONS):
            continue
        index += 1
        if index == index_chosen:
            return os.path.join(POKEMON_FOLDER, filename)
    raise ValueError(f"Image with index {index_chosen} not found in {POKEMON_FOLDER}")


def get_user_integer(
    message: str, min_value: int | None = None, max_value: int | None = None
) -> int:
    while True:
        user_input = input(f"{message} : ")
        try:
            value = int(user_input)
            if (min_value is not None) and (value < min_value):
                print(f"value must be greater than or equal to {min_value}")
                continue
            if (max_value is not None) and (value > max_value):
                print(f"value must be less than or equal to {max_value}")
                continue
            return value
        except Exception as _:
            print("invalid value, please try again")


def clear_folder(folder: str) -> None:
    if not os.path.exists(folder):
        os.makedirs(folder)
    files = [f"{folder}/{a}" for a in os.listdir(folder)]
    if RESIZED_FOLDER in files:
        files.pop(files.index(RESIZED_FOLDER))
    for file in files:
        send2trash.send2trash(file)


def open_image_as_rgba(image_path: str) -> Image.Image:
    with Image.open(image_path) as image:
        image_in_memory = image.copy()
        if image.mode != "RGBA":
            return image_in_memory.convert("RGBA")
        return image_in_memory


def save_layers(image_name: str) -> None:
    index = get_user_integer(
        f"choose a pokemon between 0 and {POKEMON_COUNT}",
        min_value=0,
        max_value=POKEMON_COUNT,
    )
    pokemon_image = get_image(index)
    image = open_image_as_rgba(pokemon_image)
    image.save(f"./{image_name}.png")


def main() -> None:
    print("ATTENTION THE FOLDER CONTENTS WILL BE DELETED !!!!!")
    input("Press Enter to continue... (ctrl + C to cancel)")
    clear_folder(FRAMES_FOLDER)
    clear_folder(RESIZED_FOLDER)
    save_layers("source")
    save_layers("target")


if __name__ == "__main__":
    main()
