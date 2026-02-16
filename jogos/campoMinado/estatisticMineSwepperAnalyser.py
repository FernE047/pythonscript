from PIL import Image, ImageGrab

# this code was an attempt to read an image and make a representation of the minesweeper board, but it was not successful, the colors of the pixels were not consistent on windows 7.
# the code is incomplete and not used, but it is kept here for reference and future attempts to read the minesweeper board from an image.

def open_image_as_rgba(image_path: str) -> Image.Image:
    with Image.open(image_path) as image:
        image_in_memory = image.copy()
        if image.mode != "RGBA":
            return image_in_memory.convert("RGBA")
        return image_in_memory


def get_pixel(image: Image.Image, coord: tuple[int, int]) -> tuple[int, ...]:
    pixel = image.getpixel(coord)
    if pixel is None:
        raise ValueError("Pixel not found")
    if isinstance(pixel, int):
        raise ValueError("Image is not in RGB mode")
    if isinstance(pixel, float):
        raise ValueError("Image is not in RGB mode")
    if len(pixel) < 4:
        raise ValueError("Image is not in RGB mode")
    return pixel


def main() -> None:
    image = ImageGrab.grabclipboard()
    if image is None:
        raise Exception("No image in clipboard")
    if isinstance(image, list):
        raise Exception("Clipboard contains multiple items, expected an image")
    image.save("screen.png")
    image.close()
    image = open_image_as_rgba("screen.png")
    print("0 - 9X9")
    print("1 - 16X16")
    print("2 - 16X30")
    game_mode = input()
    if game_mode == "0":
        top_left_corner = (436, 133)
        grid_width = 9
        grid_height = 9
        cell_size = 55
    elif game_mode == "1":
        top_left_corner = (400, 99)
        grid_width = 16
        grid_height = 16
        cell_size = 35
    else:
        top_left_corner = (154, 99)
        grid_width = 30
        grid_height = 16
        cell_size = 35
    board: list[list[float | tuple[int, ...]]] = []
    for _ in range(grid_width):
        row: list[float | tuple[int, ...]] = []
        for _ in range(grid_height):
            row.append(9.0)
        board.append(row)
    width_end = top_left_corner[0] + grid_width * cell_size
    height_end = top_left_corner[1] + grid_height * cell_size
    for cell_index_x, cell_start_x in enumerate(
        range(top_left_corner[0], width_end, cell_size)
    ):
        for cell_index_y, cell_start_y in enumerate(
            range(top_left_corner[1], height_end, cell_size)
        ):
            rgb_total = [0, 0, 0]
            cell_width_end = cell_start_x + cell_size
            cell_height_end = cell_start_y + cell_size
            for x in range(cell_start_x, cell_width_end):
                for y in range(cell_start_y, cell_height_end):
                    pixel = get_pixel(image, (x, y))
                    for color_index in range(3):
                        rgb_total[color_index] += pixel[color_index]
            average_color: list[int] = []
            for color_index in range(3):
                average_color.append(rgb_total[color_index] // (cell_size**2))
            color = tuple(average_color)
            board[cell_index_x][cell_index_y] = color
            print(color)
        print()


if __name__ == "__main__":
    main()
