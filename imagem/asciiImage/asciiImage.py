from PIL import Image
import os


def get_image_from_folder() -> list[str]:
    print("enter the image folder:")
    image_folder = input()
    print("quantity")
    user_input = input()
    try:
        quantity = int(user_input)
    except ValueError:
        quantity = None
    folder = f"images/{image_folder}"
    images: list[str] = []
    if os.path.exists(folder):
        for file_name in os.listdir(folder):
            if file_name.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif")):
                images.append(os.path.join(folder, file_name))
                if quantity is not None and len(images) >= quantity:
                    break
    return images


def resize_image_to_width(
    width_output: int, image_black_white: Image.Image
) -> Image.Image:
    width, height = image_black_white.size
    if width <= width_output:
        return image_black_white
    aspectRatio = width_output / width
    height_output = int(height * aspectRatio)
    return image_black_white.resize((width_output, height_output))


def set_display_width() -> int:
    print("size")
    print("165 - max")
    print("075 - min")
    print("060 - terminal")
    print("026 - whats")
    size = input()
    if size == "whats":
        return 26
    if size == "max":
        return 165
    if size == "min":
        return 75
    if size == "terminal":
        return 60
    try:
        return int(size)
    except ValueError:
        return 75


def main() -> None:
    image_paths = get_image_from_folder()
    brightness_levels = [" ", "`", ".", ",", "+", "%", "@", "#"]
    width_output = set_display_width()
    for image in image_paths:
        print("\n" + image + "\n")
        image_colored = Image.open(image)
        image_black_white = image_colored.convert("L")
        image_output = resize_image_to_width(width_output, image_black_white)
        width, height = image_output.size
        for y in range(height):
            row = ""
            for x in range(width):
                pixel = image_output.getpixel((x, y))
                assert isinstance(pixel, int) # since the image is in 'L' mode
                row += brightness_levels[int(pixel / 32) - 1]
            print(row)


if __name__ == "__main__":
    main()
