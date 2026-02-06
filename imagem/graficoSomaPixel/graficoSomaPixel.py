from PIL import Image
import os
import gc

INPUT_IMAGE_FOLDER = "./funny_images"
OUTPUT_IMAGE_FOLDER = f"{INPUT_IMAGE_FOLDER}/graficos"
BACKGROUND_COLOR = (255, 255, 255, 255)
HIGHLIGHT_COLOR = (0, 0, 0, 255)
INITIAL_ATTEMPT = 1
MAX_BRIGHTNESS = 255
COLOR_CHANNELS = 3
OUTPUT_HEIGHT = MAX_BRIGHTNESS * COLOR_CHANNELS
LOGGING_PIXEL_THRESHOLD = 1000
LOGGING_OUTPUT_THRESHOLD = 10
SCALING_FACTOR = 10


def generate_brightness_histogram(img: str, scaling_attempt: int = INITIAL_ATTEMPT) -> Image.Image:
    imagem = Image.open(img)
    width, height = imagem.size
    tamanho = width * height
    print(tamanho)
    pixel_counter = 0
    brightness_threshold_counts = [0 for _ in range(OUTPUT_HEIGHT)]
    for x in range(width):
        for y in range(height):
            pixel = imagem.getpixel((x, y))
            if pixel is None:
                pixel = BACKGROUND_COLOR
            if not isinstance(pixel, tuple):
                pixel_int = int(pixel)
                pixel = (pixel_int, pixel_int, pixel_int, MAX_BRIGHTNESS)
            color_sum = sum(pixel[:COLOR_CHANNELS])
            if pixel_counter % LOGGING_PIXEL_THRESHOLD == 0:
                print(str(pixel_counter))
            for index in range(OUTPUT_HEIGHT):
                if color_sum >= OUTPUT_HEIGHT - index:
                    brightness_threshold_counts[OUTPUT_HEIGHT - index] += 1
            pixel_counter += 1
    while True:
        try:
            size = (int(tamanho / scaling_attempt), OUTPUT_HEIGHT)
            output_image = Image.new("RGBA", size, BACKGROUND_COLOR)
            break
        except Exception:
            scaling_attempt *= SCALING_FACTOR
    for index in range(len(brightness_threshold_counts)):
        if index % LOGGING_OUTPUT_THRESHOLD == 0:
            print(str(index))
        brightness_threshold_count = brightness_threshold_counts[index]
        for x in range(brightness_threshold_count):
            output_image.putpixel((x, index), HIGHLIGHT_COLOR)
    return output_image


def main() -> None:
    print(INPUT_IMAGE_FOLDER)
    images = os.listdir(INPUT_IMAGE_FOLDER)
    try:
        output_folder = OUTPUT_IMAGE_FOLDER
        os.makedirs(output_folder, exist_ok=True)
    except Exception:
        output_folder = INPUT_IMAGE_FOLDER
    for image in images:
        output_image = generate_brightness_histogram(f"{INPUT_IMAGE_FOLDER}/{image}")
        image_name, extension = os.path.splitext(image)
        output_name = f"{image_name}_graf{extension}"
        output_image.save(os.path.join(output_folder, output_name))
    print(gc.collect())
    # I used to love gc.collect because I have leaked memory in the past using C programs. I know it's not really needed in Python but at the past I was very traumatized by memory leaks.

    # TODO: implement Rotation, Cut and Resize


if __name__ == "__main__":
    main()
