from PIL import Image
from colorsys import hsv_to_rgb

def fazImagem(pontoFinal,nome):
    image = Image.new("RGBA",(256,256),(0,0,100))
    distancia = lambda ponto1,ponto2:((ponto1[0]-ponto2[0])**2+(ponto1[1]-ponto2[1])**2)**0.5
    D = distancia((0,0),pontoFinal)
    for x in range(256):
        for y in range(256):
            image.putpixel((x,y),tuple([int(a) for a in hsv_to_rgb(0,0,distancia((x,y),pontoFinal)/D*255)]))
    image.save(nome)

fazImagem((255,255),"C:\\Users\\Programador\\Desktop\\pic1.png")
fazImagem((127,127),"C:\\Users\\Programador\\Desktop\\pic2.png")
fazImagem((185,220),"C:\\Users\\Programador\\Desktop\\pic3.png")

