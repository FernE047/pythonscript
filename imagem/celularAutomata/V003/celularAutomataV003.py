from PIL import Image

def coordDirecao(coord,n):
    if(n>7):
        n = n%8
    x,y = coord
    if n == 0:
        return(x+1,y+1)
    if n == 1:
        return(x,y+1)
    if n == 2:
        return(x-1,y+1)
    if n == 3:
        return(x+1,y)
    if n == 4:
        return(x-1,y)
    if n == 5:
        return(x+1,y-1)
    if n == 6:
        return(x,y-1)
    if n == 7:
        return(x-1,y-1)
    return (x,y)

def quantiaVizinhos(coord,imagem):
    viz = 0
    for direcao in range(8):
        coordAtual = coordDirecao(coord,direcao)
        if (max(coordAtual)<200) and (min(coordAtual)>-1) :
            if imagem.getpixel(coordAtual) == (0,0,0):
                viz += 1
            if imagem.getpixel(coordAtual) == (0,0,0,255):
                viz += 1
    return viz

imagemOrigem = Image.open("imagemInput.png")
temPreto = True
a = 0
while temPreto:
    temPreto = False
    proximoFrame = Image.new("RGBA",(200,200),(255,255,255))
    for x in range(200):
        for y in range(200):
            coord = (x,y)
            temPreto = True
            viz = quantiaVizinhos(coord,imagemOrigem)
            coordAtual = coordDirecao(coord,viz)
            if viz in range(1,4):
                if (max(coordAtual)<200) and (min(coordAtual)>-1) :
                    proximoFrame.putpixel(coordAtual,(0,0,0))
    print("imagemOutput{0:03d}.png".format(a))
    proximoFrame.save("imagemOutput{0:03d}.png".format(a))
    proximoFrame.close()
    imagemOrigem.close()
    imagemOrigem = Image.open("imagemOutput{0:03d}.png".format(a))
    a += 1
imagemOrigem.close()
