from PIL import Image
from os import listdir
from time import time


def embelezeTempo(segundos: float) -> str:
    if segundos < 0:
        segundos = -segundos
        sign = "-"
    else:
        sign = ""
    total_ms = int(round(segundos * 1000))
    ms = total_ms % 1000
    total_s = total_ms // 1000
    s = total_s % 60
    total_min = total_s // 60
    m = total_min % 60
    total_h = total_min // 60
    h = total_h % 24
    d = total_h // 24
    parts: list[str] = []

    def add(value: int, singular: str, plural: str) -> None:
        if value:
            parts.append(f"{value} {singular if value == 1 else plural}")

    add(d, "day", "days")
    add(h, "hour", "hours")
    add(m, "minute", "minutes")
    add(s, "second", "seconds")
    if ms or not parts:
        parts.append(f"{ms} millisecond" if ms == 1 else f"{ms} milliseconds")
    return sign + ", ".join(parts)

def coordDirection(coordIni,direction):
    x,y = coordIni
    if(direction == 2):
        coord = (x,y-1)
    elif(direction == 0):
        coord = (x+1,y)
    elif(direction == 1):
        coord = (x,y+1)
    else:
        coord = (x-1,y)
    return coord

def coordOppositeDirection(coord,direction):
    return coordDirection(coord,oppositeDirection(direction))

def oppositeDirection(direction):
    return 3-direction#(direction+2)%4

def testaDirection(coord,direction,imagem):
    largura,altura = imagem.size
    x,y = coord
    if direction==2:
        if y > 1:
            if imagem.getpixel((x,y-1)) == BRANCO:
                return True
    if direction==0:
        if x < largura-2:
            if imagem.getpixel((x+1,y)) == BRANCO:
                return True
    if direction==1:
        if y < altura-2:
            if imagem.getpixel((x,y+1)) == BRANCO:
                return True
    if direction==3:
        if x > 1:
            if imagem.getpixel((x-1,y)) == BRANCO:
                return True
    return False

def possibleDirections(coord,imagem):
    lista = []
    for direction in range(4):
        if testaDirection(coord,direction,imagem):
            lista.append(direction)
    return lista

BRANCO = (255,255,255,255)
PRETO = (0,0,0,255)
VERMELHO = (255,0,0,255)
imagem = Image.open(f"pureLabirint//labirint{241:04d}.png")
largura,altura = imagem.size
FINAL = (largura-2,altura-2)
INICIAL = (1,1)
coord = INICIAL
path = [-1]
it = 0
it2 = 0
inicio = time()
while coord != FINAL:
    it2 +=1
    if len(path) == 1:
        path[-1] +=1
        if(testaDirection(coord,path[-1],imagem)):
            coord = coordDirection(coord,path[-1])
            coord = coordDirection(coord,path[-1])
            path.append(-1)
            it += 1
    else:
        directionsList = possibleDirections(coord,imagem)
        if len(directionsList) == 1:                            #se o caminho for fechado, volte para trás
            coord = coordOppositeDirection(coord,path[-2])
            coord = coordOppositeDirection(coord,path[-2])
            path.pop(-1)
            while len(possibleDirections(coord,imagem)) == 2:
                coord = coordOppositeDirection(coord,path[-2])
                coord = coordOppositeDirection(coord,path[-2])
                path.pop(-1)
        elif len(directionsList) == 2:                          #se só houver uma possibilidade siga ela
            if directionsList[0] != oppositeDirection(path[-2]):
                path[-1] = directionsList[0]
            else:
                path[-1] = directionsList[1]
            coord = coordDirection(coord,path[-1])
            coord = coordDirection(coord,path[-1])
            path.append(-1)
            it += 1
        else:
            if path[-1] == 4:                                   #se todas as direções foram testadas, volte para trás
                coord = coordOppositeDirection(coord,path[-2])
                coord = coordOppositeDirection(coord,path[-2])
                path.pop(-1)
                while len(possibleDirections(coord,imagem)) == 2:
                    coord = coordOppositeDirection(coord,path[-2])
                    coord = coordOppositeDirection(coord,path[-2])
                    path.pop(-1)
            else:                                               #se tem direções faltando, vá
                path[-1] +=1
                if(path[-1] != oppositeDirection(path[-2])):
                    if(testaDirection(coord,path[-1],imagem)):
                        coord = coordDirection(coord,path[-1])
                        coord = coordDirection(coord,path[-1])
                        path.append(-1)
                        it += 1
final = time()
print("caminhos testados : "+str(it))
print("iterações feitas : "+str(it2))
print(embelezeTempo(final-inicio))
path.pop(-1)
coord = INICIAL
imagem.putpixel(coord,VERMELHO)
for direction in path:
    coord = coordDirection(coord,direction)
    imagem.putpixel(coord,VERMELHO)
    coord = coordDirection(coord,direction)
    imagem.putpixel(coord,VERMELHO)
imagem.save(f"solvedLabirint//labirintSolved{len(listdir("solvedLabirint")):03d}.png")
imagem.close()
