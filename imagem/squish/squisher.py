from PIL import Image


def open_image_as_rgba(image_path: str) -> Image.Image:
    with Image.open(image_path) as image:
        image_in_memory = image.copy()
        if image.mode != "RGBA":
            return image_in_memory.convert("RGBA")
        return image_in_memory


def main() -> None:
    imagem = open_image_as_rgba("input.png")
    tamanho = imagem.size
    squished = Image.new("RGBA",tamanho,(255,255,255,255))
    xPosition = 0
    yPosition = 0
    corMemory = imagem.getpixel((0,0))

    for y in range(0,tamanho[1]):
        for x in range(0,tamanho[0]):
            corAtual = imagem.getpixel((x,y))
            if corAtual != corMemory or x == tamanho[0]-1 :
                squished.putpixel((xPosition,yPosition),corMemory)
                xPosition +=1
                corMemory = corAtual
        yPosition += 1
        xPosition = 0
    print("outputA.png")
    squished.save("outputA.png")
    squished = Image.new("RGBA",tamanho,(255,255,255,255))
    xPosition = 0
    yPosition = 0
    corMemory = imagem.getpixel((0,0))

    for x in range(0,tamanho[0]):
        for y in range(0,tamanho[1]):
            corAtual = imagem.getpixel((x,y))
            if corAtual != corMemory or y == tamanho[1]-1 :
                squished.putpixel((xPosition,yPosition),corMemory)
                yPosition +=1
                corMemory = corAtual
        xPosition += 1
        yPosition = 0
    print("outputB.png")
    squished.save("outputB.png")

    squished = Image.new("RGBA",tamanho,(255,255,255,255))
    xPosition = tamanho[0]-1
    yPosition = 0
    corMemory = imagem.getpixel((tamanho[0]-1,0))
    for y in range(0,tamanho[1]):
        for x in range(tamanho[0]-1,-1,-1):
            corAtual = imagem.getpixel((x,y))
            if corAtual != corMemory or x == 0 :
                squished.putpixel((xPosition,yPosition),corMemory)
                xPosition -= 1
                corMemory = corAtual
        yPosition += 1
        xPosition = tamanho[0]-1
    print("outputC.png")
    squished.save("outputC.png")

    squished = Image.new("RGBA",tamanho,(255,255,255,255))
    xPosition = 0
    yPosition = tamanho[1]-1
    corMemory = imagem.getpixel((0,tamanho[1]-1))
    for x in range(0,tamanho[0]):
        for y in range(tamanho[1]-1,-1,-1):
            corAtual = imagem.getpixel((x,y))
            if corAtual != corMemory or y == 0 :
                squished.putpixel((xPosition,yPosition),corMemory)
                yPosition -= 1
                corMemory = corAtual
        xPosition += 1
        yPosition = tamanho[1]-1
    print("outputD.png")
    squished.save("outputD.png")


if __name__ == "__main__":
    main()