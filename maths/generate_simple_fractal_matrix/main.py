from PIL import Image
import os

RANDOM_INDEX_SEED = 29
MAX_SIZE = 5000
BACKGROUND_COLOR = (255, 255, 255, 255)
HIGHLIGHT_COLOR = (0, 0, 0, 255)


def convert_matrix_to_image(matrix: list[list[int]]) -> Image.Image:
    height = len(matrix)
    width = max([len(row_index) for row_index in matrix])
    print(f"\nheight: {height}\nwidth: {width}")
    for row_index in range(height):
        while len(matrix[row_index]) < width:
            matrix[row_index].append(0)
    output_image = Image.new("RGBA", (width, height), BACKGROUND_COLOR)
    for y in range(height):
        for x in range(width):
            if matrix[y][x]:
                output_image.putpixel((x, y), HIGHLIGHT_COLOR)
    return output_image


def generate_next_fractal(
    fractal_pattern: Image.Image, reference: Image.Image
) -> Image.Image | None:
    width_reference, height_reference = reference.size
    width_pattern, height_pattern = fractal_pattern.size
    width = width_reference * width_pattern
    height = height_reference * height_pattern
    fractal = Image.new("RGBA", (width, height), BACKGROUND_COLOR)
    if (width > MAX_SIZE) or (height > MAX_SIZE):
        return None
    for x in range(width_reference):
        for y in range(height_reference):
            if reference.getpixel((x, y)) == HIGHLIGHT_COLOR:
                fractal.paste(fractal_pattern, (x * width_pattern, y * height_pattern))
    return fractal


def generate_fractals(matrix: list[list[int]], name: str) -> None:
    new_folder = os.path.join(os.getcwd(), name.title())
    os.makedirs(new_folder)
    reference_image = convert_matrix_to_image(matrix)
    fractal_image: Image.Image = reference_image
    save_path = os.path.join(new_folder, f"{name.title()}_01.png")
    fractal_image.save(save_path)
    fractal_index = 2
    while True:
        new_fractal = generate_next_fractal(fractal_image, reference_image)
        if new_fractal is None:
            print(f"done {fractal_index} fractals\n")
            return
        save_path = os.path.join(new_folder, f"{name.title()}_{fractal_index:02d}.png")
        new_fractal.save(save_path)
        fractal_image = new_fractal
        fractal_index += 1


def main() -> None:
    random_index = RANDOM_INDEX_SEED
    matrix: list[list[int]] = [[]]
    current_index = 0
    print(
        "'0' for nothing\n'1' for value\n'empty' for new line\nother to save\n'apg' at the end to save and delete"
    )
    while True:
        print(matrix)
        user_input = input()
        if user_input == "":
            current_index += 1
            matrix.append([])
        elif user_input.isdigit():
            matrix[current_index] = [int(digit) for digit in list(user_input)]
            current_index += 1
            matrix.append([])
        else:
            if user_input[-3:] == "apg":
                matrix = matrix[:-1]
                user_input = user_input[:-3]
            if user_input == "random":
                user_input += str(random_index)
                random_index += 1
            generate_fractals(matrix, user_input)
            matrix = [[]]
            current_index = 0
            break


if __name__ == "__main__":
    main()
