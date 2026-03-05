from pathlib import Path
import imageio
from PIL import Image

RESIZE_FACTOR = 4
RESAMPLING_MODE = Image.Resampling.NEAREST
FRAMES_FOLDER = Path("frames")
RESIZED_FOLDER = FRAMES_FOLDER / "resized"
# this constant is used to determine how many times the first and last frames will be repeated in the gif, to make it look better
ATTENTION_INTERVAL = 10


def colocaImagemNoGif(writer, nome: Path) -> None:  # type: ignore
    image = imageio.imread(nome)  # type: ignore
    writer.append_data(image)  # type: ignore


def get_frames_from_folder(folder_path: Path) -> list[Path]:
    frames: list[Path] = []
    for frame_file in folder_path.iterdir():
        frames.append(frame_file)
    return frames


def open_image(image_path: Path) -> Image.Image:
    with Image.open(image_path) as image:
        image_in_memory = image.copy()
        return image_in_memory


def generate_gif() -> None:
    frames = get_frames_from_folder(FRAMES_FOLDER)
    frames.remove(RESIZED_FOLDER)
    for filename in frames:
        image = open_image(filename)
        filename = RESIZED_FOLDER / f"{filename.stem}_resize{filename.suffix}"
        width, height = image.size
        resize_size = (width * RESIZE_FACTOR, height * RESIZE_FACTOR)
        image.resize(resize_size, resample=RESAMPLING_MODE).save(filename)
    file_amount = len(list(RESIZED_FOLDER.iterdir()))
    gif_name = Path(f"Animation{file_amount:03d}.gif")
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
