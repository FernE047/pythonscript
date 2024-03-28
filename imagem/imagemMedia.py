from PIL import Image
import os
aImage=Image.open('a.jpg')
bImage=Image.open('b.jpg')
width, height =aImage.size
faixa=Image.new('RGB', (width, height), 'white')
for x in range(width):
    for y in range(height):
        pixelA=aImage.getpixel((x,y))
        pixelB=bImage.getpixel((x,y))
        faixa.putpixel((x, y), (int((pixelA[0]+pixelB[0])/2),int((pixelA[1]+pixelB[1])/2),int((pixelA[2]+pixelB[2])/2)))
faixa.save('c8.jpg')
print('veja')
