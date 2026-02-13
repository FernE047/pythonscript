from PIL import Image

MAX_BRIGHTNESS = 255
BACKGROUND_COLOR = (255, 255, 255, 255)
COLOR_CHANNELS = 4


def get_user_integer(message: str) -> int:
    while True:
        user_input = input(f"{message}")
        try:
            valor = int(user_input)
            return valor
        except Exception as _:
            print("Invalid value, please try again")


def get_user_image() -> Image.Image:
    while True:
        user_input = input("Enter the image name (with extension): ")
        try:
            imagem = open_image_as_rgba(user_input)
            return imagem
        except Exception as _:
            print("Invalid file, please try again")


def get_pixel(imagem: Image.Image, coord: tuple[int, int]) -> tuple[int, ...]:
    pixel = imagem.getpixel(coord)
    if pixel is None:
        return BACKGROUND_COLOR
    if not isinstance(pixel, tuple):
        pixel_int = int(pixel)
        return (pixel_int, pixel_int, pixel_int, MAX_BRIGHTNESS)
    return pixel


def open_image_as_rgba(image_path: str) -> Image.Image:
    with Image.open(image_path) as image:
        image_in_memory = image.copy()
        if image.mode != "RGBA":
            return image_in_memory.convert("RGBA")
        return image_in_memory


def processaImagemPorImagem(
    image_input: Image.Image, image_target: Image.Image, frames: int
) -> None:
    size = image_input.size
    width, height = size
    total_frames = frames + 1
    for frame in range(frames):
        current_frame = frame + 1
        image = Image.new("RGBA", size, BACKGROUND_COLOR)
        for x in range(width):
            for y in range(height):
                coord = (x, y)
                pixel_input = get_pixel(image_input, coord)
                pixel_target = get_pixel(image_target, coord)
                color: list[int] = []
                for index in range(COLOR_CHANNELS):
                    channel_input = pixel_input[index]
                    channel_target = pixel_target[index]
                    difference = channel_target - channel_input
                    frame_normalized = current_frame / total_frames
                    current_change = frame_normalized * difference
                    color.append(int(channel_input + current_change))
                image.putpixel(coord, tuple(color))
        image.save(f"output_{current_frame:02d}.png")


def main() -> None:
    input_image = get_user_image()
    target_image = get_user_image()
    frames = get_user_integer("\nEnter the number of middle frames: ")
    width_input, height_input = input_image.size
    width_target, height_target = target_image.size
    size_input = width_input * height_input
    size_target = width_target * height_target
    if size_input > size_target:
        input_image = input_image.resize((width_target, height_target))
    else:
        target_image = target_image.resize((width_input, height_input))
    input_image.save("output_00.png")
    target_image.save(f"output_{frames + 1:02d}.png")
    processaImagemPorImagem(input_image, target_image, frames)


if __name__ == "__main__":
    main()
