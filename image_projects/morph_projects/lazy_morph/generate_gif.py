import imageio
import os
from PIL import Image

RESIZE_FACTOR = 4
RESAMPLING_MODE = Image.Resampling.NEAREST
FRAMES_FOLDER = "./frames"
RESIZED_FOLDER = f"{FRAMES_FOLDER}/resized"
# this constant is used to determine how many times the first and last frames will be repeated in the gif, to make it look better
ATTENTION_INTERVAL = 10


def colocaImagemNoGif(writer, nome: str) -> None:  # type: ignore
    image = imageio.imread(nome)  # type: ignore
    writer.append_data(image)  # type: ignore


def get_frames_from_folder(folder_path: str) -> list[str]:
    frames: list[str] = []
    for frame_file in os.listdir(folder_path):
        frames.append(f"{folder_path}/{frame_file}")
    return frames


def open_image(image_path: str) -> Image.Image:
    with Image.open(image_path) as image:
        image_in_memory = image.copy()
        return image_in_memory


def main() -> None:
    frames = get_frames_from_folder(FRAMES_FOLDER)
    frames.remove(RESIZED_FOLDER)
    for filename in frames:
        image = open_image(filename)
        name_without_path, extension = os.path.basename(filename).split(".")
        filename = f"{RESIZED_FOLDER}/{name_without_path}_resize.{extension}"
        width, height = image.size
        resize_size = (width * RESIZE_FACTOR, height * RESIZE_FACTOR)
        image.resize(resize_size, resample=RESAMPLING_MODE).save(filename)
    file_amount = len(os.listdir(RESIZED_FOLDER))
    gif_name = f"./Animation{file_amount:03d}.gif"
    with imageio.get_writer(gif_name, mode="I") as writer:  # type: ignore
        frames = get_frames_from_folder(RESIZED_FOLDER)
        first_frame = frames.pop(0)
        for _ in range(ATTENTION_INTERVAL):
            colocaImagemNoGif(writer, first_frame)
        last_frame = frames.pop()
        for frame in frames:
            colocaImagemNoGif(writer, frame)
        for _ in range(ATTENTION_INTERVAL):
            colocaImagemNoGif(writer, last_frame)
    print("Gif created successfully!")


if __name__ == "__main__":
    main()
