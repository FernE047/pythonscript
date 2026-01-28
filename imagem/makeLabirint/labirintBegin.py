from PIL import Image
from os import listdir


def coordDirection(coord, direction):
    x, y = coord
    if direction == 0:
        coord = (x, y + 1)
    elif direction == 1:
        coord = (x + 1, y)
    elif direction == 2:
        coord = (x, y - 1)
    else:
        coord = (x - 1, y)
    return coord


BRANCO = (255, 255, 255, 255)
PRETO = (0, 0, 0, 255)
imagem = Image.open(f"pureLabirint\\labirint{4:03d}.png")
largura, altura = imagem.size
for x in range(1, largura - 1, 2):
    for y in range(1, altura - 1, 2):
        coord = (x, y)
        closedDirection = []
        if imagem.getpixel(coord) == BRANCO:
            for direction in range(4):
                novaCoord = coordDirection(coord, direction)
                if imagem.getpixel(novaCoord) == PRETO:
                    closedDirection.append(novaCoord)
            if len(closedDirection) == 3:
                imagem.putpixel(coord, (255, 0, 0, 255))
            if len(closedDirection) == 2:
                imagem.putpixel(coord, (0, 255, 0, 255))
            if len(closedDirection) == 1:
                imagem.putpixel(coord, (0, 0, 255, 255))
            if len(closedDirection) == 0:
                imagem.putpixel(coord, (255, 255, 0, 255))
imagem.save(f"labirint{len(listdir()):03d}.png")
imagem.close()
