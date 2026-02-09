import imageio
import os
from PIL import Image

FRAME_FOLDER = "./frames"
RESIZED_FOLDER = f"{FRAME_FOLDER}/resized"
RESIZE_FACTOR = 4
RESAMPLING_MODE = Image.Resampling.NEAREST
IMAGE_MAX_AREA = 10000


def colocaImagemNoGif(
    writer: imageio.core.format.Writer,  # type:ignore
    nome: str,
) -> None:
    imagem = imageio.imread(nome)  # type:ignore
    writer.append_data(imagem)  # type:ignore


def resize(image_file_path: str) -> None:
    image = Image.open(image_file_path)
    image_name, extension = os.path.splitext(image_file_path)
    image_file_path = f"{image_name}_resize{extension}"
    width, height = image.size
    if width * height < IMAGE_MAX_AREA:
        resize_width = width * RESIZE_FACTOR
        resize_height = height * RESIZE_FACTOR
        resize_size = (resize_width, resize_height)
        image.resize(resize_size, resample=RESAMPLING_MODE).save(image_file_path)
    else:
        image.save(image_file_path)
    image.close()


def main() -> None:
    frames = [
        f"{FRAME_FOLDER}/{frame_name}" for frame_name in os.listdir(f"{FRAME_FOLDER}")
    ]
    frames.remove(RESIZED_FOLDER)
    for frame in frames:
        resize(frame)
    unique_id_file = len(os.listdir("./"))
    gif_name = f"./Morph_{unique_id_file:03d}.gif"
    with imageio.get_writer(gif_name, mode="I") as writer:  # type:ignore
        frames = [
            f"{RESIZED_FOLDER}/{frame_name}"
            for frame_name in os.listdir(f"{RESIZED_FOLDER}/")
        ]
        first_frame = frames.pop(0)
        for _ in range(10):
            colocaImagemNoGif(writer, first_frame)
        last_frame = frames.pop()
        for frame in frames:
            colocaImagemNoGif(writer, frame)
        for _ in range(10):
            colocaImagemNoGif(writer, last_frame)
    print("Gif created successfully!")


if __name__ == "__main__":
    main()
