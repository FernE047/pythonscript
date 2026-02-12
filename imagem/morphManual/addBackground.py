from PIL import Image
from morpher import interpolate_tuples
from corrigeFrames import fix_trapped_pixels
import os

CoordData = tuple[int, int]
BACKGROUND_COLOR = (255, 255, 255, 0)
FRAME_FOLDER = "./frames"
ALPHA_CHANNEL = 3
MAX_BRIGHTNESS = 255
SOURCE_FOLDER = "./partes/iniciais"
TARGET_FOLDER = "./partes/finais"


def get_pixel(imagem: Image.Image, coord: CoordData) -> tuple[int, ...]:
    pixel = imagem.getpixel(coord)
    if pixel is None:
        return BACKGROUND_COLOR
    if not isinstance(pixel, tuple):
        pixel_int = int(pixel)
        return (pixel_int, pixel_int, pixel_int)
    return pixel


def generate_background(image_name: str) -> Image.Image:
    print("back iniciado")
    image = Image.open(f"./{image_name}.png")
    directory = SOURCE_FOLDER if image_name == "source" else TARGET_FOLDER
    for partsName in [f"{directory}/{fileName}" for fileName in os.listdir(directory)]:
        parte = Image.open(partsName)
        width, height = parte.size
        is_first_occurrence = True
        for x in range(width):
            alterations = 0
            for y in range(height):
                coord = (x, y)
                parte_pixel = get_pixel(parte, coord)
                if parte_pixel[ALPHA_CHANNEL] == MAX_BRIGHTNESS:
                    image.putpixel(coord, BACKGROUND_COLOR)
                    alterations += 1
            if is_first_occurrence and (alterations > 0):
                is_first_occurrence = False
            if not is_first_occurrence and (alterations == 0):
                break
    fix_trapped_pixels(image, [])
    image.save(f"./background_{image_name}.png")
    print("background finished")
    return image


def main() -> None:
    background_source = generate_background("source")
    background_target = generate_background("target")
    frames = [f"{FRAME_FOLDER}/{file}" for file in os.listdir(FRAME_FOLDER)]
    frames.pop(0)
    frames.pop()
    frames.pop()
    for frame_index, frame_name in enumerate(frames):
        frame = Image.open(frame_name)
        width, height = background_source.size
        for x in range(width):
            for y in range(height):
                coord = (x, y)
                pixel = get_pixel(frame, coord)
                if pixel[ALPHA_CHANNEL] != 0:
                    continue
                pixel_source = get_pixel(background_source, coord)
                pixel_target = get_pixel(background_target, coord)
                interpolated_pixel = interpolate_tuples(
                    pixel_source, pixel_target, frame_index
                )
                frame.putpixel(coord, interpolated_pixel)
        print(frame_index)
        frame.save(frame_name)
        frame.close()


if __name__ == "__main__":
    main()
