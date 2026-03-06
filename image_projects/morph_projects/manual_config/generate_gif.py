from pathlib import Path
import imageio
from PIL import Image

FRAME_FOLDER = Path("frames")
RESIZED_FOLDER = FRAME_FOLDER / "resized"
RESIZE_FACTOR = 4
RESAMPLING_MODE = Image.Resampling.NEAREST
IMAGE_MAX_AREA = 10000
# how many frames will be repeated at the beginning and end of the gif, to make it look better
GIF_START_DELAY = 10


def colocaImagemNoGif(
    writer: imageio.core.format.Writer,  # type:ignore
    nome: Path,
) -> None:
    imagem = imageio.imread(nome)  # type:ignore
    writer.append_data(imagem)  # type:ignore


def open_image(image_path: Path) -> Image.Image:
    with Image.open(image_path) as image:
        image_in_memory = image.copy()
        return image_in_memory


def resize(image_file_path: Path) -> None:
    image = open_image(image_file_path)
    image_file_path = Path(f"{image_file_path.stem}_resize{image_file_path.suffix}")
    width, height = image.size
    if width * height < IMAGE_MAX_AREA:
        resize_width = width * RESIZE_FACTOR
        resize_height = height * RESIZE_FACTOR
        resize_size = (resize_width, resize_height)
        image.resize(resize_size, resample=RESAMPLING_MODE).save(image_file_path)
    else:
        image.save(image_file_path)


def generate_gif() -> None:
    frames = [
        frame_name for frame_name in FRAME_FOLDER.iterdir() if frame_name.is_file()
    ]
    frames.remove(RESIZED_FOLDER)
    for frame in frames:
        resize(frame)
    unique_id_file = len(list(Path(".").iterdir()))
    gif_name = Path(f"Morph_{unique_id_file:03d}.gif")
    with imageio.get_writer(gif_name, mode="I") as writer:  # type:ignore
        frames = [frame_name for frame_name in RESIZED_FOLDER.iterdir()]
        first_frame = frames.pop(0)
        for _ in range(GIF_START_DELAY):
            colocaImagemNoGif(writer, first_frame)
        last_frame = frames.pop()
        for frame in frames:
            colocaImagemNoGif(writer, frame)
        for _ in range(GIF_START_DELAY):
            colocaImagemNoGif(writer, last_frame)
    print("Gif created successfully!")
