from PIL import Image, ImageDraw


def main() -> None:
    imagemNumber = "6"

    imagemOrigem = Image.open("images" + imagemNumber + ".jpg")
    tamanho = imagemOrigem.size
    width, height = tamanho
    if (width % 2 == 0) and (height % 2 == 0):
        imagemBest = Image.new("RGBA", (width + 3, height + 3))
        imagemBest.paste(imagemOrigem, (1, 1))
    elif width % 2 == 0:
        imagemBest = Image.new("RGBA", (width + 3, height + 2))
        imagemBest.paste(imagemOrigem, (1, 1))
    elif height % 2 == 0:
        imagemBest = Image.new("RGBA", (width + 2, height + 3))
        imagemBest.paste(imagemOrigem, (1, 1))
    else:
        imagemBest = Image.new("RGBA", (width + 2, height + 2))
        imagemBest.paste(imagemOrigem, (1, 1))
    print("melhor imagem feita")
    tamanho = imagemBest.size
    width, height = tamanho
    meio = (int((width + 1) / 2), int((height + 1) / 2))
    extensao = 2 * width + 2 * height + 4
    imageGraf = Image.new("RGB", (extensao, height))
    print(str(extensao))
    a = 0
    for aheight in range(0, meio[1] + 1):
        lineImage = Image.new("RGBA", (width, height), (255, 255, 255, 255))
        draw = ImageDraw.Draw(lineImage)
        draw.line(
            (meio[0], meio[1], 0, aheight), fill=(0, 0, 0, 255), width=1
        )  # (firstX,firstY,secondX,secondY)
        altGraf = 0
        if aheight % 50 == 0:
            print(str(aheight))
            imageGraf.save("imagesgraf" + imagemNumber + ".jpg")
        for y in range(0, meio[1] + 1):
            for x in range(0, meio[0] + 1):
                if lineImage.getpixel((x, y)) == (0, 0, 0, 255):
                    imageGraf.putpixel((a, altGraf), imagemBest.getpixel((x, y)))
                    altGraf += 1
        a += 1
    for aheight in range(meio[1] + 1, height):
        lineImage = Image.new("RGBA", (width, height), (255, 255, 255, 255))
        draw = ImageDraw.Draw(lineImage)
        draw.line(
            (meio[0], meio[1], 0, aheight), fill=(0, 0, 0, 255), width=1
        )  # (firstX,firstY,secondX,secondY)
        altGraf = 0
        if aheight % 50 == 0:
            print(str(aheight))
            imageGraf.save("imagesgraf" + imagemNumber + ".jpg")
        for y in range(height - 1, meio[1] - 1, -1):
            for x in range(0, meio[0] + 1):
                if lineImage.getpixel((x, y)) == (0, 0, 0, 255):
                    imageGraf.putpixel((a, altGraf), imagemBest.getpixel((x, y)))
                    altGraf += 1
        a += 1
    for awidth in range(0, meio[0] + 1):
        lineImage = Image.new("RGBA", (width, height), (255, 255, 255, 255))
        draw = ImageDraw.Draw(lineImage)
        draw.line(
            (meio[0], meio[1], awidth, height - 1), fill=(0, 0, 0, 255), width=1
        )  # (firstX,firstY,secondX,secondY)
        altGraf = 0
        if awidth % 50 == 0:
            print(str(awidth))
            imageGraf.save("imagesgraf" + imagemNumber + ".jpg")
        for y in range(height - 1, meio[1] - 1, -1):
            for x in range(0, meio[0] + 1):
                if lineImage.getpixel((x, y)) == (0, 0, 0, 255):
                    imageGraf.putpixel((a, altGraf), imagemBest.getpixel((x, y)))
                    altGraf += 1
        a += 1
    for awidth in range(meio[0] + 1, width):
        lineImage = Image.new("RGBA", (width, height), (255, 255, 255, 255))
        draw = ImageDraw.Draw(lineImage)
        draw.line(
            (meio[0], meio[1], awidth, height - 1), fill=(0, 0, 0, 255), width=1
        )  # (firstX,firstY,secondX,secondY)
        altGraf = 0
        if awidth % 50 == 0:
            print(str(awidth))
            imageGraf.save("imagesgraf" + imagemNumber + ".jpg")
        for y in range(height - 1, meio[1] - 1, -1):
            for x in range(width - 1, meio[0] - 1, -1):
                if lineImage.getpixel((x, y)) == (0, 0, 0, 255):
                    imageGraf.putpixel((a, altGraf), imagemBest.getpixel((x, y)))
                    altGraf += 1
        a += 1
    for aheight in range(height - 1, meio[1] - 1, -1):
        lineImage = Image.new("RGBA", (width, height), (255, 255, 255, 255))
        draw = ImageDraw.Draw(lineImage)
        draw.line(
            (meio[0], meio[1], width - 1, aheight), fill=(0, 0, 0, 255), width=1
        )  # (firstX,firstY,secondX,secondY)
        altGraf = 0
        if aheight % 50 == 0:
            print(str(aheight))
            imageGraf.save("imagesgraf" + imagemNumber + ".jpg")
        for y in range(height - 1, meio[1] - 1, -1):
            for x in range(width - 1, meio[0] - 1, -1):
                if lineImage.getpixel((x, y)) == (0, 0, 0, 255):
                    imageGraf.putpixel((a, altGraf), imagemBest.getpixel((x, y)))
                    altGraf += 1
        a += 1
    for aheight in range(meio[1], -1, -1):
        lineImage = Image.new("RGBA", (width, height), (255, 255, 255, 255))
        draw = ImageDraw.Draw(lineImage)
        draw.line(
            (meio[0], meio[1], width - 1, aheight), fill=(0, 0, 0, 255), width=1
        )  # (firstX,firstY,secondX,secondY)
        altGraf = 0
        if aheight % 50 == 0:
            print(str(aheight))
            imageGraf.save("imagesgraf" + imagemNumber + ".jpg")
        for y in range(0, meio[1] + 1):
            for x in range(width - 1, meio[0] - 1, -1):
                if lineImage.getpixel((x, y)) == (0, 0, 0, 255):
                    imageGraf.putpixel((a, altGraf), imagemBest.getpixel((x, y)))
                    altGraf += 1
        a += 1
    for awidth in range(width - 1, meio[0] - 1, -1):
        lineImage = Image.new("RGBA", (width, height), (255, 255, 255, 255))
        draw = ImageDraw.Draw(lineImage)
        draw.line(
            (meio[0], meio[1], awidth, 0), fill=(0, 0, 0, 255), width=1
        )  # (firstX,firstY,secondX,secondY)
        altGraf = 0
        if awidth % 50 == 0:
            print(str(awidth))
            imageGraf.save("imagesgraf" + imagemNumber + ".jpg")
        for y in range(0, meio[1] + 1):
            for x in range(width - 1, meio[0] - 1, -1):
                if lineImage.getpixel((x, y)) == (0, 0, 0, 255):
                    imageGraf.putpixel((a, altGraf), imagemBest.getpixel((x, y)))
                    altGraf += 1
        a += 1
    for awidth in range(meio[0], -1, -1):
        lineImage = Image.new("RGBA", (width, height), (255, 255, 255, 255))
        draw = ImageDraw.Draw(lineImage)
        draw.line(
            (meio[0], meio[1], awidth, 0), fill=(0, 0, 0, 255), width=1
        )  # (firstX,firstY,secondX,secondY)
        altGraf = 0
        if awidth % 50 == 0:
            print(str(awidth))
            imageGraf.save("imagesgraf" + imagemNumber + ".jpg")
        for y in range(0, meio[1] + 1):
            for x in range(0, meio[0] + 1):
                if lineImage.getpixel((x, y)) == (0, 0, 0, 255):
                    imageGraf.putpixel((a, altGraf), imagemBest.getpixel((x, y)))
                    altGraf += 1
        a += 1
    imageGraf.save("imagesgraf" + imagemNumber + ".jpg")


if __name__ == "__main__":
    main()