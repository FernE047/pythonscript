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

imagemOrigem = Image.open("imagemInput.png")
temPreto = True
a = 0
while temPreto:
    temPreto = False
    proximoFrame = Image.new("RGBA",(200,200),(255,255,255))
    for x in range(200):
        for y in range(200):
            coord = (x,y)
            if imagemOrigem.getpixel(coord) in [(0,0,0),(0,0,0,255)]:
                temPreto = True
                for d in range(8):
                    coordAtual = coordDirecao(coord,d)
                    if (max(coordAtual)<200) and (min(coordAtual)>-1) :
                        if imagemOrigem.getpixel(coordAtual) not in [(0,0,0),(0,0,0,255)]:
                            proximoFrame.putpixel(coordAtual,(0,0,0))
    print(f"imagemOutput{a:03d}.png")
    proximoFrame.save(f"imagemOutput{a:03d}.png")
    proximoFrame.close()
    imagemOrigem.close()
    imagemOrigem = Image.open(f"imagemOutput{a:03d}.png")
    a += 1
imagemOrigem.close()
