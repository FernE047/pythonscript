from PIL import Image
from os import listdir

def coordDirection(coordIni,direction):
    x,y = coordIni
    if(direction == 0):
        coord = (x,y+1)
    elif(direction == 1):
        coord = (x+1,y)
    elif(direction == 2):
        coord = (x,y-1)
    else:
        coord = (x-1,y)
    return coord

def isSolved(labirint):
    return labirint.getpixel(FINAL) == VERMELHO

def labirintSolver(labirint,coord,path):
    """print(coord)
    print(path)"""
    if not isSolved(labirint):
        for direction in range(4):
            if direction == (path[-1]-2)%4:
                continue
            else:
                path.append(direction)
            testCoord = coordDirection(coord,direction)
            nextCoord = coordDirection(testCoord,direction)
            try:
                nextPixel = labirint.getpixel(nextCoord)
                nextPixel = labirint.getpixel(testCoord)
            except:
                path.pop()
                continue
            if nextPixel == BRANCO:
                if nextCoord == FINAL:
                    labirint.putpixel(nextCoord,VERMELHO)
                else:
                    labirintSolver(labirint,nextCoord,path)
            if isSolved(labirint):
                imagem.putpixel(testCoord,VERMELHO)
                imagem.putpixel(nextCoord,VERMELHO)
                break
            path.pop()


def main() -> None:
    BRANCO = (255,255,255,255)
    PRETO = (0,0,0,255)
    VERMELHO = (255,0,0,255)
    imagem = Image.open(f"pureLabirint//labirint{234:04d}.png")
    largura,altura = imagem.size
    FINAL = (largura-2,altura-2)
    INICIAL = (1,1)
    path = [8]
    labirintSolver(imagem,INICIAL,path)
    imagem.save(f"labirintSolved{len(listdir("pureLabirint")):03d}.png")
    imagem.close()


if __name__ == "__main__":
    main()