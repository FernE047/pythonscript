from PIL import Image

# this code is used to transform a pokemon into a square image, it's incomplete.


def detectCorners(image: Image.Image) -> tuple[int, int, int, int]:
    largura, altura = image.size
    low_x = largura
    high_x = 0
    low_y = altura
    high_y = 0
    for x in range(largura):
        for y in range(altura):
            pixel = image.getpixel((x, y))
            if pixel is None:
                raise ValueError("exception just to avoid a mypy error, pixel is None")
            if not isinstance(pixel, tuple):
                raise ValueError("exception just to avoid a mypy error, pixel is not a tuple")
            if pixel[3] == 255:
                if x < low_x:
                    low_x = x
                if y < low_y:
                    low_y = y
                if x > high_x:
                    high_x = x
                if y > high_y:
                    high_y = y
    return (low_x, high_x, low_y, high_y)


def main() -> None:
    for index in range(762):
        filename = f"pokedex/pokemon{index:03d}.png"
        print(filename)
        image = Image.open(filename)
        width, height = image.size  # type: ignore
        # not used currently, but may be used in the future.
        low_x, high_x, low_y, high_y = detectCorners(image)
        size_x = high_x - low_x + 1
        size_y = high_y - low_y + 1
        largest_size = max(size_x, size_y)
        for t in range(largest_size):  # type: ignore
            # not used currently, but may be used in the future.
            for x in range(low_x, high_x + 1):  # type: ignore
                # not used currently, but may be used in the future.
                for y in range(low_y, high_y + 1):
                    if y + size_y:  # type: ignore
                        # past me stopped coding in this line above
                        pass


if __name__ == "__main__":
    main()
