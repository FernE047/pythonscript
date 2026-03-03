from PIL import Image, ImageDraw

#this was the first time I used PIL ImageDraw to draw a line

WHITE = (255, 255, 255, 255)
SIZE = (100, 100)
COORD_A = (50, 25)
COORD_B = (80, 0)
LINE = (COORD_A[0], COORD_A[1], COORD_B[0], COORD_B[1])
FILL = 0
WIDTH = 1


def main() -> None:
    line_image = Image.new("RGB", SIZE, WHITE)
    draw = ImageDraw.Draw(line_image)
    draw.line(LINE, fill=FILL, width=WIDTH)
    # (firstX,firstY,secondX,secondY)
    line_image.save("teste.png")


if __name__ == "__main__":
    main()
